import ast
from pathlib import Path
import pandas as pd
import pytest
from graph import analyze, DEFAULT_CONFIG, DataValidationError
from graph.roles import base_rule
from graph.serialization import snapshot
from graph import load_config


@pytest.fixture
def c():
    return load_config(DEFAULT_CONFIG)


def row(**kw):
    return dict(in_deg=0, out_deg=0, in_kzt=0.0, pass_through=None, is_seed=False, depth=1, **kw)


@pytest.mark.parametrize('patch,expected', [
    ({'in_deg': 5}, 'consolidator'), ({'out_deg': 10}, 'distributor'),
    ({'in_deg': 1, 'out_deg': 1, 'pass_through': .95}, 'transit'),
    ({'in_deg': 1, 'out_deg': 1, 'pass_through': .8}, 'transit'),
    ({'in_deg': 1, 'out_deg': 1, 'pass_through': 1.2}, 'transit'),
    ({'in_deg': 1, 'out_deg': 1, 'pass_through': .95, 'is_seed': True}, 'peripheral'),
    ({'in_deg': 1, 'in_kzt': 300000.0}, 'terminal'),
    ({'in_deg': 1, 'in_kzt': 300000.0, 'depth': 4}, 'peripheral'),
    ({'in_deg': 5, 'in_kzt': 300000.0, 'depth': 4}, 'consolidator'),
    ({}, 'peripheral'), ({'in_deg': 5, 'out_deg': 10}, 'consolidator')])
def test_rules(c, patch, expected):
    data = row()
    data.update(patch)
    assert base_rule(data, c)[0] == expected


def write_data(folder, nodes=None, edges=None, tx=None):
    folder.mkdir(exist_ok=True)
    # Above JS safe integer; consecutive IDs would collapse if converted via float.
    first = int('900000000000000001')
    if nodes is None:
        nodes = pd.DataFrame({'gid': [first + i for i in range(4)], 'depth': [0, 1, 4, 0], 'is_seed': [True, False, False, True]})
    if edges is None:
        edges = pd.DataFrame({'src': [first, first+1], 'dst': [first+1, first+2], 'sum_kzt': [400000.0, 380000.0], 'n_tx': [1, 1], 'depth': [1, 2]})
    if tx is None:
        tx = edges[['src', 'dst', 'sum_kzt']].copy()
        tx['date'] = '2026-07-01'
    for name, df in [('nodes', nodes), ('edges', edges), ('transactions', tx)]:
        df.to_parquet(folder / (name + '.parquet'), index=False)
    return nodes, edges, tx


def test_full_contract_determinism_and_no_writes(tmp_path):
    nodes, _, _ = write_data(tmp_path)
    before = set(tmp_path.iterdir())
    first, second = analyze(tmp_path), analyze(tmp_path)
    for name in ('nodes', 'edges', 'clusters', 'top'):
        pd.testing.assert_frame_equal(getattr(first, name), getattr(second, name))
    assert set(tmp_path.iterdir()) == before
    assert set(first.nodes.gid) == set(nodes.gid)
    assert first.nodes.gid.dtype == 'int64'
    assert first.nodes.loc[first.nodes.is_boundary, 'role'].tolist() == ['peripheral']
    isolated = first.nodes[first.nodes.is_isolated].iloc[0]
    assert isolated.role == 'peripheral' and isolated.role_score == .3
    assert 'данных недостаточно' in isolated.evidence
    assert isolated.pass_through is None
    assert first.nodes.evidence.str.len().max() <= 200
    snap = snapshot(first)
    import json
    encoded = json.dumps(snap, ensure_ascii=False, allow_nan=False)
    assert str(nodes.gid.iloc[1]) in encoded
    assert all(isinstance(n['gid'], str) for n in snap['nodes'])
    assert all(isinstance(e['src'], str) for e in snap['edges'])
    assert first.clusters.n_nodes.sum() == len(nodes)
    assert first.nodes.role_score.between(0, 1).all()
    assert first.nodes.priority_score.between(0, 1).all()


