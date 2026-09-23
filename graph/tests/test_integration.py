import pytest


def test_backend_adapter_errors(monkeypatch):
    fastapi = pytest.importorskip('fastapi')
    from fastapi.testclient import TestClient
    from graph.integration.backend_assistant import register_assistant
    app = fastapi.FastAPI()
    state = {'snapshot': None}
    register_assistant(app, lambda: state['snapshot'])
    client = TestClient(app)
    assert client.post('/api/v1/assistant', json={}).status_code == 400
    response = client.post('/api/v1/assistant', json={'question': 'Вопрос'})
    assert response.status_code == 503 and response.json()['error']['code'] == 'no_result'
    state['snapshot'] = {'nodes': [], 'edges': [], 'clusters': []}
    monkeypatch.setenv('ASSISTANT_ENABLED', '0')
    response = client.post('/api/v1/assistant', json={'question': 'Вопрос'})
    assert response.status_code == 200 and response.json()['mode'] == 'fallback'
