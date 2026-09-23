from .base import ExtraResult

def run(ctx):
    from graph.query import SnapshotTools
    from graph.serialization import json_value
    from .export import payload
    edges=[dict(src=a,dst=b,**d) for a,b,d in ctx.graph.edges(data=True)]
    snap=json_value(dict(nodes=ctx.nodes.to_dict('records'),edges=edges,clusters=getattr(ctx,'clusters',[]),run={'config':ctx.config},extras=payload(ctx.results)))
    tools=SnapshotTools(snap)
    cards=[tools.get_node_card(str(g)) for g in ctx.nodes.sort_values('priority_rank').head(20).gid]
    return ExtraResult(summary={'n_cards':len(cards)},documents={'cards_top': '\n\n---\n\n'.join(c['text'] for c in cards)})
