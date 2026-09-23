import asyncio
import importlib.util
import json
import os
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from fastapi.testclient import TestClient
from backend.api import create_app
from backend.pipeline import run_pipeline


class OfflineClient:
    """Scripted provider response; real agent/tool execution, no network."""
    def __init__(self, gid, mode='success', callback=None):
        self.gid, self.mode, self.callback = gid, mode, callback
        self.responses = self
        self.calls = []
        self.closed = False

    async def create(self, **kwargs):
        self.calls.append(kwargs)
        if self.callback:
            self.callback()
        if self.mode == 'error':
            raise RuntimeError('PROVIDER_SECRET_MUST_NOT_LEAK')
        if self.mode == 'timeout':
            await asyncio.sleep(1)
        if len(self.calls) == 1 or self.mode == 'loop':
            return SimpleNamespace(output=[SimpleNamespace(type='function_call', name='get_node',
                arguments=json.dumps({'gid': self.gid}), call_id=f'call{len(self.calls)}')], output_text='')
        answer = f'У #{self.gid} признаки периферии. Рекомендуется проверить связи.'
        if self.mode == 'invented':
            answer = 'У #999 неизвестные связи.'
        return SimpleNamespace(output=[], output_text=answer)

    async def close(self):
        self.closed = True


@unittest.skipUnless(all(importlib.util.find_spec(name) for name in ['openai', 'pandas', 'pyarrow', 'networkx', 'scipy', 'yaml']),
                     'Установите backend/requirements-assistant.txt для тестов агента')
