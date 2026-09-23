"""JSON conversion without loss of 64-bit identifiers."""
import json
import math
from datetime import date, datetime
from .export import gid, records

NULLABLE = {'pass_through', 'temporal', 'why', 'error'}


def normalize(value, key='', nullable=False):
    if hasattr(value, 'item'):
        value = value.item()
    if key in {'gid', 'src', 'dst'}:
        return gid(value)
    if key == 'top_gids':
        return [gid(item) for item in value]
    if value is None or isinstance(value, float) and math.isnan(value):
        if key in NULLABLE or nullable:
            return None
        raise ValueError(f'Недопустимое пустое поле: {key}')
    if isinstance(value, dict):
        return {str(k): normalize(v, str(k), nullable or key in ('values', 'extras')) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [normalize(v, nullable=nullable) for v in value]
    if isinstance(value, (date, datetime)):
        return value.isoformat()
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError(f'Недопустимое число: {key}')
        precision = {'role_score': 4, 'priority_score': 6, 'sum_kzt': 2, 'sum_kzt_internal': 2, 'in_kzt': 2, 'out_kzt': 2, 'turnover_kzt': 2}.get(key)
        return round(value, precision) if precision is not None else value
    return value


def write_json(path, value):
    path.write_text(json.dumps(normalize(value), ensure_ascii=False, allow_nan=False, indent=2) + '\n', encoding='utf-8')


def write_snapshot(directory, result, run):
    snapshot = {'run': run, **{key: records(getattr(result, key)) for key in ['nodes', 'edges', 'clusters', 'top']}}
    if getattr(result, 'extras', None):
        try:
            from graph.extras.export import payload, write
            snapshot['extras'] = payload(result.extras)
            write(directory, result.extras)
        except Exception as exc:
            snapshot.pop('extras', None)
            warning = f'extras export: {type(exc).__name__}'
            if warning not in result.quality['warnings']:
                result.quality['warnings'].append(warning)
    write_json(directory / 'snapshot.json', snapshot)
    write_json(directory / 'run.json', run)
    write_json(directory / 'quality_report.json', result.quality)
