from datetime import date
import pandas as pd
import pytest
from graph import load_config,DEFAULT_CONFIG
from graph.features import build_features
from graph.extras.base import Context
from graph.extras import boundary,temporal,routes,anomalies,resilience,gaps,run_all


def context(transfers,depths=None,seeds=None):
    ids=sorted(set(v for a,b,_,_ in transfers for v in (a,b)))
    tx=pd.DataFrame([dict(src=a,dst=b,sum_kzt=v,date=date(2026,7,d)) for a,b,v,d in transfers])
    edges=tx.groupby(['src','dst']).agg(sum_kzt=('sum_kzt','sum'),n_tx=('sum_kzt','size')).reset_index()
    n=pd.DataFrame([dict(gid=g,depth=(depths or {}).get(g,1),is_seed=g in (seeds or [])) for g in ids])
    c=load_config(DEFAULT_CONFIG);g,n=build_features(n,edges,c)
    n['role']='peripheral';n['priority_score']=[1 if v==2 else .1 for v in ids];n['priority_rank']=n.priority_score.rank(method='first',ascending=False).astype(int)
    return Context(g,n,tx,c)


def test_fifo_does_not_double_spend_or_match_expired_inflow():
    ctx=context([(1,2,100000,1),(2,3,95000,2),(2,4,95000,2)])
    f=temporal.run(ctx).features[2]
    assert f['fast_pass_share']==1 and f['fast_matched_kzt']==100000
    assert f['median_hold_days']==1
    ctx=context([(1,2,100000,1),(2,3,95000,2)])
    assert temporal.run(ctx).features[2]['fast_pass_share']==.95
    ctx=context([(1,2,100000,1),(2,3,95000,6)])
    assert temporal.run(ctx).features[2]['fast_pass_share']==0


def test_sync_and_boundary_late_correction():
    ctx=context([(1,4,10000,1),(2,4,10000,1),(3,4,10000,1)])
    r=temporal.run(ctx)
    assert r.features[4]['sync_in_days']==1
    transfers=[(100+i,i,10000,1) for i in range(1,12)]+[(100,999,10000,31)]
    ctx=context(transfers,depths={999:4});r=boundary.run(ctx)
    assert r.features[999]['p_onward']==0
    assert r.features[999]['boundary_status']=='unknown' and r.features[999]['late_inflow']


def test_cycles_chains_and_rotation_of_time_start():
    ctx=context([(1,2,10000,1),(1,2,10000,3),(2,3,10000,2),(2,3,10000,4),(3,1,10000,1)])
    r=routes.run(ctx)
    chain=r.tables['chains'].query('a==1 and b==2 and c==3').iloc[0]
    assert chain.repeats==2 and chain.median_lag_days==1
    cycle=r.tables['cycles'].iloc[0]
    assert cycle.time_consistent # Valid chronological start is 3, not minimum gid 1.
    assert cycle.path=='1→2→3→1'


def test_splitting_uses_full_day_windows_not_cherry_picked_transfers():
    ctx=context([(1,2,50000,1),(1,2,50000,2),(1,2,50000,3)])
    assert anomalies.run(ctx).summary['split_pairs']==1
    ctx=context([(1,2,10000,1),(1,2,50000,2),(1,2,200000,3)])
    assert anomalies.run(ctx).summary['split_pairs']==0
    # Same-day outlier must not be dropped to manufacture a low CV.
    ctx=context([(1,2,50000,1)]*3+[(1,2,500000,1)])
    assert anomalies.run(ctx).summary['split_pairs']==0


def test_resilience_and_silent_seed_requests():
    ctx=context([(1,2,10000,1),(2,3,10000,2),(2,4,10000,2)],seeds=[1,4])
    ctx.config['extras']['resilience']['remove_counts']=[0,1]
    ctx.config['extras']['resilience']['random_repeats']=2
    r=resilience.run(ctx)
    assert r.tables['resilience'].query("strategy=='priority' and n_removed==1").iloc[0].seed_pairs_retained==0
    ctx.results['boundary']=boundary.run(ctx);ctx.results['anomalies']=anomalies.run(ctx)
    requests=gaps.run(ctx).tables['gaps']
    assert '4' in requests[requests.gap_type=='G_SEED_SILENT'].iloc[0].gids


def test_extra_failure_isolated_and_core_frame_unchanged(monkeypatch):
    ctx=context([(1,2,10000,1)]);before=ctx.nodes.copy(deep=True)
    monkeypatch.setattr(boundary,'run',lambda ctx:(_ for _ in ()).throw(ValueError('injected')))
    results,summary,warnings=run_all(ctx.graph,ctx.nodes,ctx.transactions,ctx.config)
    assert summary['boundary']['available'] is False
    assert summary['temporal']['available'] is True and warnings
    pd.testing.assert_frame_equal(ctx.nodes,before)


def test_optional_counterparty_gid_never_roundtrips_through_float():
    from graph.extras.export import payload
    g=900000000000000001
    ctx=context([(g,g+1,50000,1),(g,g+1,50000,2),(g,g+1,50000,3)])
    r=anomalies.run(ctx)
    rows=payload({'anomalies':r})['tables']['anomalies']
    split=next(x for x in rows if x['anomaly_type']=='split_pair')
    assert split['gid']==str(g) and split['counterparty_gid']==str(g+1)
