"""Acceptance checks on local organizer data; never modify original inputs."""
import csv
import hashlib
import importlib.util
import json
import random
import shutil
import tempfile
import time
import unittest
from pathlib import Path

from fastapi.testclient import TestClient
from backend.api import create_app
from backend.export import SCHEMAS
from backend.pipeline import run_pipeline

BASE = Path(__file__).resolve().parents[1]
DATA = BASE / 'data'
CONFIG = BASE.parent / 'graph' / 'config' / 'methodology.yaml'
INPUTS = ['nodes.parquet', 'edges.parquet', 'transactions.parquet']
HAS_INPUTS = all((DATA / name).is_file() for name in INPUTS)
HAS_ENGINE = all(importlib.util.find_spec(name) for name in ['pandas', 'pyarrow', 'networkx', 'scipy', 'yaml'])


def hashes(directory, names):
    return {name: hashlib.sha256((directory / name).read_bytes()).hexdigest() for name in names}


@unittest.skipUnless(HAS_INPUTS and HAS_ENGINE, 'Нужны backend/data/*.parquet и зависимости requirements-graph.txt')
class RealDataAcceptanceTests(unittest.TestCase):
    def test_a01_a10_a11_a14(self):
        import pandas as pd
        original = hashes(DATA, INPUTS)
        with tempfile.TemporaryDirectory(dir=BASE / 'tests') as tmp:
            root = Path(tmp)
            first, second = root / 'first', root / 'second'
            for output in [first, second]:
                start = time.perf_counter()
                self.assertEqual(run_pipeline(DATA, output, CONFIG), 0)
                self.assertLess(time.perf_counter() - start, 300, 'A01: анализ должен занимать менее 300 с')
            expected = hashes(first, SCHEMAS)
            self.assertEqual(expected, hashes(second, SCHEMAS), 'A10: CSV должны совпадать побайтово')
            with (first / 'nodes_roles.csv').open(encoding='utf-8', newline='') as stream:
                rows = list(csv.DictReader(stream))
            with TestClient(create_app(first)) as client:
                for row in random.Random(42).sample(rows, min(5, len(rows))):
                    response = client.get('/api/v1/nodes/' + row['gid'])
                    self.assertEqual(response.status_code, 200)
                    node = response.json()['node']
                    for field in ['gid', 'role', 'evidence']:
                        self.assertEqual(node[field], row[field])
                    for field in ['role_score', 'priority_score']:
                        self.assertEqual(node[field], float(row[field]))
                    self.assertEqual(node['cluster_id'], int(row['cluster_id']))
                for name in SCHEMAS:
                    response = client.get('/api/v1/export/' + name)
                    self.assertEqual(response.status_code, 200)
                    self.assertEqual(hashlib.sha256(response.content).hexdigest(), expected[name])
            broken = root / 'broken'
            broken.mkdir()
            marker = (first / 'LATEST').read_bytes()
            for defect in ['missing_file', 'duplicate_gid', 'unknown_gid']:
                with self.subTest(defect=defect):
                    for name in INPUTS:
                        shutil.copyfile(DATA / name, broken / name)
                    if defect == 'missing_file':
                        (broken / 'edges.parquet').unlink()
                    elif defect == 'duplicate_gid':
                        nodes = pd.read_parquet(broken / 'nodes.parquet')
                        pd.concat([nodes, nodes.iloc[:1]]).to_parquet(broken / 'nodes.parquet', index=False)
                    else:
                        nodes = pd.read_parquet(broken / 'nodes.parquet')
                        unknown = 1
                        ids = set(nodes.gid)
                        while unknown in ids:
                            unknown += 1
                        edges = pd.read_parquet(broken / 'edges.parquet')
                        edges.loc[0, 'dst'] = unknown
                        edges.to_parquet(broken / 'edges.parquet', index=False)
                    self.assertEqual(run_pipeline(broken, first, CONFIG), 2)
                    self.assertEqual((first / 'LATEST').read_bytes(), marker)
                    self.assertEqual(hashes(first, SCHEMAS), expected)
                    attempt = json.loads((first / 'last_attempt.json').read_text(encoding='utf-8'))
                    self.assertEqual(attempt['status'], 'failed')
        self.assertEqual(hashes(DATA, INPUTS), original, 'Исходные parquet не должны изменяться')