@pytest.mark.parametrize('defect', ['duplicate_node', 'unknown_node', 'sum', 'missing_tx', 'count', 'nan', 'infinity', 'bad_date', 'duplicate_pair', 'float_gid', 'fractional_count', 'bool_string', 'missing_column'])
def test_validation(tmp_path, defect):
    n, e, t = write_data(tmp_path)
    if defect == 'duplicate_node': n = pd.concat([n, n.iloc[:1]])
    elif defect == 'unknown_node': e.loc[0, 'dst'] = 42
    elif defect == 'sum': t.loc[0, 'sum_kzt'] += .02
    elif defect == 'missing_tx': t = t.iloc[:1]
    elif defect == 'count': e.loc[0, 'n_tx'] = 2
    elif defect == 'nan': e.loc[0, 'sum_kzt'] = float('nan')
    elif defect == 'infinity': e.loc[0, 'sum_kzt'] = float('inf')
    elif defect == 'bad_date': t.loc[0, 'date'] = '2026-02-30'
    elif defect == 'duplicate_pair': e = pd.concat([e, e.iloc[:1]])
    elif defect == 'float_gid': n.gid = n.gid.astype(float)
    elif defect == 'fractional_count': e['n_tx'] = [1.5, 1.0]
    elif defect == 'bool_string': n.is_seed = n.is_seed.astype(str)
    elif defect == 'missing_column': n = n.drop(columns='depth')
    write_data(tmp_path, n, e, t)
    with pytest.raises(DataValidationError) as info:
        analyze(tmp_path)
    assert info.value.details


def test_missing_file(tmp_path):
    with pytest.raises(DataValidationError):
        analyze(tmp_path)


def test_only_isolates_and_zero_priority(tmp_path):
    n, e, t = write_data(tmp_path)
    write_data(tmp_path, n, e.iloc[:0], t.iloc[:0])
    result = analyze(tmp_path)
    assert result.nodes.priority_score.eq(0).all()
    assert len(result.clusters) == len(n)
    assert result.nodes.pass_through.map(lambda x: x is None).all()


def test_no_literal_real_ids():
    for path in Path(DEFAULT_CONFIG).parents[1].glob('*.py'):
        for node in ast.walk(ast.parse(path.read_text(encoding='utf-8'))):
            assert not (isinstance(node, ast.Constant) and isinstance(node.value, (float, int)) and node.value >= 10**15)


def test_projection_reciprocal_and_loops(tmp_path, c):
    from graph.features import build_features
    from graph.clusters import partition
    n, e, t = write_data(tmp_path)
    back = e.iloc[[0]].copy()
    back['src'], back['dst'] = back.dst.copy(), back.src.copy()
    loop = e.iloc[[0]].copy()
    loop.dst = loop.src
    e = pd.concat([e, back, loop], ignore_index=True)
    write_data(tmp_path, n, e)
    result = analyze(tmp_path)
    g, frame = build_features(n, e, c)
    ug, _ = partition(g, frame, c)
    assert ug.edges[int(e.src.iloc[0]), int(e.dst.iloc[0])]['w'] == 800000
    assert len(result.quality['self_loops']) == 1
    assert result.nodes.in_tx.sum() == 3


def test_coordinator_needs_structure_and_keeps_base(c):
    import networkx as nx
    from graph.roles import assign
    g = nx.DiGraph([(2, 1), (3, 1)])
    rows = []
    for gid, out_deg, bc, clusters in [(1, 0, 1., 2), (2, 10, 0., 1), (3, 10, 0., 1)]:
        r = row()
        r.update(gid=gid, out_deg=out_deg, out_kzt=0., betweenness=bc,
                 n_nbr_clusters=clusters, is_boundary=False, is_isolated=False, external_inflow=False)
        rows.append(r)
    frame = assign(pd.DataFrame(rows), g, c)
    assert frame.iloc[0].role == 'coordinator'
    assert frame.iloc[0].base_role == 'peripheral'
    assert frame.iloc[0].up_hubs == 2
    rows[0]['n_nbr_clusters'] = 1
    assert assign(pd.DataFrame(rows), g, c).iloc[0].role == 'peripheral'
