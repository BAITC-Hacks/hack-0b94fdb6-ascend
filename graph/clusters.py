import networkx as nx
import pandas as pd
from .models import ROLES


def partition(g, frame, config):
    ug = nx.Graph()
    ug.add_nodes_from(g)
    for a, b, data in g.edges(data=True):
        ug.add_edge(a, b, w=ug.get_edge_data(a, b, {}).get('w', 0.0) + data['sum_kzt'])
    components = sorted(nx.weakly_connected_components(g), key=lambda s: (-len(s), min(s)))
    # Louvain's modularity is undefined on a graph with no edges.
    groups = nx.community.louvain_communities(ug, weight='w', resolution=config['louvain_resolution'], seed=config['random_seed']) if ug.number_of_edges() else [{v} for v in ug]
    groups = sorted(groups, key=lambda s: (-len(s), min(s)))
    for col, parts in [('cluster_id', groups), ('component_id', components)]:
        mapping = {v: i for i, part in enumerate(parts) for v in part}
        frame[col] = frame.gid.map(mapping).astype('int64')
    membership = frame.set_index('gid').cluster_id.to_dict()
    frame['n_nbr_clusters'] = [len({membership[u] for u in set(g.predecessors(v)) | set(g.successors(v))} - {membership[v]}) for v in frame.gid]
    return ug, components


def summarize(frame, edges, config):
    rows = []
    mapping = frame.set_index('gid').cluster_id
    internal = edges[edges.src.map(mapping) == edges.dst.map(mapping)].copy()
    internal['cluster_id'] = internal.src.map(mapping)
    totals = internal.groupby('cluster_id').sum_kzt.sum().to_dict()
    sizes = frame.groupby('component_id').size().to_dict()
    for cid, part in frame.groupby('cluster_id', sort=True):
        ordered = part.sort_values(['priority_score', 'gid'], ascending=[False, True])
        lead = ordered.iloc[0]
        n_seed = int(part.is_seed.sum())
        hubs = ordered[ordered.role.isin(['coordinator', 'consolidator'])]
        dist = ordered[ordered.role == 'distributor']
        counts = {role: int((part.role == role).sum()) for role in ROLES}
        if len(part) == 1 and bool(lead.is_isolated):
            rule, text = 'H_ISOLATED', 'Изолированный узел: переводов в выгрузке нет, данных для гипотезы недостаточно'
        elif n_seed >= config['cluster_collect_seeds'] and len(hubs):
            rule, text = 'H_COLLECT', f'Признаки сбора средств от {n_seed} seed с концентрацией у {int(hubs.iloc[0].gid)}'
        elif len(dist) and float(dist.out_kzt.sum()) > float(part.out_kzt.sum()) * config['cluster_fanout_share']:
            rule, text = 'H_FANOUT', f'Признаки веерного распределения от {int(dist.iloc[0].gid)} на {int(dist.iloc[0].out_deg)} получателей'
        elif counts['transit'] / len(part) >= config['cluster_transit_share']:
            rule, text = 'H_TRANSIT', 'Признаки транзитной цепочки: средства проходят без удержания'
        elif int(lead.component_id) != 0 and sizes[int(lead.component_id)] <= config['layout_small_component']:
            rule, text = 'H_SMALL', f'Изолированный фрагмент из {sizes[int(lead.component_id)]} узлов, связь с основной сетью не наблюдается'
        elif not n_seed:
            rule, text = 'H_NOSEED', f'Фрагмент без seed на {int(part.depth.min())}-м колене; назначение не определено'
        else:
            rule, text = 'H_MIXED', 'Смешанная структура: ' + ', '.join(f'{k}={v}' for k, v in counts.items() if v) + '; требуется ручной разбор'
        rows.append(dict(cluster_id=int(cid), n_nodes=len(part), n_seed=n_seed,
                         sum_kzt_internal=round(float(totals.get(cid, 0)), 2),
                         top_gids=[str(v) for v in ordered.gid.head(5)], hypothesis=text,
                         hypothesis_rule=rule, role_counts=counts, component_ids=sorted(int(x) for x in part.component_id.unique())))
    return pd.DataFrame(rows)
