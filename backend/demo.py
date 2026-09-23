"""Explicit synthetic fixture; never used as a fallback for real analysis."""
from types import SimpleNamespace


def analyze(data_dir, config_path):
    nodes, clusters, top = [], [], []
    for i in range(24):
        identifier = 900000000000000000 + i
        score = round(1 - i / 24, 6)
        node = dict(gid=identifier, depth=0, is_seed=True, is_boundary=False,
                    is_isolated=True, external_inflow=False, role='peripheral',
                    base_role='peripheral', role_score=0.3, priority_score=score,
                    priority_rank=i + 1, cluster_id=i, component_id=i,
                    pass_through=None, temporal=None, evidence='Синтетический пример: изолированный узел',
                    x=float(i * 10), y=0.0)
        node.update({k: 0 for k in ['in_deg', 'out_deg', 'in_tx', 'out_tx', 'seed_in', 'seed_reach', 'n_nbr_clusters', 'up_hubs', 'down_hubs']})
        node.update({k: 0.0 for k in ['in_kzt', 'out_kzt', 'betweenness', 'pagerank']})
        node.update(rule_id='R_PERIPH', rule_text='Синтетический пример', thresholds={}, values={}, strength=0.0,
                    alternatives=[], limitations=['isolated'], priority_contributions={k: 0.0 for k in ['in_kzt', 'betweenness', 'n_nbr_clusters', 'seed_reach', 'role', 'seed_factor']}, why='Синтетический пример')
        nodes.append(node)
        clusters.append(dict(cluster_id=i, n_nodes=1, n_seed=1, sum_kzt_internal=0.0,
                             top_gids=[identifier], hypothesis='Синтетический изолят', hypothesis_rule='demo',
                             role_counts={'peripheral': 1}, component_ids=[i]))
        top.append(dict(rank=i + 1, gid=identifier, role='peripheral', priority_score=score, why='Синтетический пример'))
    return SimpleNamespace(nodes=nodes, edges=[], clusters=clusters, top=top,
        run_meta=dict(_synthetic=True, methodology_version='demo-not-analysis', contract_version='2.0',
            counts=dict(nodes=24, edges=0, transactions=0, seeds=24, clusters=24, components=24, isolated=24, boundary=0),
            role_counts={'peripheral': 24}, turnover_kzt=0.0, period={'from': '2026-07-01', 'to': '2026-07-31'},
            config={}, warnings=['СИНТЕТИЧЕСКИЕ ДАННЫЕ. Не результат анализа.']),
        quality={'_synthetic': True, 'warnings': ['Демонстрационный режим']})
