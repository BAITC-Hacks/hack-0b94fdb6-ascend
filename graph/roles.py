import numpy as np

RULE_IDS = {'consolidator': 'R_CONS', 'distributor': 'R_DIST', 'transit': 'R_TRANS',
            'terminal': 'R_TERM', 'coordinator': 'R_COORD', 'peripheral': 'R_PERIPH'}


def base_rule(row, c):
    strengths = {'consolidator': row['in_deg'] / c['cons_min_in_deg'],
                 'distributor': row['out_deg'] / c['dist_min_out_deg']}
    p = row['pass_through']
    eligible = not row['is_seed'] and row['in_deg'] >= 1 and row['out_deg'] >= 1
    # Piecewise distance keeps the contract formula for the symmetric 0.8–1.2 corridor.
    width = (1 - c['transit_low']) if p is not None and p <= 1 else (c['transit_high'] - 1)
    strengths['transit'] = max(0.0, 2 - abs(p - 1) / width) if eligible and p is not None else 0.0
    strengths['terminal'] = row['in_kzt'] / c['term_min_in_kzt'] if row['depth'] < c['boundary_depth'] and row['out_deg'] == 0 else 0.0
    fired = [role for role, value in strengths.items() if value >= 1 - 1e-12]
    # Explicit corridor checks avoid floating-point threshold surprises.
    if 'transit' in fired and not c['transit_low'] <= p <= c['transit_high']:
        fired.remove('transit')
    role = max(fired, key=lambda r: strengths[r]) if fired else 'peripheral'
    s = strengths.get(role, max(strengths.values()))
    alternatives = [dict(role=r, rule_id=RULE_IDS[r], strength=float(strengths[r])) for r in fired if r != role]
    return role, float(s), alternatives


def assign(frame, g, c):
    rows = frame.to_dict('records')
    base = [base_rule(row, c) for row in rows]
    frame['base_role'] = [r[0] for r in base]
    role_map = dict(zip(frame.gid, frame.base_role))
    frame['up_hubs'] = [sum(role_map[u] in ('consolidator', 'distributor', 'transit') for u in g.predecessors(v)) for v in frame.gid]
    frame['down_hubs'] = [sum(role_map[u] in ('consolidator', 'distributor') for u in g.successors(v)) for v in frame.gid]
    bc_threshold = float(frame.betweenness.quantile(c['coord_bc_quantile']))
    c['coord_bc_threshold'] = bc_threshold
    details, roles, scores = [], [], []
    thresholds = {k: c[k] for k in ('cons_min_in_deg', 'dist_min_out_deg', 'transit_low', 'transit_high',
                                   'term_min_in_kzt', 'coord_bc_threshold', 'coord_min_nbr_clusters', 'coord_min_hubs', 'boundary_depth')}
    texts = {'consolidator': f"in_deg >= {c['cons_min_in_deg']}",
             'distributor': f"out_deg >= {c['dist_min_out_deg']}",
             'transit': f"не seed; in_deg >= 1; out_deg >= 1; {c['transit_low']} <= pass_through <= {c['transit_high']}",
             'terminal': f"depth < {c['boundary_depth']}; out_deg = 0; in_kzt >= {c['term_min_in_kzt']}",
             'coordinator': f"betweenness >= {bc_threshold}; n_nbr_clusters >= {c['coord_min_nbr_clusters']}; max(up_hubs, down_hubs) >= {c['coord_min_hubs']}",
             'peripheral': 'Ни одно специализированное правило не сработало'}
    for row, (role, s, alts) in zip(frame.to_dict('records'), base):
        coord = row['betweenness'] >= bc_threshold and row['n_nbr_clusters'] >= c['coord_min_nbr_clusters'] and max(row['up_hubs'], row['down_hubs']) >= c['coord_min_hubs']
        if coord:
            if role != 'peripheral':
                alts = [dict(role=role, rule_id=RULE_IDS[role], strength=s)] + alts
            role = 'coordinator'
            # If the population quantile is zero, that condition is met but adds no evidence above threshold.
            ratios = [row['betweenness'] / bc_threshold if bc_threshold > 0 else 1.0,
                      row['n_nbr_clusters'] / c['coord_min_nbr_clusters'],
                      max(row['up_hubs'], row['down_hubs']) / c['coord_min_hubs']]
            s = min(ratios)
            score = float(np.mean([min(1, v / 2) for v in ratios]))
        elif role == 'peripheral':
            score = c['isolated_role_score'] if row['is_isolated'] else 1 - 0.5 * min(1, s)
        else:
            score = min(1, 0.5 * s)
        if row['is_boundary']:
            score *= c['boundary_factor']
        limitations = [label for flag, label in [('is_boundary', 'boundary'), ('is_seed', 'seed_inflow_incomplete'),
                                                ('external_inflow', 'external_inflow'), ('is_isolated', 'isolated')] if row[flag]]
        details.append(dict(rule_id=RULE_IDS[role], rule_text=texts[role], thresholds=thresholds.copy(),
                            values={k: row[k] for k in ('in_deg', 'out_deg', 'in_kzt', 'out_kzt', 'pass_through', 'depth', 'betweenness', 'n_nbr_clusters', 'up_hubs', 'down_hubs')},
                            strength=float(s), alternatives=alts, limitations=limitations,
                            priority_contributions={}, why=None))
        roles.append(role)
        scores.append(round(max(0, min(1, score)), 4))
    frame['role'], frame['role_score'] = roles, scores
    frame['evidence_detail'] = details
    return frame
