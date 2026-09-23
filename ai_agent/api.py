"""Register optional agent endpoints before any catch-all frontend mount."""
import asyncio
import json
from pathlib import Path
from fastapi import APIRouter, Request
from fastapi.responses import FileResponse, JSONResponse
from .config import enabled
from .service import Assistant, AssistantError
from graph.query import SnapshotTools, ToolError


def install(app, get_snapshot, *, assistant_factory=Assistant, replace_disabled=False):
    path = '/api/v1/assistant'
    existing = [r for r in app.router.routes if getattr(r, 'path', None) == path]
    if existing and not replace_disabled:
        raise ValueError('Маршрут assistant уже есть; явно разрешите замену обработчика')
    if replace_disabled:
        app.router.routes[:] = [r for r in app.router.routes if r not in existing]
    router = APIRouter()
    gate = asyncio.Semaphore(2)
    cached = {'snapshot': None, 'tools': None}

    def queries():
        snap = get_snapshot()
        if snap is None:
            return None
        if cached['snapshot'] is not snap:
            tools = SnapshotTools(snap)
            cached.update(snapshot=snap, tools=tools)
        return cached['tools']

    @router.get('/api/v1/assistant/status')
    def status():
        snap = get_snapshot()
        return {'enabled': enabled(), 'ready': snap is not None, 'mode': 'ai' if enabled() else 'fallback',
                'run_id': snap.get('run', {}).get('run_id') if snap else None}

    @router.post(path)
    async def ask(request: Request):
        origin = request.headers.get('origin')
        own_origin = f'{request.url.scheme}://{request.url.netloc}'
        if origin and origin not in (own_origin, 'http://localhost:5173', 'http://127.0.0.1:5173'):
            return error('invalid_param', 'Источник запроса не разрешён', 400)
        # Bound the received body, including chunked requests.
        raw = bytearray()
        async for chunk in request.stream():
            raw.extend(chunk)
            if len(raw) > 65536:
                return error('invalid_param', 'Запрос слишком большой', 400)
        try:
            body = json.loads(raw)
            if not isinstance(body, dict) or set(body) - {'question', 'history'} or 'question' not in body:
                raise ValueError()
            q, h = body['question'], body.get('history', [])
            if not isinstance(q, str) or not q.strip() or len(q) > 4000:
                raise ValueError()
            if not isinstance(h, list) or len(h) > 6 or any(not isinstance(x, dict) or set(x) != {'role', 'content'} or x['role'] not in ('user', 'assistant') or not isinstance(x['content'], str) or len(x['content']) > 4000 for x in h):
                raise ValueError()
        except (ValueError, TypeError, KeyError):
            return error('invalid_param', 'Ожидаются question (1–4000 символов) и history (до 6 сообщений user/assistant)', 400)
        snap = get_snapshot()
        if snap is None:
            return error('no_result', 'Сначала выполните расчёт графа', 503)
        if gate.locked():
            return error('internal', 'Ассистент занят. Повторите запрос позже.', 500)
        async with gate:
            try:
                agent = assistant_factory(snap)
                answer = await agent.ask(q, h)
                # Keep the backend team's additive run_id field and expose it to the widget.
                run_id = snap.get('run', {}).get('run_id', '')
                return JSONResponse(dict(answer, run_id=run_id), headers={'X-Analysis-Run-Id': str(run_id)})
            except AssistantError as exc:
                return JSONResponse(exc.response(), status_code=exc.status)
            except Exception:
                return error('internal', 'Сервис ассистента временно недоступен', 500)

    @router.get('/api/v1/assistant/node/{gid}')
    def node_card(gid: str):
        tools = queries()
        if tools is None:
            return error('no_result', 'Сначала выполните расчёт графа', 503)
        try:
            return tools.get_node(gid)
        except ToolError as exc:
            return error(exc.code, str(exc), 404 if exc.code == 'not_found' else 400)

    @router.get('/api/v1/assistant/suggestions')
    def suggestions():
        tools = queries()
        if tools is None:
            return {'items': []}
        top = tools.ordered(tools.nodes)
        items = ['Кого из участников графа проверить в первую очередь и почему?']
        if top:
            items.append(f'Объясни роль и ограничения данных для #{top[0]}')
        groups = {}
        for n in tools.nodes.values():
            if n.get('is_seed'):
                groups.setdefault(n['cluster_id'], []).append(n['gid'])
        if groups:
            chosen = sorted(groups.values(), key=lambda x: (-len(x), min(int(g) for g in x)))[0]
            gids = sorted(chosen, key=int)[:5]
            if len(gids) >= 2:
                items.append('Кто собирает деньги с этих участников: ' + ', '.join('#'+g for g in gids) + '?')
        return {'items': items}

    ui = Path(__file__).parent / 'ui'

    @router.get('/assistant', include_in_schema=False)
    def console():
        return FileResponse(ui / 'index.html', media_type='text/html')

    @router.get('/analysis-extras', include_in_schema=False)
    def extras_screen():
        return FileResponse(ui / 'extras.html', media_type='text/html')

    @router.get('/ai-agent/assistant.js', include_in_schema=False)
    def widget():
        return FileResponse(ui / 'assistant.js', media_type='application/javascript')

    app.router.routes[0:0] = router.routes
    app.openapi_schema = None
    return router


def error(code, message, status):
    return JSONResponse({'error': {'code': code, 'message': message, 'details': {}}}, status_code=status)
