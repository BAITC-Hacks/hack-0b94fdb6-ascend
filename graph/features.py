import networkx as nx
import pandas as pd


def build_features(nodes, edges, config):
    g = nx.DiGraph()
    g.add_nodes_from(int(x) for x in nodes.gid)
    for r in edges.itertuples(index=False):
        if r.src != r.dst:
            g.add_edge(int(r.src), int(r.dst), sum_kzt=float(r.sum_kzt), n_tx=int(r.n_tx))
    result = nodes.copy()
    for name, direction, weight in [('in_deg', g.in_degree, None), ('out_deg', g.out_degree, None),
                                     ('in_kzt', g.in_degree, 'sum_kzt'), ('out_kzt', g.out_degree, 'sum_kzt'),
                                     ('in_tx', g.in_degree, 'n_tx'), ('out_tx', g.out_degree, 'n_tx')]:
        dtype = float if name.endswith('kzt') else 'int64'
        result[name] = result.gid.map(dict(direction(weight=weight))).astype(dtype)
    result['pass_through'] = pd.Series([float(o/i) if i else None for i, o in zip(result.in_kzt, result.out_kzt)], dtype=object)
    result['is_boundary'] = result.depth == config['boundary_depth']
    result['is_isolated'] = result.in_deg + result.out_deg == 0
    result['external_inflow'] = ~result.is_seed & (result.out_kzt > result.in_kzt * config['external_inflow_ratio'])
    seeds = set(result.loc[result.is_seed, 'gid'])
    result['seed_in'] = [len(set(g.predecessors(v)) & seeds) for v in result.gid]
    reach = dict.fromkeys(g, 0)
    for seed in sorted(seeds):
        for v in nx.descendants(g, seed):
            reach[v] += 1
    result['seed_reach'] = result.gid.map(reach)
    result['betweenness'] = result.gid.map(nx.betweenness_centrality(g, normalized=True, weight=None))
    result['pagerank'] = result.gid.map(nx.pagerank(g, weight='sum_kzt', alpha=config['pagerank_alpha']))
    result['temporal'] = None
    return g, result
