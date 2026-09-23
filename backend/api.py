"""Read-only snapshot API. Reload swaps a complete state in one assignment."""
import json
import logging
import os
import re
from collections import deque
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Literal

from fastapi import FastAPI, Query, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException
from .export import ROLES, SCHEMAS
from .assistant import REQUEST_SCHEMA, answer, readiness

SHORT = 'gid role role_score priority_score priority_rank cluster_id is_seed is_boundary is_isolated depth x y'.split()
DETAIL = 'rule_id rule_text thresholds values strength alternatives limitations priority_contributions why'.split()
PREFIX = '/api/v1'


class ApiError(Exception):
    def __init__(self, code, message, status=400):
        self.code, self.message, self.status = code, message, status


def short(node):
    return {key: node[key] for key in SHORT}


class Snapshot:
    def __init__(self, output):
        marker = output / 'LATEST'
        if not marker.exists():
            raise ApiError('no_result', 'Нет успешного результата. Сначала запустите pipeline.', 503)
        run_id = marker.read_text(encoding='utf-8').strip()
        if not re.fullmatch(r'[0-9]{8}T[0-9]{6}Z-[0-9a-f]{8}', run_id):
            raise ValueError('Некорректный LATEST')
        self.directory = output / 'runs' / run_id
        self.data = json.loads((self.directory / 'snapshot.json').read_text(encoding='utf-8'))
        if self.data['run']['run_id'] != run_id:
            raise ValueError('run_id снимка не совпадает с LATEST')
        self.nodes = {n['gid']: n for n in self.data['nodes']}
        if len(self.nodes) != len(self.data['nodes']):
            raise ValueError('Повторяющиеся gid в снимке')
        self.clusters = {c['cluster_id']: c for c in self.data['clusters']}
        self.members = {cid: [] for cid in self.clusters}
        self.incoming = {gid: [] for gid in self.nodes}
        self.outgoing = {gid: [] for gid in self.nodes}
        for node in self.nodes.values():
            if not isinstance(node['gid'], str) or not re.fullmatch(r'[0-9]{1,19}', node['gid']):
                raise ValueError('gid должен быть десятичной строкой')
            short(node)
            self.members[node['cluster_id']].append(node)
        for edge in self.data['edges']:
            self.outgoing[edge['src']].append(edge)
            self.incoming[edge['dst']].append(edge)
        for name in SCHEMAS:
            if not (self.directory / name).is_file():
                raise ValueError(f'Нет файла результата: {name}')

    def node(self, gid):
        if not re.fullmatch(r'[0-9]{1,19}', gid):
            raise ApiError('invalid_gid', 'gid должен содержать от 1 до 19 цифр')
        if gid not in self.nodes:
            raise ApiError('not_found', 'Узел не найден', 404)
        return self.nodes[gid]

    def cluster(self, cid):
        if cid not in self.clusters:
            raise ApiError('not_found', 'Кластер не найден', 404)
        return self.clusters[cid]