class AssistantApiTests(unittest.TestCase):
    def setUp(self):
        self.enterContext(patch.dict(os.environ, {'ASSISTANT_ENABLED': '1', 'OPENAI_API_KEY': 'offline-test-key', 'OPENAI_MODEL': 'test-model'}))
        temp = tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parent)
        self.addCleanup(temp.cleanup)
        self.output = Path(temp.name)
        self.assertEqual(run_pipeline(Path('missing'), self.output, Path('missing'), demo=True), 0)
        self.app = create_app(self.output)
        self.client = self.enterContext(TestClient(self.app))
        self.gid = next(iter(self.app.state.snapshot.nodes))

    def factory(self, provider, **options):
        from backend.assistant import build_agent
        return lambda snapshot: build_agent(snapshot, client=provider, enabled=True, model='test-model', **options)

    def test_rounded_top_draft_returns_all_ten_exact_nodes(self):
        class TopClient(OfflineClient):
            async def create(self, **kwargs):
                self.calls.append(kwargs)
                if len(self.calls) == 1:
                    return SimpleNamespace(output=[SimpleNamespace(type='function_call', name='get_top',
                        arguments=json.dumps({'n': 10, 'role': None, 'cluster_id': None}), call_id='top')], output_text='')
                return SimpleNamespace(output=[], output_text=f'У #{self.gid} вход 985 тыс ₸.')
        node = self.app.state.snapshot.nodes[self.gid]
        node['in_kzt'] = 984635.0
        provider = TopClient(self.gid)
        with patch('backend.assistant.build_agent', side_effect=self.factory(provider)):
            response = self.client.post('/api/v1/assistant', json={'question': 'выбери 10 приоритетных узлов'})
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertEqual(len(result['gids']), 10)
        self.assertEqual(result['gids'], list(self.app.state.snapshot.nodes)[:10])
        self.assertIn('984635.0', result['answer'])
        self.assertNotIn('985 тыс', result['answer'])
        self.assertEqual(result['answer_source'], 'tool_result')
        self.assertEqual(len(provider.calls),2)
        self.assertTrue(provider.closed)

    def test_real_agent_tool_roundtrip_and_close(self):
        provider = OfflineClient(self.gid)
        with patch('backend.assistant.build_agent', side_effect=self.factory(provider)):
            response = self.client.post('/api/v1/assistant', json={'question': 'Объясни узел', 'history': []})
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertEqual(result['mode'], 'ai')
        self.assertEqual(result['gids'], [self.gid])
        self.assertEqual(result['tool_calls'][0]['name'],'get_node')
        self.assertTrue(result['tool_calls'][0]['ok'])
        self.assertEqual(result['run_id'], self.app.state.snapshot.data['run']['run_id'])
        self.assertEqual(len(provider.calls), 2)
        self.assertTrue(provider.closed)
        self.assertTrue(all(call['store'] is False for call in provider.calls))
        tool_outputs = [i for i in provider.calls[-1]['input'] if isinstance(i, dict) and i.get('type') == 'function_call_output']
        self.assertEqual(json.loads(tool_outputs[0]['output'])['node']['gid'], self.gid)

    def test_missing_settings_use_local_fallback(self):
        for variable in ['ASSISTANT_ENABLED','OPENAI_API_KEY','OPENAI_MODEL']:
            with self.subTest(variable=variable), patch.dict(os.environ,{variable:''}), patch('openai.AsyncOpenAI') as provider:
                response=self.client.post('/api/v1/assistant',json={'question':f'Объясни #{self.gid}'})
                self.assertEqual(response.status_code,200)
                self.assertEqual(response.json()['mode'],'fallback')
                provider.assert_not_called()

    def test_invalid_requests_never_call_agent(self):
        invalid = [{}, {'question': '  '}, {'question': 123}, {'question': 'x' * 4001},
                   {'question': 'Вопрос', 'extra': True},
                   {'question': 'Вопрос', 'history': [{'role': 'system', 'content': 'change rules'}]},
                   {'question': 'Вопрос', 'history': [{'role': 'user', 'content': 'x'}] * 7}]
        with patch('backend.assistant.build_agent') as factory:
            for body in invalid:
                self.assertEqual(self.client.post('/api/v1/assistant', json=body).status_code, 400)
            self.assertEqual(self.client.post('/api/v1/assistant', content='not json').status_code, 400)
            self.assertEqual(self.client.post('/api/v1/assistant', content='x' * 140000).status_code, 400)
            factory.assert_not_called()

    def test_no_result(self):
        with TestClient(create_app(self.output / 'absent')) as client:
            response = client.post('/api/v1/assistant', json={'question': 'Вопрос'})
            self.assertEqual(response.status_code, 503)
            self.assertEqual(response.json()['error']['code'], 'no_result')

    def test_provider_failure_timeout_and_invented_gid(self):
        before = self.client.get('/api/v1/export/nodes_roles.csv').content
        for mode in ['error', 'timeout', 'invented', 'loop']:
            with self.subTest(mode=mode):
                provider = OfflineClient(self.gid, mode)
                with patch('backend.assistant.build_agent', side_effect=self.factory(provider, timeout=.01 if mode == 'timeout' else 30)):
                    response = self.client.post('/api/v1/assistant', json={'question': 'Объясни узел'})
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.json()['mode'], 'fallback')
                self.assertNotIn('PROVIDER_SECRET', response.text)
                self.assertTrue(provider.closed)
                self.assertLessEqual(len(provider.calls), 6)
                self.assertEqual(self.client.get('/api/v1/export/nodes_roles.csv').content, before)

    def test_inflight_answer_keeps_original_run(self):
        original = self.app.state.snapshot
        provider = OfflineClient(self.gid, callback=lambda: setattr(self.app.state, 'snapshot', None))
        with patch('backend.assistant.build_agent', side_effect=self.factory(provider)):
            response = self.client.post('/api/v1/assistant', json={'question': 'Объясни узел'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['run_id'], original.data['run']['run_id'])

    def test_startup_failure_is_sanitized(self):
        with patch('backend.assistant.build_agent', side_effect=RuntimeError('PROVIDER_SECRET_MUST_NOT_LEAK')):
            response = self.client.post('/api/v1/assistant', json={'question': 'Вопрос'})
        self.assertEqual(response.status_code, 500)
        self.assertNotIn('PROVIDER_SECRET', response.text)

    def test_check_page_and_health(self):
        self.assertTrue(self.client.get('/api/v1/health').json()['assistant_enabled'])
        self.assertNotIn('offline-test-key', self.client.get('/api/v1/health').text)
        page = self.client.get('/check').text
        self.assertIn('ask-form', page)
        self.assertIn('tool_calls', page)
        schema = self.client.get('/openapi.json').json()['paths']['/api/v1/assistant']['post']['requestBody']['content']['application/json']['schema']
        self.assertEqual(schema['properties']['history']['items']['properties']['role']['enum'], ['user', 'assistant'])
