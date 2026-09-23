from bisect import bisect_left
import networkx as nx
import pandas as pd
from .base import ExtraResult

def run(ctx):
    g=ctx.graph; cfg=ctx.cfg['routes']; seeds=set(ctx.nodes.loc[ctx.nodes.is_seed,'gid'])
    dates={(int(a),int(b)):sorted(v.date) for (a,b),v in ctx.transactions.groupby(['src','dst'])}
    features={int(v):dict(n_cycles=0,n_time_consistent_cycles=0) for v in g};cycles=[]; truncated=False
    for cycle in nx.simple_cycles(g,length_bound=cfg['cycle_max_len']):
        if len(cycle)<2:continue
        if len(cycles)>=cfg['cycle_budget']: truncated=True;break
        j=cycle.index(min(cycle));cycle=cycle[j:]+cycle[:j];pairs=list(zip(cycle,cycle[1:]+cycle[:1]))
        # A chronological cycle may start at any vertex, not only the canonical minimum gid.
        consistent=False
        for start in range(len(pairs)):
            previous=None;ok=True
            for edge in pairs[start:]+pairs[:start]:
                ds=dates[edge]; k=0 if previous is None else bisect_left(ds,previous)
                if k==len(ds):ok=False;break
                previous=ds[k]
            if ok:consistent=True;break
        weights=[g.edges[e]['sum_kzt'] for e in pairs]
        cycles.append(dict(length=len(cycle),cycle_type='reciprocal' if len(cycle)==2 else 'cycle',path='→'.join(map(str,cycle+[cycle[0]])),min_edge_kzt=min(weights),total_kzt=sum(weights),has_seed=bool(set(cycle)&seeds),time_consistent=consistent))
        for v in cycle:features[v]['n_cycles']+=1;features[v]['n_time_consistent_cycles']+=int(consistent)
    cycles.sort(key=lambda r:(r['length'],tuple(map(int,r['path'].split('→')))))
    for i,r in enumerate(cycles):r['cycle_id']=f'C{i+1:05}'
    chains=[];candidates=0
    for b in sorted(g):
        for a in sorted(g.predecessors(b)):
            if g[a][b]['n_tx']<2:continue
            for c in sorted(g.successors(b)):
                if g[b][c]['n_tx']<2:continue
                candidates+=1;ins=dates[a,b];outs=dates[b,c];i=0;lags=[];ends=[]
                for out in outs:
                    while i<len(ins) and (out-ins[i]).days>cfg['chain_days']:i+=1
                    if i<len(ins) and 0<=(out-ins[i]).days<=cfg['chain_days']:
                        lags.append((out-ins[i]).days);ends.extend([ins[i],out]);i+=1
                if len(lags)>=cfg['chain_min_repeats']:
                    chains.append(dict(a=a,b=b,c=c,repeats=len(lags),sum_ab=g[a][b]['sum_kzt'],sum_bc=g[b][c]['sum_kzt'],median_lag_days=float(pd.Series(lags).median()),first_date=str(min(ends)),last_date=str(max(ends))))
    chains.sort(key=lambda r:(-r['repeats'],-min(r['sum_ab'],r['sum_bc']),r['a'],r['b'],r['c']))
    total=len(chains);chains=chains[:cfg['chain_max']]
    for i,r in enumerate(chains):r['chain_id']=f'H{i+1:05}'
    return ExtraResult({'chains':pd.DataFrame(chains,columns='chain_id a b c repeats sum_ab sum_bc median_lag_days first_date last_date'.split()),'cycles':pd.DataFrame(cycles,columns='cycle_id length cycle_type path min_edge_kzt total_kzt has_seed time_consistent'.split())},dict(n_cycles=len(cycles),length_counts={str(k):sum(r['length']==k for r in cycles) for k in range(2,7)},chain_candidates=candidates,n_chains=total,truncated=truncated or total>cfg['chain_max'],limitation='Неубывающие даты не доказывают возврат одних и тех же средств; времени суток нет.'),features)
