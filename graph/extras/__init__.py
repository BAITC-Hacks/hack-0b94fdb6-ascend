"""Optional deterministic analyses. Failures never change P0 classifications."""
from importlib import import_module
from time import perf_counter
from .base import Context, ExtraResult

MODULES=('boundary','temporal','routes','anomalies','resilience','gaps','cards')

def run_all(graph,nodes,transactions,config,clusters=None):
    ctx=Context(graph,nodes,transactions,config);warnings=[];summary={}
    ctx.clusters=[] if clusters is None else clusters.to_dict('records')
    if not config['extras']['enabled']:return {},summary,warnings
    for name in MODULES:
        started=perf_counter()
        try:
            result=import_module(f'graph.extras.{name}').run(ctx)
            ctx.results[name]=result
            summary[name]=dict(available=True,**result.summary)
        except Exception as exc:
            warnings.append(f'extras.{name}: {type(exc).__name__}: {exc}')
            ctx.results[name]=ExtraResult();summary[name]=dict(available=False,error=type(exc).__name__)
    return ctx.results,summary,warnings
