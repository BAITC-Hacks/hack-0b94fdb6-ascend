"""Compose the existing backend with the agent, without editing teammate files."""
from .api import install
from .config import enabled


def create_app(output_dir=None, *, snapshot_path=None, assistant_factory=None):
    from backend.api import create_app as backend_app
    app = backend_app(output_dir=output_dir)
    if snapshot_path is not None:
        # Explicit standalone graph snapshot for local agent development.
        import json
        from pathlib import Path
        snapshot = json.loads(Path(snapshot_path).read_text(encoding='utf-8'))
        if not isinstance(snapshot, dict) or not all(k in snapshot for k in ('run', 'nodes', 'edges', 'clusters')):
            raise ValueError('Некорректный файл снимка')
        def get_snapshot():
            return snapshot
    else:
        def get_snapshot():
            current = getattr(app.state, 'snapshot', None)
            return current.data if current else None
    kwargs = {'assistant_factory': assistant_factory} if assistant_factory else {}
    install(app, get_snapshot, replace_disabled=True, **kwargs)
    # Backend health must report the actual optional assistant state.
    app.router.routes[:] = [r for r in app.router.routes if getattr(r, 'path', None) != '/api/v1/health']
    from fastapi.routing import APIRoute
    def health():
        snap = get_snapshot()
        active = enabled()
        return {'status': 'ok', 'run_id': snap['run'].get('run_id') if snap else None,
                'assistant_enabled': active,
                'assistant_message': 'Настроен. Доступ к модели проверяется при отправке вопроса.' if active else 'Ассистент отключён: настройте ASSISTANT_ENABLED, OPENAI_API_KEY и OPENAI_MODEL.'}
    app.router.routes.insert(0, APIRoute('/api/v1/health', health, methods=['GET']))
    app.openapi_schema = None
    return app
