"""Deterministic CSV output for contract 2.0; no scoring logic."""
import csv
import math
import re
from pathlib import Path

SCHEMAS = {
    'nodes_roles.csv': ['gid', 'role', 'role_score', 'cluster_id', 'priority_score', 'evidence'],
    'clusters.csv': ['cluster_id', 'n_nodes', 'n_seed', 'sum_kzt_internal', 'top_gids', 'hypothesis'],
    'top_nodes.csv': ['rank', 'gid', 'role', 'priority_score', 'why'],
}
ROLES = {'coordinator', 'consolidator', 'distributor', 'transit', 'terminal', 'peripheral'}


def records(table):
    return table.to_dict(orient='records') if hasattr(table, 'to_dict') else list(table)


def gid(value):
    # Reject floats: converting one to int could silently preserve an already rounded ID.
    text = str(value)
    if not re.fullmatch(r'[0-9]{1,19}', text) or int(text) > 2**63 - 1:
        raise ValueError(f'Некорректный gid: {text}')
    return str(int(text))


def write_csvs(directory: Path, nodes, clusters, top):
    tables = {
        'nodes_roles.csv': sorted(records(nodes), key=lambda n: (-round(float(n['priority_score']), 6), int(gid(n['gid'])))),
        'clusters.csv': sorted(records(clusters), key=lambda c: c['cluster_id']),
        'top_nodes.csv': sorted(records(top), key=lambda n: n['rank'])[:20],
    }
    for name, rows in tables.items():
        with (directory / name).open('w', encoding='utf-8', newline='') as stream:
            writer = csv.DictWriter(stream, fieldnames=SCHEMAS[name], lineterminator='\n')
            writer.writeheader()
            for row in rows:
                values = {key: row[key] for key in SCHEMAS[name]}
                if 'gid' in values:
                    values['gid'] = gid(values['gid'])
                if 'top_gids' in values:
                    values['top_gids'] = ';'.join(gid(item) for item in values['top_gids'])
                for key, precision in [('role_score', 4), ('priority_score', 6), ('sum_kzt_internal', 2)]:
                    if key in values:
                        number = float(values[key])
                        if not math.isfinite(number):
                            raise ValueError(f'{name}: {key} должен быть конечным')
                        values[key] = f'{number:.{precision}f}'
                writer.writerow(values)


def validate_csvs(directory: Path, source_nodes):
    tables = {}
    for name, columns in SCHEMAS.items():
        raw = (directory / name).read_bytes()
        if raw.startswith(b'\xef\xbb\xbf') or b'\r\n' in raw:
            raise ValueError(f'{name}: неверная кодировка или переводы строк')
        with (directory / name).open(encoding='utf-8', newline='') as stream:
            reader = csv.DictReader(stream)
            if reader.fieldnames != columns:
                raise ValueError(f'{name}: неверные колонки')
            tables[name] = list(reader)
        for row in tables[name]:
            if any(value is None or not value.strip() for value in row.values()):
                raise ValueError(f'{name}: пустое обязательное поле')
    nodes = tables['nodes_roles.csv']
    source = records(source_nodes)
    expected = {gid(n['gid']) for n in source}
    by_gid = {n['gid']: n for n in nodes}
    if len(expected) != len(source) or len(by_gid) != len(nodes) or set(by_gid) != expected:
        raise ValueError('Множество gid не совпадает с входными узлами или содержит дубли')
    for node in nodes:
        gid(node['gid'])
        if node['role'] not in ROLES or not 0 < len(node['evidence']) <= 200:
            raise ValueError('Некорректная роль или evidence')
        for field in ['role_score', 'priority_score']:
            if not 0 <= float(node[field]) <= 1:
                raise ValueError(f'Некорректный {field}')
    for node in source:
        if node['is_boundary'] and by_gid[gid(node['gid'])]['role'] == 'terminal':
            raise ValueError('Узел границы не может иметь роль terminal')
    clusters = tables['clusters.csv']
    cluster_ids = {int(c['cluster_id']) for c in clusters}
    if len(cluster_ids) != len(clusters) or sum(int(c['n_nodes']) for c in clusters) != len(nodes):
        raise ValueError('Некорректные размеры кластеров')
    for node in nodes:
        if int(node['cluster_id']) not in cluster_ids:
            raise ValueError('Неизвестный кластер')
    for cluster in clusters:
        members = {n['gid'] for n in nodes if n['cluster_id'] == cluster['cluster_id']}
        if len(members) != int(cluster['n_nodes']) or not 0 <= int(cluster['n_seed']) <= len(members):
            raise ValueError('Состав кластера не совпадает с n_nodes/n_seed')
        amount = float(cluster['sum_kzt_internal'])
        if not math.isfinite(amount) or amount < 0:
            raise ValueError('Некорректный оборот кластера')
        leaders = cluster['top_gids'].split(';')
        if len(leaders) > 5 or len(set(leaders)) != len(leaders) or not set(leaders) <= members:
            raise ValueError('Некорректный top_gids')
    top = tables['top_nodes.csv']
    if len(top) != min(20, len(nodes)) or len({n['gid'] for n in top}) != len(top):
        raise ValueError('Неверный размер или дубли top_nodes')
    for rank, item in enumerate(top, 1):
        node = by_gid.get(item['gid'])
        if int(item['rank']) != rank or node is None or any(item[k] != node[k] for k in ['role', 'priority_score']):
            raise ValueError('top_nodes не согласован с nodes_roles')
    ordered = sorted(nodes, key=lambda n: (-float(n['priority_score']), int(n['gid'])))
    if nodes != ordered or [n['gid'] for n in top] != [n['gid'] for n in ordered[:20]]:
        raise ValueError('Неверная сортировка приоритета')
