"""Lossless snapshot boundary: identifiers are decimal strings, nulls are explicit."""
import math
import numpy as np


def json_value(value, key=None):
    if value is None:
        return None
    if isinstance(value, dict):
        return {str(k): json_value(v, str(k)) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_value(v, 'gid' if key in ('gids', 'top_gids') else None) for v in value]
    if key in ('gid', 'src', 'dst'):
        if isinstance(value, (float, np.floating)):
            raise ValueError('gid нельзя сериализовать из float')
        return str(value)
    if isinstance(value, np.generic):
        value = value.item()
    if isinstance(value, float) and not math.isfinite(value):
        raise ValueError('NaN/Infinity запрещены в снимке')
    return value


def snapshot(result, run=None):
    return json_value({'run': run or result.run_meta,
                       'nodes': result.nodes.to_dict('records'), 'edges': result.edges.to_dict('records'),
                       'clusters': result.clusters.to_dict('records'), 'top': result.top.to_dict('records')})
