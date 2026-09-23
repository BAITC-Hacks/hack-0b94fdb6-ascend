"""End-to-end real engine on generated parquet, without organizer data."""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from fastapi.testclient import TestClient
from backend.api import create_app
from backend.export import SCHEMAS
from backend.pipeline import run_pipeline


@unittest.skipUnless(all(importlib.util.find_spec(m) for m in ['pandas', 'pyarrow', 'networkx', 'scipy', 'yaml']),
                     'Установите backend/requirements-graph.txt для интеграции Graph')
class GraphIntegrationTests(unittest.TestCase):
    def test_parquet_to_api_determinism_and_failed_inputs(self):
        import pandas as pd
        from graph import DEFAULT_CONFIG
        with tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parent) as tmp:
            root = Path(tmp)
            data, output = root / 'data', root / 'output'
            data.mkdir()
            base = 900000000000000001
            nodes = pd.DataFrame({'gid': [base + i for i in range(4)], 'depth': [0, 1, 4, 0],
                                  'is_seed': [True, False, False, True]})
            edges = pd.DataFrame({'src': [base, base + 1], 'dst': [base + 1, base + 2],
                                  'sum_kzt': [400000.0, 380000.0], 'n_tx': [1, 1], 'depth': [1, 2]})
            tx = edges[['src', 'dst', 'sum_kzt']].copy()
            tx['date'] = '2026-07-01'
            for name, frame in [('nodes', nodes), ('edges', edges), ('transactions', tx)]:
                frame.to_parquet(data / f'{name}.parquet', index=False)
            self.assertEqual(run_pipeline(data, output, DEFAULT_CONFIG), 0)
            first = {n: (output / n).read_bytes() for n in SCHEMAS}
            self.assertEqual(run_pipeline(data, output, DEFAULT_CONFIG), 0)
            self.assertEqual(first, {n: (output / n).read_bytes() for n in SCHEMAS})
            marker = (output / 'LATEST').read_bytes()
            with TestClient(create_app(output)) as client:
                self.assertEqual(client.get('/api/v1/nodes').json()['total'], 4)
                card = client.get(f'/api/v1/nodes/{base + 1}').json()
                self.assertEqual(card['node']['role'], 'transit')
                self.assertEqual(len(client.get('/api/v1/graph').json()['edges']), 2)
                self.assertEqual(client.get('/api/v1/export/nodes_roles.csv').content, first['nodes_roles.csv'])
            for defect in ['duplicate_gid', 'unknown_gid', 'missing_file']:
                with self.subTest(defect=defect):
                    nodes.to_parquet(data / 'nodes.parquet', index=False)
                    edges.to_parquet(data / 'edges.parquet', index=False)
                    if defect == 'duplicate_gid':
                        pd.concat([nodes, nodes.iloc[:1]]).to_parquet(data / 'nodes.parquet', index=False)
                    elif defect == 'unknown_gid':
                        bad = edges.copy()
                        bad.loc[0, 'dst'] = 42
                        bad.to_parquet(data / 'edges.parquet', index=False)
                    else:
                        (data / 'edges.parquet').unlink()
                    self.assertEqual(run_pipeline(data, output, DEFAULT_CONFIG), 2)
                    self.assertEqual((output / 'LATEST').read_bytes(), marker)
                    self.assertEqual(first, {n: (output / n).read_bytes() for n in SCHEMAS})
                    self.assertEqual(json.loads((output / 'last_attempt.json').read_text(encoding='utf-8'))['status'], 'failed')
