import hashlib
import json
import math
import re
import sqlite3
from dataclasses import dataclass
from datetime import datetime, date, timezone
from pathlib import Path


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


@dataclass
class Snapshot:
    run_id: str
    scope: str
    created: str
    synthetic: bool
    nodes: dict
    edges: dict
    fingerprint: str
    period: dict

    @classmethod
    def parse(cls, graph, overview, source):
        run = graph.get('run_id')
        if not isinstance(run, str) or not 1 <= len(run) <= 100 or run != overview.get('run_id') or overview.get('status') != 'succeeded':
            raise ValueError('Нет согласованного успешного снимка.')
        created = datetime.fromisoformat(overview['created_at'].replace('Z', '+00:00'))
        if created.tzinfo is None:
            raise ValueError('Время снимка должно содержать часовой пояс.')
        period = overview['period']
        if date.fromisoformat(period['from']) > date.fromisoformat(period['to']):
            raise ValueError('Некорректный период.')
        raw_nodes, raw_edges = graph['nodes'], graph['edges']
        if not isinstance(raw_nodes, list) or not isinstance(raw_edges, list) or len(raw_nodes) > 100000 or len(raw_edges) > 200000:
            raise ValueError('Некорректный или слишком большой снимок.')
        nodes, edges = {}, {}
        for node in raw_nodes:
            gid, score = node['gid'], node['priority_score']
            if not isinstance(gid, str) or not re.fullmatch(r'\d{1,24}', gid) or gid in nodes:
                raise ValueError('GID должен быть уникальной строкой цифр.')
            if isinstance(score, bool) or not isinstance(score, (int, float)) or not math.isfinite(score) or not 0 <= score <= 1:
                raise ValueError('Некорректная оценка приоритета.')
            nodes[gid] = node
        for edge in raw_edges:
            src, dst = edge['src'], edge['dst']
            if not isinstance(src, str) or not isinstance(dst, str) or src not in nodes or dst not in nodes or (src, dst) in edges:
                raise ValueError('Некорректная или повторяющаяся связь.')
            amount = edge.get('sum_kzt', 0)
            if isinstance(amount, bool) or not isinstance(amount, (int, float)) or not math.isfinite(amount) or amount < 0:
                raise ValueError('Некорректная сумма связи.')
            edges[src, dst] = {'src': src, 'dst': dst, 'sum_kzt': amount,
                               'priority': max(nodes[src]['priority_score'], nodes[dst]['priority_score'])}
        counts = overview.get('counts', {})
        if counts.get('nodes') != len(nodes) or counts.get('edges') != len(edges):
            raise ValueError('Количество узлов/связей не совпадает с обзором.')
        synthetic = overview.get('_synthetic') is True
        methodology = overview.get('methodology_version')
        if not isinstance(methodology, str) or not methodology:
            raise ValueError('Не указана методология снимка.')
        scope = digest([source, period, methodology, synthetic])
        return cls(run, scope, created.astimezone(timezone.utc).isoformat(), synthetic,
                   nodes, edges, digest(graph), period)


