import numpy as np


def rank(frame, c):
    weights = c['priority_weights']
    contributions = {}
    for key in ('in_kzt', 'betweenness', 'n_nbr_clusters', 'seed_reach'):
        contributions[key] = frame[key].rank(method='max', pct=True).where(frame[key] != 0, 0) * weights[key]
    contributions['role'] = frame.role.map(c['role_weights']) * frame.role_score * weights['role']
    factors = np.where(frame.is_seed, c['seed_factor'], 1.0)
    raw = sum(contributions.values()) * factors
    maximum = float(raw.max())
    frame['priority_score'] = (raw / maximum if maximum else raw * 0).round(6)
    for i, detail in enumerate(frame.evidence_detail):
        detail['priority_contributions'] = {key: float(vals.iloc[i]) for key, vals in contributions.items()}
        detail['priority_contributions']['seed_factor'] = float(factors[i])
    order = frame.sort_values(['priority_score', 'gid'], ascending=[False, True]).index
    frame['priority_rank'] = 0
    frame.loc[order, 'priority_rank'] = range(1, len(frame) + 1)
    return frame
