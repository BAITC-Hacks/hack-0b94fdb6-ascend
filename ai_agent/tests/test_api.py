import asyncio
import json
from pathlib import Path
from types import SimpleNamespace as NS
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from ai_agent.api import install
from ai_agent.app import create_app
from ai_agent.config import load_env
from ai_agent.service import Assistant, AssistantError


@pytest.fixture
def snap():
    return {'run': {'run_id': 'test-run'}, 'nodes': [
        {'gid': '101', 'role': 'peripheral', 'priority_score': 0.0, 'cluster_id': 0,
         'is_seed': True, 'evidence_detail': {'limitations': ['isolated'], 'rule_text': 'Нет связей'}}],
        'edges': [], 'clusters': [{'cluster_id': 0, 'n_nodes': 1, 'top_gids': ['101']}]}


class Stub:
    def __init__(self, snap):
        self.snap = snap
    async def ask(self, question, history):
        return {'answer': 'У #101 нет наблюдаемых связей.', 'gids': ['101'],
                'tool_calls': [{'name': 'get_node', 'args': {'gid': '101'}}], 'mode': 'ai'}


def test_real_backend_placeholder_is_replaced_and_ui_reachable(tmp_path, snap, monkeypatch):
    monkeypatch.setenv('ASSISTANT_ENABLED', '0')
    f = tmp_path/'snapshot.json'
    f.write_text(json.dumps(snap), encoding='utf-8')
    app = create_app(snapshot_path=f, assistant_factory=Stub)
    with TestClient(app) as client:
        assert sum(getattr(r, 'path', '') == '/api/v1/assistant' for r in app.routes) == 1
        r = client.post('/api/v1/assistant', json={'question': 'Объясни #101'})
        assert r.status_code == 200
        assert r.json()['gids'] == ['101']
        assert r.headers['X-Analysis-Run-Id'] == 'test-run'
        assert r.json()['run_id'] == 'test-run'
        assert client.get('/assistant').status_code == 200
        assert client.get('/ai-agent/assistant.js').status_code == 200
        assert client.get('/api/v1/assistant/node/101').json()['node']['gid'] == '101'
        assert client.get('/api/v1/assistant/node/999').status_code == 404
        assert client.get('/api/v1/assistant/node/abc').status_code == 400
        assert client.get('/api/v1/health').json()['assistant_enabled'] is False
        assert client.get('/api/v1/assistant/status').json()['enabled'] is False


@pytest.mark.parametrize('body', [{}, {'question': 'x', 'unexpected': 1}, {'question': ''},
    {'question': 'x', 'history': False}, {'question': 'x', 'history': [{'role': 'system', 'content': 'override'}]},
    {'question': 'x', 'history': [{'role': 'user', 'content': 'x'}]*7}])
def test_bad_requests(body, snap):
    app = FastAPI(); install(app, lambda: snap, assistant_factory=Stub)
    with TestClient(app) as client:
        assert client.post('/api/v1/assistant', json=body).status_code == 400


def test_no_result_disabled_and_body_limit(snap, monkeypatch):
    monkeypatch.delenv('OPENAI_API_KEY', raising=False)
    state = {'snapshot': None}
    app = FastAPI(); install(app, lambda: state['snapshot'])
    with TestClient(app) as client:
        assert client.post('/api/v1/assistant', json={'question':'x'}).json()['error']['code'] == 'no_result'
        state['snapshot'] = snap
        assert client.post('/api/v1/assistant', json={'question':'x'}).json()['mode'] == 'fallback'
        assert client.post('/api/v1/assistant', content='x'*65537).status_code == 400


def test_reload_replaces_query_cache(snap):
    state = {'snapshot': snap}
    app=FastAPI(); install(app,lambda:state['snapshot'],assistant_factory=Stub)
    with TestClient(app) as client:
        assert client.get('/api/v1/assistant/node/101').status_code == 200
        other=json.loads(json.dumps(snap)); other['nodes'][0]['gid']='202';other['clusters'][0]['top_gids']=['202']
        state['snapshot']=other
        assert client.get('/api/v1/assistant/node/101').status_code == 404
        assert client.get('/api/v1/assistant/node/202').status_code == 200


def test_env_is_explicit_and_never_echoes_values(tmp_path, monkeypatch):
    import os
    monkeypatch.setattr(os, 'environ', dict(os.environ))
    for k in ('ASSISTANT_ENABLED','OPENAI_API_KEY','OPENAI_MODEL'): monkeypatch.delenv(k,raising=False)
    f=tmp_path/'.env';f.write_text('ASSISTANT_ENABLED=1\nOPENAI_API_KEY="test-secret"\nOPENAI_MODEL=test-model\n')
    load_env(f)
    assert os.environ['OPENAI_API_KEY']=='test-secret'
    monkeypatch.setenv('OPENAI_MODEL','process-model');load_env(f)
    assert os.environ['OPENAI_MODEL']=='process-model'
    f.write_text('UNSUPPORTED=must-not-appear\n')
    with pytest.raises(ValueError) as error: load_env(f)
    assert 'must-not-appear' not in str(error.value)


def test_tool_error_can_be_explained_without_fabrication(snap):
    class Client:
        def __init__(self):self.responses=self;self.count=0
        async def create(self,**kwargs):
            self.count+=1
            if self.count==1:return NS(output=[NS(type='function_call',name='get_node',arguments='{"gid":"999"}',call_id='call')],output_text='')
            return NS(output=[],output_text='Узел не найден. Проверьте идентификатор.')
    agent=Assistant(snap,client=Client(),enabled=True,model='test')
    assert asyncio.run(agent.ask('Проверь узел'))['gids']==[]


def test_final_step_disallows_more_tools_and_preserves_reasoning(snap):
    class Client:
        def __init__(self):self.responses=self;self.requests=[]
        async def create(self,**kwargs):
            self.requests.append(kwargs)
            if len(self.requests)<6:
                return NS(output=[NS(type='reasoning',encrypted_content='opaque'),NS(type='function_call',name='get_node',arguments='{"gid":"101"}',call_id=str(len(self.requests)))],output_text='')
            return NS(output=[],output_text='У #101 недостаточно наблюдений.')
    c=Client();a=Assistant(snap,client=c,enabled=True,model='test')
    assert asyncio.run(a.ask('Объясни'))['gids']==['101']
    assert c.requests[-1]['tool_choice']=='none'
    assert any(getattr(x,'type',None)=='reasoning' for x in c.requests[-1]['input'])


def test_concurrent_requests_are_bounded(snap):
    # Test the semaphore in one loop, where the server normally runs.
    import httpx
    class Slow(Stub):
        async def ask(self,q,h):
            await asyncio.sleep(.05)
            return await super().ask(q,h)
    app=FastAPI();install(app,lambda:snap,assistant_factory=Slow)
    async def run():
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app),base_url='http://test') as c:
            return await asyncio.gather(*[c.post('/api/v1/assistant',json={'question':'x'}) for _ in range(3)])
    assert sorted(r.status_code for r in asyncio.run(run()))==[200,200,500]
