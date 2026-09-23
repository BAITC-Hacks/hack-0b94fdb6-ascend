"""Contract 2.0 graph engine. analyze() has no writes or network operations."""
from pathlib import Path
from time import perf_counter
import platform
import os
import math
import yaml
from .models import AnalysisResult, DataValidationError
from .load import load
from .validate import validate
from .features import build_features
from .clusters import partition, summarize
from .roles import assign
from .priority import rank
from .evidence import explain
from .layout import layout

DEFAULT_CONFIG = Path(__file__).parent / 'config' / 'methodology.yaml'


def load_config(path):
    defaults = yaml.safe_load(DEFAULT_CONFIG.read_text(encoding='utf-8'))
    supplied = yaml.safe_load(Path(path).read_text(encoding='utf-8'))
    if not isinstance(supplied, dict):
        raise ValueError('Конфигурация должна быть YAML-объектом')
    unknown = set(supplied) - set(defaults)
    if unknown:
        raise ValueError(f'Неизвестные параметры: {sorted(unknown)}')
    defaults.update(supplied)
    c = defaults
    if c['version'] != 'roles-v1' or not 0 < c['transit_low'] < 1 < c['transit_high']:
        raise ValueError('Некорректная версия или коридор транзита')
    for key, value in c.items():
        if isinstance(value, (int, float)) and (not math.isfinite(value) or value < 0 or (value == 0 and key not in ('random_seed', 'boundary_factor', 'isolated_role_score', 'seed_factor'))):
            raise ValueError(f'Параметр {key} должен быть конечным и положительным')
    for key in ('coord_bc_quantile', 'boundary_factor', 'isolated_role_score', 'seed_factor', 'pagerank_alpha', 'cluster_fanout_share', 'cluster_transit_share'):
        if not 0 <= c[key] <= 1:
            raise ValueError(f'{key} должен лежать в [0, 1]')
    for key in ('priority_weights', 'role_weights'):
        if set(c[key]) != set(yaml.safe_load(DEFAULT_CONFIG.read_text(encoding='utf-8'))[key]) or any(not isinstance(v, (int, float)) or not math.isfinite(v) or not 0 <= v <= 1 for v in c[key].values()):
            raise ValueError(f'Некорректные {key}')
    if not math.isclose(sum(c['priority_weights'].values()), 1):
        raise ValueError('Сумма priority_weights должна быть 1')
    if c['top_n_api'] < c['top_n'] or c['evidence_max_len'] > 200:
        raise ValueError('Некорректные лимиты top/evidence')
    for key in ('random_seed', 'cons_min_in_deg', 'dist_min_out_deg', 'coord_min_nbr_clusters', 'coord_min_hubs', 'top_n', 'top_n_api', 'evidence_max_len', 'boundary_depth', 'layout_iterations', 'layout_small_component', 'cluster_collect_seeds'):
        if type(c[key]) is not int:
            raise ValueError(f'{key} должен быть целым числом')
    return c


def analyze(data_dir: Path, config_path: Path = DEFAULT_CONFIG) -> AnalysisResult:
    started = perf_counter()
    timings = {}
    def stage(name, fn):
        t = perf_counter()
        result = fn()
        timings[name] = round(perf_counter()-t, 6)
        return result
    config = load_config(config_path)
    nodes, edges, tx, checksums = stage('load', lambda: load(data_dir))
    quality = stage('validate', lambda: validate(nodes, edges, tx, config))
    nodes = nodes.sort_values('gid').reset_index(drop=True)
    edges = edges.sort_values(['src', 'dst']).reset_index(drop=True)
    tx = tx.sort_values(['src', 'dst', 'date', 'sum_kzt']).reset_index(drop=True)
    dates = tx.groupby(['src', 'dst']).agg(first_date=('date', 'min'), last_date=('date', 'max')).reset_index()
    edges = edges.merge(dates, on=['src', 'dst'], how='left')
    for col in ('first_date', 'last_date'):
        edges[col] = edges[col].map(str)
    g, frame = stage('features', lambda: build_features(nodes, edges, config))
    ug, components = stage('clusters', lambda: partition(g, frame, config))
    frame = stage('roles', lambda: assign(frame, g, config))
    frame = stage('priority', lambda: rank(frame, config))
    frame = stage('evidence', lambda: explain(frame, config))
    frame = stage('layout', lambda: layout(ug, components, frame, config))
    clusters = stage('cluster_hypotheses', lambda: summarize(frame, edges, config))
    top = frame.sort_values('priority_rank').head(config['top_n_api'])[['priority_rank', 'gid', 'role', 'priority_score', 'why']].rename(columns={'priority_rank': 'rank'}).reset_index(drop=True)
    expected = config.get('reference_counts', {}).get('components')
    if expected is not None and expected != len(components):
        quality['warnings'].append(f'components: {len(components)}, справочное значение {expected}')
    counts = dict(quality['counts'], clusters=len(clusters), components=len(components), isolated=int(frame.is_isolated.sum()), boundary=int(frame.is_boundary.sum()))
    from .models import ROLES
    meta = dict(methodology_version=config['version'], contract_version='2.0',
                duration_sec=round(perf_counter()-started, 6), stage_timings=timings,
                input_checksums=checksums, counts=counts,
                role_counts={r: int((frame.role == r).sum()) for r in ROLES},
                turnover_kzt=round(float(edges.sum_kzt.sum()), 2),
                period={'from': str(tx.date.min()) if len(tx) else None, 'to': str(tx.date.max()) if len(tx) else None},
                config=config, warnings=quality['warnings'],
                machine={'os': platform.system(), 'python': platform.python_version(), 'cpu': platform.processor() or str(os.cpu_count()), 'ram_gb': None}, error=None)
    return AnalysisResult(frame, edges, clusters, top, meta, quality)


__all__ = ['analyze', 'AnalysisResult', 'DataValidationError', 'DEFAULT_CONFIG']
