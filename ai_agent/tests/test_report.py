import asyncio
from types import SimpleNamespace as NS
from ai_agent.report import report
from ai_agent.service import Assistant


NODE = dict(gid='101', role='consolidator', in_kzt=610100.0, out_kzt=3374866.0,
            in_deg=11, out_deg=39, role_score=.8776, priority_score=.955098,
            cluster_id=0, evidence='Наблюдаемые входящие связи; правило R_TEST.')


def test_exact_money_and_partial_coverage_are_not_group_transfers():
    f = dict(requested_sources=5, max_depth=4, exact_intersection=False,
             limitation='Достижимость не доказывает движение средств.',
             items=[dict(node=NODE, matched_sources=2)], truncated=True)
    text, gids, common = report([f])
    assert 'для всех 5' in text and 'не найдено' in text
    assert '2 из 5' in text and 'не сумма переводов от этой группы' in text
    assert '610,100 ₸' in text and '3,374,866 ₸' in text
    assert 'Основание:' in text and 'R_TEST' in text
    assert gids == {'101'} and common


def test_bad_numeric_draft_returns_actual_financial_facts():
    class Client:
        def __init__(self): self.responses=self; self.count=0
        async def create(self, **kwargs):
            self.count+=1
            if self.count==1:
                return NS(output=[NS(type='function_call', name='get_node', arguments='{"gid":"101"}', call_id='a')], output_text='')
            return NS(output=[], output_text='У #101 вход 999999999.')
    c=Client()
    result=asyncio.run(Assistant({'nodes':[NODE], 'edges':[], 'clusters':[]},client=c,enabled=True,model='test').ask('Проанализируй'))
    assert '999999999' not in result['answer']
    assert '610,100 ₸' in result['answer'] and '3,374,866 ₸' in result['answer']
    assert result['mode']=='fallback' and result['warnings']
    assert result['gids']==['101'] and c.count==3