def create_app(output_dir=None, frontend_dir=None):
    output = Path(output_dir or os.getenv('OUTPUT_DIR', str(Path(__file__).parent / 'output'))).resolve()

    @asynccontextmanager
    async def lifespan(app):
        app.state.snapshot = None
        try:
            app.state.snapshot = Snapshot(output)
        except ApiError:
            pass
        except Exception:
            logging.exception('Не удалось загрузить снимок')
        yield

    app = FastAPI(title='Граф денег — API', version='2.0', lifespan=lifespan,
                  docs_url=None, redoc_url=None)
    app.add_middleware(CORSMiddleware, allow_origins=['http://localhost:5173', 'http://127.0.0.1:5173'],
                       allow_methods=['GET', 'POST'], allow_headers=['*'])

    @app.exception_handler(ApiError)
    async def api_error(request, exc):
        return JSONResponse({'error': {'code': exc.code, 'message': exc.message, 'details': {}}}, status_code=exc.status)

    @app.exception_handler(RequestValidationError)
    async def bad_param(request, exc):
        return await api_error(request, ApiError('invalid_param', 'Некорректные параметры запроса'))

    @app.exception_handler(HTTPException)
    async def http_error(request, exc):
        return await api_error(request, ApiError('not_found' if exc.status_code == 404 else 'invalid_param',
                                                'Ресурс не найден' if exc.status_code == 404 else 'Запрос не поддерживается', exc.status_code))

    @app.exception_handler(Exception)
    async def internal(request, exc):
        logging.error('Ошибка API', exc_info=(type(exc), exc, exc.__traceback__))
        return await api_error(request, ApiError('internal', 'Внутренняя ошибка сервиса', 500))

    def state():
        current = app.state.snapshot
        if current is None:
            raise ApiError('no_result', 'Нет успешного результата. Сначала запустите pipeline.', 503)
        return current

    @app.get(PREFIX + '/health')
    def health():
        current = app.state.snapshot
        enabled, message = readiness()
        return {'status': 'ok', 'run_id': current.data['run']['run_id'] if current else None,
                'assistant_enabled': enabled, 'assistant_message': message}

    @app.get(PREFIX + '/overview')
    def overview():
        current = app.state.snapshot
        attempt = output / 'last_attempt.json'
        return {**(current.data['run'] if current else {'status': 'no_result', 'run_id': None}),
                'last_attempt': json.loads(attempt.read_text(encoding='utf-8')) if attempt.exists() else None}

    @app.post(PREFIX + '/reload')
    def reload():
        replacement = Snapshot(output)
        app.state.snapshot = replacement
        return {'run_id': replacement.data['run']['run_id']}

    @app.get(PREFIX + '/graph')
    def graph():
        s = state()
        return {'nodes': [short(n) for n in s.nodes.values()], 'edges': s.data['edges'], 'run_id': s.data['run']['run_id']}

    @app.get(PREFIX + '/nodes')
    def nodes(q: str = '', role: str | None = None, cluster_id: int | None = Query(None, ge=0),
              is_seed: bool | None = None, sort: Literal['priority', 'gid'] = 'priority',
              limit: int = Query(50, ge=1, le=200), offset: int = Query(0, ge=0)):
        s = state()
        if role is not None and role not in ROLES:
            raise ApiError('invalid_param', 'Неизвестная роль')
        items = [n for n in s.nodes.values() if n['gid'].startswith(q) and (role is None or n['role'] == role)
                 and (cluster_id is None or n['cluster_id'] == cluster_id) and (is_seed is None or n['is_seed'] == is_seed)]
        items.sort(key=lambda n: (len(n['gid']), n['gid']) if sort == 'gid' else (-n['priority_score'], int(n['gid'])))
        return {'items': [short(n) for n in items[offset:offset + limit]], 'total': len(items), 'limit': limit, 'offset': offset}

    @app.get(PREFIX + '/nodes/{gid}')
    def node(gid: str):
        n = state().node(gid)
        return {'node': {k: v for k, v in n.items() if k not in DETAIL and k != 'evidence_detail'},
                'evidence_detail': n.get('evidence_detail', {k: n[k] for k in DETAIL if k in n})}

    @app.get(PREFIX + '/nodes/{gid}/neighbors')
    def neighbors(gid: str, direction: Literal['in', 'out', 'both'] = 'both', limit: int = Query(50, ge=1, le=500)):
        s = state()
        s.node(gid)
        edges = (s.incoming[gid] if direction != 'out' else []) + (s.outgoing[gid] if direction != 'in' else [])
        edges = list({(e['src'], e['dst']): e for e in edges}.values())
        edges.sort(key=lambda e: (-e['sum_kzt'], int(e['src']), int(e['dst'])))
        return {'items': [{'edge': e, 'node': short(s.nodes[e['dst'] if e['src'] == gid else e['src']])} for e in edges[:limit]],
                'total': len(edges), 'truncated': len(edges) > limit}

    @app.get(PREFIX + '/subgraph')
    def subgraph(gid: str | None = None, depth: int = Query(1, ge=1, le=2),
                 cluster_id: int | None = Query(None, ge=0), max_nodes: int = Query(300, ge=1, le=500)):
        s = state()
        if (gid is None) == (cluster_id is None):
            raise ApiError('invalid_param', 'Укажите либо gid, либо cluster_id')
        truncated = False
        if gid is not None:
            s.node(gid)
            selected, queue = {gid}, deque([(gid, 0)])
            while queue:
                current, level = queue.popleft()
                if level == depth:
                    continue
                linked = {e['src'] for e in s.incoming[current]} | {e['dst'] for e in s.outgoing[current]}
                for neighbor in sorted(linked, key=int):
                    if neighbor in selected:
                        continue
                    if len(selected) == max_nodes:
                        truncated = True
                    else:
                        selected.add(neighbor)
                        queue.append((neighbor, level + 1))
        else:
            s.cluster(cluster_id)
            members = sorted(s.members[cluster_id], key=lambda n: (-n['priority_score'], int(n['gid'])))
            selected = {n['gid'] for n in members[:max_nodes]}
            truncated = len(members) > max_nodes
        return {'nodes': [short(s.nodes[g]) for g in sorted(selected, key=int)],
                'edges': [e for e in s.data['edges'] if e['src'] in selected and e['dst'] in selected],
                'truncated': truncated, 'limits': {'max_nodes': max_nodes}}

    @app.get(PREFIX + '/top')
    def top(n: int = Query(20, ge=1, le=100)):
        s = state()
        return {'items': [dict(item, role_score=s.nodes[item['gid']]['role_score'], cluster_id=s.nodes[item['gid']]['cluster_id'])
                          for item in s.data['top'][:n]], 'run_id': s.data['run']['run_id']}

    @app.get(PREFIX + '/clusters')
    def clusters(limit: int = Query(50, ge=1, le=200), offset: int = Query(0, ge=0)):
        s = state()
        items = sorted(s.clusters.values(), key=lambda c: c['cluster_id'])
        return {'items': items[offset:offset + limit], 'total': len(items)}

    @app.get(PREFIX + '/clusters/{cluster_id}')
    def cluster(cluster_id: int):
        s = state()
        return {'cluster': s.cluster(cluster_id), 'nodes': [short(n) for n in s.members[cluster_id]]}

    @app.get(PREFIX + '/export/{name}')
    def export(name: str):
        s = state()
        if name not in SCHEMAS:
            raise ApiError('invalid_param', 'Неизвестное имя CSV')
        return FileResponse(s.directory / name, media_type='text/csv; charset=utf-8', filename=name)

    @app.post(PREFIX + '/assistant', openapi_extra={
        'requestBody': {'required': True, 'content': {'application/json': {'schema': REQUEST_SCHEMA}}}
    })
    async def assistant(request: Request):
        return await answer(request, state)

    @app.get('/check', response_class=HTMLResponse, include_in_schema=False)
    def check():
        return (Path(__file__).parent / 'check.html').read_text(encoding='utf-8')

    dist = Path(frontend_dir) if frontend_dir is not None else Path(__file__).parent.parent / 'Frontend' / 'dist'
    if (dist / 'index.html').exists():
        app.mount('/', StaticFiles(directory=dist, html=True), name='frontend')
    else:
        app.add_api_route('/', check, response_class=HTMLResponse, include_in_schema=False)
    return app


app = create_app()