class Store:
    def __init__(self, path):
        if str(path) != ':memory:':
            Path(path).parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        self.db = sqlite3.connect(path)
        self.db.row_factory = sqlite3.Row
        self.db.executescript('''
          CREATE TABLE IF NOT EXISTS meta (key TEXT PRIMARY KEY, value TEXT NOT NULL);
          CREATE TABLE IF NOT EXISTS seen (src TEXT, dst TEXT, PRIMARY KEY(src,dst));
          CREATE TABLE IF NOT EXISTS runs (run TEXT PRIMARY KEY, fingerprint TEXT NOT NULL);
          CREATE TABLE IF NOT EXISTS subscribers (uid INTEGER PRIMARY KEY, active INTEGER NOT NULL);
          CREATE TABLE IF NOT EXISTS identities (uid INTEGER PRIMARY KEY, epoch TEXT NOT NULL);
          CREATE TABLE IF NOT EXISTS attempts (uid INTEGER PRIMARY KEY, count INTEGER, until REAL);
          CREATE TABLE IF NOT EXISTS events (id TEXT PRIMARY KEY, payload TEXT NOT NULL, created TEXT NOT NULL);
          CREATE TABLE IF NOT EXISTS deliveries (event TEXT, uid INTEGER, sent INTEGER DEFAULT 0,
            attempts INTEGER DEFAULT 0, retry_at REAL DEFAULT 0, PRIMARY KEY(event,uid));
          CREATE TABLE IF NOT EXISTS reviews (event TEXT, uid INTEGER, PRIMARY KEY(event,uid));
        ''')
        if str(path) != ':memory:':
            Path(path).chmod(0o600)

    def get(self, key, default=''):
        row = self.db.execute('SELECT value FROM meta WHERE key=?', (key,)).fetchone()
        return row[0] if row else default

    def put(self, key, value):
        self.db.execute('INSERT OR REPLACE INTO meta VALUES (?,?)', (key, str(value)))

    def subscribe(self, uid, active):
        with self.db:
            self.db.execute('INSERT OR REPLACE INTO subscribers VALUES (?,?)', (uid, int(active)))
            if not active:
                self.db.execute('UPDATE deliveries SET sent=2 WHERE uid=? AND sent=0', (uid,))

    def ingest(self, snapshot, allowed, minimum=0, allow_real=False):
        if not snapshot.synthetic and not allow_real:
            raise ValueError('Реальные данные отключены: требуется ALLOW_REAL_DATA=1 после согласования.')
        run_key = digest([snapshot.scope, snapshot.run_id])
        if self.get('created') and snapshot.created < self.get('created'):
            raise ValueError('Отклонён устаревший снимок.')
        previous = self.db.execute('SELECT fingerprint FROM runs WHERE run=?', (run_key,)).fetchone()
        if previous:
            if previous[0] != snapshot.fingerprint:
                raise ValueError('Содержимое опубликованного снимка изменилось без нового run_id.')
            if self.get('scope') == snapshot.scope:
                return 'unchanged'
        reset = self.get('scope') != snapshot.scope
        seen = set() if reset else {(row[0], row[1]) for row in self.db.execute('SELECT src,dst FROM seen')}
        new = [value for key, value in snapshot.edges.items() if key not in seen]
        eligible = sorted((edge for edge in new if edge['priority'] >= minimum), key=lambda edge: (-edge['priority'], edge['src'], edge['dst']))
        now = datetime.now(timezone.utc).isoformat()
        with self.db:
            if reset:
                self.db.execute('DELETE FROM seen')
                self.db.execute('UPDATE deliveries SET sent=2 WHERE sent=0')
            self.db.executemany('INSERT OR IGNORE INTO seen VALUES (?,?)', snapshot.edges.keys())
            self.db.execute('INSERT OR IGNORE INTO runs VALUES (?,?)', (run_key, snapshot.fingerprint))
            self.put('scope', snapshot.scope); self.put('created', snapshot.created); self.put('run', snapshot.run_id)
            self.put('last_check', now); self.put('edges', len(snapshot.edges)); self.put('nodes', len(snapshot.nodes))
            if eligible and not reset:
                event_id = digest([snapshot.scope, snapshot.run_id])[:16]
                payload = {'id': event_id, 'run': snapshot.run_id, 'count': len(eligible), 'total_new': len(new),
                           'samples': eligible[:5], 'synthetic': snapshot.synthetic, 'period': snapshot.period,
                           'created': now, 'priority': eligible[0]['priority']}
                self.db.execute('INSERT INTO events VALUES (?,?,?)', (event_id, json.dumps(payload), now))
                recipients = [row[0] for row in self.db.execute('SELECT uid FROM subscribers WHERE active=1') if row[0] in allowed]
                self.db.executemany('INSERT INTO deliveries(event,uid) VALUES (?,?)', [(event_id, uid) for uid in recipients])
        return 'baseline' if reset else f'new:{len(eligible)}'

    def event(self, event_id):
        row = self.db.execute('SELECT payload FROM events WHERE id=?', (event_id,)).fetchone()
        return json.loads(row[0]) if row else None

    def latest(self, uid):
        return [json.loads(row[0]) for row in self.db.execute('''SELECT e.payload FROM events e
          JOIN deliveries d ON d.event=e.id WHERE d.uid=? AND d.sent=1 ORDER BY e.created DESC LIMIT 5''', (uid,))]

    def close(self):
        self.db.close()
