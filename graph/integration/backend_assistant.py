"""Copy/import this adapter from backend/assistant; register on the team's FastAPI app.

get_snapshot must return the already-published snapshot dict. Reload is owned by backend.
Optional dependencies: fastapi, pydantic, openai (not imported by Graph Engine).
"""


def register_assistant(app, get_snapshot):
    from fastapi.responses import JSONResponse
    from fastapi import Request
    from graph.assistant import Assistant, AssistantError

    @app.post('/api/v1/assistant')
    async def assistant_endpoint(request: Request):
        try:
            body = await request.json()
            if not isinstance(body, dict) or set(body) - {'question', 'history'} or 'question' not in body:
                raise ValueError('Неверное тело запроса')
        except (ValueError, TypeError):
            return JSONResponse(status_code=400, content={'error': {'code': 'invalid_param', 'message': 'Ожидаются question и необязательная history', 'details': {}}})
        snap = get_snapshot()
        if snap is None:
            return JSONResponse(status_code=503, content={'error': {'code': 'no_result', 'message': 'Нет успешного результата анализа', 'details': {}}})
        agent = Assistant(snap)
        try:
            return await agent.ask(body['question'], body.get('history'))
        except AssistantError as exc:
            return JSONResponse(status_code=exc.status, content=exc.response())
        finally:
            if agent.client is not None:
                await agent.client.close()

    return assistant_endpoint
