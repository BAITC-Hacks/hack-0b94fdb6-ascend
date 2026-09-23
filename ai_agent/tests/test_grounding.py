from ai_agent.service import numbers


def test_equivalent_number_formatting_is_allowed():
    assert numbers('1 817 300,00 и 0.3000') == numbers('1817300.0 и 0.3')
    assert numbers('1.2e-05') == numbers('0.000012')
    assert not numbers('1 800 000') <= numbers('1817300.0')


def test_identifiers_do_not_pass_through_float():
    assert numbers('#900000000000000001') != numbers('#900000000000000002')


def test_percentile_notation_matches_explanation():
    assert numbers('betweenness >= p99') == numbers('99-й процентиль')


def test_rounded_draft_is_repaired_before_return():
    import asyncio
    from types import SimpleNamespace as NS
    from ai_agent.service import Assistant
    class Client:
        def __init__(self): self.responses = self; self.requests = []
        async def create(self, **kwargs):
            self.requests.append(kwargs)
            if len(self.requests) == 1:
                return NS(output=[NS(type='function_call', name='get_node', arguments='{"gid":"101"}', call_id='a')], output_text='')
            text = 'У #101 оценка 0.88.' if len(self.requests) == 2 else 'У #101 оценка 0.8776.'
            return NS(output=[{'role': 'assistant', 'content': text}], output_text=text)
    # Use an SDK-like message object for output, retaining it in the repair conversation.
    class MessageClient(Client):
        async def create(self, **kwargs):
            r = await super().create(**kwargs)
            if r.output_text: r.output = [NS(type='message', role='assistant', content=r.output_text)]
            return r
    snapshot = {'nodes':[{'gid':'101','role':'coordinator','role_score':0.8776,'cluster_id':0}], 'edges':[], 'clusters':[]}
    client = MessageClient()
    result = asyncio.run(Assistant(snapshot, client=client, enabled=True, model='test').ask('Объясни узел'))
    assert result['answer'] == 'У #101 оценка 0.8776.'
    assert len(client.requests) == 3
    assert client.requests[-1]['tool_choice'] == 'none'
    assert any(isinstance(m, dict) and m.get('role') == 'developer' for m in client.requests[-1]['input'])
