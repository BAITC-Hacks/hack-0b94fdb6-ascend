import math
import re
from datetime import date, datetime
import numpy as np
import pandas as pd
from .models import DataValidationError


def fail(file, column, bad, message):
    raise DataValidationError(f'{file}: {column}: {message}; строк: {len(bad)}',
                              {'file': file, 'column': column, 'count': len(bad),
                               'examples': [str(x) for x in list(bad)[:5]]})


def integers(frame, file, col, minimum=0, maximum=None):
    vals = []
    for x in frame[col]:
        # Never round a float identifier, even if it looks integral.
        if isinstance(x, (bool, np.bool_)) or not isinstance(x, (int, np.integer, str)) or not re.fullmatch(r'[0-9]+', str(x)):
            fail(file, col, [x], 'ожидается точное целое число, не float')
        v = int(x)
        if v < minimum or v > np.iinfo(np.int64).max or (maximum is not None and v > maximum):
            fail(file, col, [x], 'значение вне диапазона')
        vals.append(v)
    frame[col] = pd.Series(vals, index=frame.index, dtype='int64')


def validate(nodes, edges, tx, config):
    schemas = {'nodes': ['gid', 'depth', 'is_seed'],
               'edges': ['src', 'dst', 'sum_kzt', 'n_tx', 'depth'],
               'transactions': ['src', 'dst', 'date', 'sum_kzt']}
    for name, df in [('nodes', nodes), ('edges', edges), ('transactions', tx)]:
        missing = set(schemas[name]) - set(df.columns)
        if missing:
            fail(name, 'schema', sorted(missing), 'нет обязательных колонок')
        for col in schemas[name]:
            if df[col].isna().any():
                fail(name, col, df.index[df[col].isna()], 'пропуски недопустимы')
        for col in ('gid', 'src', 'dst', 'n_tx', 'depth'):
            if col in schemas[name]:
                integers(df, name, col, 1 if col == 'n_tx' or (name == 'edges' and col == 'depth') else 0,
                         config['boundary_depth'] if col == 'depth' else None)
        if 'sum_kzt' in schemas[name]:
            try:
                df['sum_kzt'] = pd.to_numeric(df.sum_kzt, errors='raise').astype(float)
            except (ValueError, TypeError) as exc:
                fail(name, 'sum_kzt', [str(exc)], 'некорректная сумма')
            bad = ~np.isfinite(df.sum_kzt) | (df.sum_kzt <= 0)
            if bad.any():
                fail(name, 'sum_kzt', df.index[bad], 'сумма должна быть конечной и положительной')
    if not len(nodes):
        fail('nodes', 'gid', [], 'пустой список узлов')
    if not nodes.is_seed.map(lambda x: isinstance(x, (bool, np.bool_))).all():
        fail('nodes', 'is_seed', nodes.is_seed.tolist(), 'ожидается bool')
    if nodes.gid.duplicated().any():
        fail('nodes', 'gid', nodes.loc[nodes.gid.duplicated(), 'gid'], 'дубли')
    if edges.duplicated(['src', 'dst']).any():
        fail('edges', 'src,dst', edges.index[edges.duplicated(['src', 'dst'])], 'дубли пар')
    ids = set(nodes.gid)
    for name, df in [('edges', edges), ('transactions', tx)]:
        for col in ('src', 'dst'):
            bad = df.loc[~df[col].isin(ids), col]
            if len(bad):
                fail(name, col, bad, 'неизвестный gid')
    dates = []
    for value in tx.date:
        try:
            if not isinstance(value, (str, date, datetime, pd.Timestamp)):
                raise ValueError('not a calendar date')
            parsed = pd.Timestamp(value)
            if pd.isna(parsed) or parsed.tzinfo is not None or parsed != parsed.normalize():
                raise ValueError('time component')
            dates.append(parsed.date())
        except (ValueError, TypeError, OverflowError):
            fail('transactions', 'date', [value], 'ожидается календарная дата без времени')
    tx['date'] = pd.Series(dates, index=tx.index, dtype=object)
    agg = tx.groupby(['src', 'dst']).agg(tx_sum=('sum_kzt', 'sum'), tx_count=('sum_kzt', 'size')).reset_index()
    joined = edges.merge(agg, on=['src', 'dst'], how='outer', indicator=True)
    bad = (joined['_merge'] != 'both') | ((joined.sum_kzt - joined.tx_sum).abs() > 0.01) | (joined.n_tx != joined.tx_count)
    if bad.any():
        fail('edges/transactions', 'src,dst', joined.index[bad], 'не совпадают пары, суммы (>0.01 KZT) или число транзакций')
    warnings = []
    loops = edges.loc[edges.src == edges.dst, ['src', 'dst']].to_dict('records')
    if loops:
        warnings.append(f'Петли исключены из метрик, сохранены в рёбрах: {len(loops)}')
    depth = nodes.set_index('gid').depth
    depth_errors = int((edges.depth != edges.src.map(depth) + 1).sum())
    if depth_errors:
        warnings.append(f'edges.depth отличается от depth(src)+1: {depth_errors}')
    observed = {'nodes': len(nodes), 'edges': len(edges), 'transactions': len(tx), 'seeds': int(nodes.is_seed.sum())}
    for key, value in observed.items():
        expected = config.get('reference_counts', {}).get(key)
        if expected is not None and value != expected:
            warnings.append(f'{key}: {value}, справочное значение {expected}')
    for dep, expected in config.get('reference_depth_counts', {}).items():
        actual = int((nodes.depth == int(dep)).sum())
        if actual != expected:
            warnings.append(f'depth={dep}: {actual}, справочное значение {expected}')
    turnover = float(edges.sum_kzt.sum())
    if not math.isfinite(turnover):
        fail('edges', 'sum_kzt', [], 'переполнение суммарного оборота')
    if abs(turnover - config.get('reference_turnover_kzt', turnover)) > 0.01:
        warnings.append('Оборот отличается от справочного значения')
    if len(tx):
        period = {'from': str(min(dates)), 'to': str(max(dates))}
        if config.get('reference_period', period) != period:
            warnings.append('Период отличается от справочного значения')
    return {'warnings': warnings, 'self_loops': loops, 'edge_depth_mismatches': depth_errors,
            'transaction_reconciliation': 'passed', 'counts': observed}
