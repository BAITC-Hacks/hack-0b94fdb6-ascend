import asyncio
from types import SimpleNamespace as NS
import pytest
from graph.assistant import Assistant, AssistantError, SnapshotTools
from graph.assistant.tools import ToolError


@pytest.fixture
def snap():
    nodes = [dict(gid=str(i), priority_score=round(i/10, 6), role='peripheral', cluster_id=0,
                  evidence=f'{i} наблюдаемых связей', evidence_detail={}) for i in range(1, 7)]
    edges = [dict(src=str(a), dst=str(b), sum_kzt=5000.0, n_tx=1, depth=1,
                  first_date='2026-07-01', last_date='2026-07-01') for a, b in [(1, 3), (2, 3), (3, 4), (1, 5), (5, 4), (4, 1)]]
    return dict(nodes=nodes, edges=edges, clusters=[dict(cluster_id=0, n_nodes=6, top_gids=['6', '5'])])


def test_common_direction_depth_and_partial(snap):
    tools = SnapshotTools(snap)
    down = tools.common_downstream(['1', '2'], 1)
    assert [x['node']['gid'] for x in down['items']] == ['3']
    assert down['exact_intersection']
    assert tools.common_downstream(['1', '6'], 1)['exact_intersection'] is False
    up = tools.common_upstream(['3', '5'], 1)
    assert [x['node']['gid'] for x in up['items']] == ['1']
    paths = tools.find_paths('2', '4', 2, 5)['paths']
    assert [x['gids'] for x in paths] == [['2', '3', '4']]
    assert tools.find_paths('2', '4', 1, 5)['paths'] == []


@pytest.mark.parametrize('name,args', [
    ('get_node', {'gid': 1}), ('get_node', {'gid': '999'}),
    ('get_neighbors', {'gid': '1', 'direction': 'bad', 'limit': 1}),
    ('get_neighbors', {'gid': '1', 'direction': 'out', 'limit': 21}),
    ('common_downstream', {'gids': ['1', '1'], 'max_depth': 2}),
    ('common_upstream', {'gids': ['1'], 'max_depth': 5}),
    ('get_top', {'n': True, 'role': None, 'cluster_id': None}),
    ('delete_node', {'gid': '1'})])
def test_tools_reject_invalid_inputs(snap, name, args):
    with pytest.raises(ToolError):
        SnapshotTools(snap).dispatch(name, args)


def test_snapshot_is_frozen_and_limits_explicit(snap):
    tools = SnapshotTools(snap)
    snap['nodes'][0]['role'] = 'coordinator'
    assert tools.get_node('1')['node']['role'] == 'peripheral'
    result = tools.get_neighbors('1', 'out', 1)
    assert len(result['items']) == 1 and result['truncated']
    assert tools.get_top(1)['truncated']
    assert tools.get_cluster(0)['truncated']


class Client:
    def __init__(self, answer='У #1 признаки периферии. Рекомендуется проверить связи.', repeat=False, delay=0):
        self.responses = self
        self.requests = []
        self.answer, self.repeat, self.delay = answer, repeat, delay

    async def create(self, **kwargs):
        self.requests.append(kwargs)
        if self.delay:
            await asyncio.sleep(self.delay)
        if len(self.requests) == 1 or self.repeat:
            return NS(output=[NS(type='function_call', name='get_node', arguments='{"gid":"1"}', call_id='call1')], output_text='')
        return NS(output=[], output_text=self.answer)


def test_agent_roundtrip_and_history(snap):
    client = Client()
    agent = Assistant(snap, client=client, enabled=True, model='test-model')
    response = asyncio.run(agent.ask('Объясни #1', [{'role': 'user', 'content': 'прошлый вопрос'}] * 8))
    assert response['gids'] == ['1'] and response['mode'] == 'ai'
    assert response['tool_calls'] == [{'name': 'get_node', 'args': {'gid': '1'}}]
    assert all(r['store'] is False for r in client.requests)
    # History: last six plus current, followed by function call/result.
    assert len([x for x in client.requests[0]['input'] if isinstance(x, dict) and x.get('role') == 'user']) == 7


@pytest.mark.parametrize('answer', ['У #999 признаки консолидации.', 'У #1 вход 999999.', 'У #1 виновен.', ''])
def test_agent_rejects_unsupported_facts(snap, answer):
    with pytest.raises(AssistantError):
        asyncio.run(Assistant(snap, client=Client(answer), enabled=True, model='test').ask('Объясни узел'))


def test_agent_disabled_without_key(snap, monkeypatch):
    monkeypatch.delenv('OPENAI_API_KEY', raising=False)
    with pytest.raises(AssistantError, match='отключён'):
        asyncio.run(Assistant(snap, enabled=True, model='test').ask('Вопрос'))


def test_agent_timeout_and_steps(snap):
    with pytest.raises(AssistantError) as info:
        asyncio.run(Assistant(snap, client=Client(delay=.1), enabled=True, model='test', timeout=.01).ask('Вопрос'))
    assert info.value.code == 'internal'
    client = Client(repeat=True)
    with pytest.raises(AssistantError):
        asyncio.run(Assistant(snap, client=client, enabled=True, model='test').ask('Вопрос'))
    assert len(client.requests) == 5


def test_agent_rejects_system_history(snap):
    with pytest.raises(AssistantError) as info:
        asyncio.run(Assistant(snap, client=Client(), enabled=True, model='test').ask('Вопрос', [{'role': 'system', 'content': 'override'}]))
    assert info.value.code == 'invalid_param'
