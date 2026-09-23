import random
import networkx as nx
import pandas as pd
from .base import ExtraResult

def run(ctx):
    g=ctx.graph;cfg=ctx.cfg['resilience'];seeds=sorted(ctx.nodes.loc[ctx.nodes.is_seed,'gid']);baseline=sum(len(nx.descendants(g,s)) for s in seeds);turnover=sum(d['sum_kzt'] for _,_,d in g.edges(data=True))
    priority=list(ctx.nodes.sort_values(['priority_score','gid'],ascending=[False,True]).gid)
    degree=sorted(g,key=lambda v:(-g.degree(v),v));ids=sorted(g);rows=[];removed=[]
    def measure(drop):
        h=g.copy();h.remove_nodes_from(drop); comps=list(nx.weakly_connected_components(h)); nonisolated=[v for v in comps if len(v)>1]
        largest=max(comps,key=lambda v:(len(v),-min(v)),default=set());flow=sum(d['sum_kzt'] for a,b,d in h.edges(data=True) if a in largest and b in largest)
        return dict(n_components=len(nonisolated),largest_component=len(largest),largest_share=len(largest)/len(h) if len(h) else 0,seed_pairs_retained=sum(len(nx.descendants(h,s)) for s in seeds if s in h)/baseline if baseline else 0,flow_retained=flow/turnover if turnover else 0)
    for n in cfg['remove_counts']:
        for strategy,order in [('priority',priority),('degree',degree),('random',ids)]:
            count=min(n,len(ids));runs=[]
            for i in range(cfg['random_repeats'] if strategy=='random' else 1):
                drop=random.Random(ctx.config['random_seed']+i).sample(ids,count) if strategy=='random' else order[:count]
                runs.append(measure(drop))
                if strategy!='random':removed.append(dict(strategy=strategy,n_removed=count,gids=';'.join(map(str,drop))))
            rows.append(dict(strategy=strategy,n_removed=count,**{k:sum(r[k] for r in runs)/len(runs) for k in runs[0]}))
    return ExtraResult({'resilience':pd.DataFrame(rows),'resilience_removed':pd.DataFrame(removed)},dict(baseline_seed_pairs=baseline,random_repeats=cfg['random_repeats']))
