import csv
import io
import json
import tempfile
import unittest
from pathlib import Path
from fastapi.testclient import TestClient
from backend.api import create_app
from backend.pipeline import run_pipeline


class ApiTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parent)
        self.addCleanup(self.temp.cleanup)
        self.output = Path(self.temp.name)
        self.assertEqual(run_pipeline(Path('missing'), self.output, Path('missing'), demo=True), 0)
        self.run_id = (self.output / 'LATEST').read_text().strip()
        self.snapshot_path = self.output / 'runs' / self.run_id / 'snapshot.json'
        snapshot = json.loads(self.snapshot_path.read_text(encoding='utf-8'))
        self.ids = [n['gid'] for n in snapshot['nodes']]
        # Directed chain plus an inbound edge; BFS uses both directions.
        snapshot['edges'] = [dict(src=self.ids[a], dst=self.ids[b], sum_kzt=amount, n_tx=1, depth=1,
                                  first_date='2026-07-01', last_date='2026-07-01')
                             for a, b, amount in [(0, 1, 5000), (1, 2, 7000), (3, 0, 9000)]]
        self.snapshot_path.write_text(json.dumps(snapshot), encoding='utf-8')
        self.client = self.enterContext(TestClient(create_app(self.output), raise_server_exceptions=False))

    def test_api_matches_csv(self):
        response = self.client.get('/api/v1/export/nodes_roles.csv')
        self.assertEqual(response.status_code, 200)
        self.assertIn('attachment', response.headers['content-disposition'])
        rows = list(csv.DictReader(io.StringIO(response.text)))
        for row in rows[:5]:
            data = self.client.get('/api/v1/nodes/' + row['gid']).json()
            node = data['node']
            self.assertEqual(node['gid'], row['gid'])
            self.assertEqual(node['role'], row['role'])
            self.assertEqual(node['role_score'], float(row['role_score']))
            self.assertEqual(node['priority_score'], float(row['priority_score']))
            self.assertEqual(node['cluster_id'], int(row['cluster_id']))
            self.assertEqual(data['evidence_detail']['rule_id'], 'R_PERIPH')

    def test_errors(self):
        for path, status, code in [
            ('nodes/abc', 400, 'invalid_gid'), ('nodes/1', 404, 'not_found'),
            ('nodes?limit=201', 400, 'invalid_param'), ('nodes?role=bad', 400, 'invalid_param'),
            ('nodes?is_seed=maybe', 400, 'invalid_param'), ('top?n=0', 400, 'invalid_param'),
            ('clusters/999', 404, 'not_found'), ('export/secret', 400, 'invalid_param'),
            ('subgraph', 400, 'invalid_param'), ('subgraph?gid=1&cluster_id=0', 400, 'invalid_param'),
            ('unknown', 404, 'not_found')]:
            with self.subTest(path=path):
                response = self.client.get('/api/v1/' + path)
                self.assertEqual(response.status_code, status)
                self.assertEqual(response.json()['error']['code'], code)

    def test_filters_top_and_clusters(self):
        data = self.client.get('/api/v1/nodes?role=peripheral&is_seed=true&limit=2&offset=1').json()
        self.assertEqual(data['total'], 24)
        self.assertEqual([n['gid'] for n in data['items']], self.ids[1:3])
        self.assertEqual(self.client.get('/api/v1/nodes', params={'q': self.ids[5]}).json()['total'], 1)
        self.assertEqual(self.client.get('/api/v1/nodes?is_seed=false').json()['total'], 0)
        top = self.client.get('/api/v1/top?n=24').json()
        self.assertEqual(len(top['items']), 24)
        self.assertIn('role_score', top['items'][0])
        self.assertEqual(self.client.get('/api/v1/clusters?limit=2&offset=1').json()['total'], 24)
        self.assertEqual(self.client.get('/api/v1/clusters/0').json()['nodes'][0]['gid'], self.ids[0])

    def test_neighbors_and_bfs(self):
        result = self.client.get(f'/api/v1/nodes/{self.ids[0]}/neighbors?limit=1').json()
        self.assertEqual(result['total'], 2)
        self.assertTrue(result['truncated'])
        self.assertEqual(result['items'][0]['node']['gid'], self.ids[3])
        outgoing = self.client.get(f'/api/v1/nodes/{self.ids[0]}/neighbors?direction=out').json()
        self.assertEqual(outgoing['total'], 1)
        result = self.client.get('/api/v1/subgraph', params={'gid': self.ids[0], 'depth': 2}).json()
        self.assertEqual({n['gid'] for n in result['nodes']}, set(self.ids[:4]))
        self.assertEqual(len(result['edges']), 3)
        result = self.client.get('/api/v1/subgraph', params={'gid': self.ids[0], 'depth': 2, 'max_nodes': 2}).json()
        self.assertEqual(len(result['nodes']), 2)
        self.assertTrue(result['truncated'])
        self.assertEqual(len(self.client.get('/api/v1/subgraph?cluster_id=0').json()['nodes']), 1)

    def test_reload_export_consistency_and_failure(self):
        old_export = self.client.get('/api/v1/export/nodes_roles.csv').content
        self.assertEqual(run_pipeline(Path('missing'), self.output, Path('missing'), demo=True), 0)
        new_id = (self.output / 'LATEST').read_text().strip()
        self.assertNotEqual(new_id, self.run_id)
        (self.output / 'nodes_roles.csv').write_text('wrong root file', encoding='utf-8')
        self.assertEqual(self.client.get('/api/v1/health').json()['run_id'], self.run_id)
        self.assertEqual(self.client.get('/api/v1/export/nodes_roles.csv').content, old_export)
        self.assertEqual(self.client.post('/api/v1/reload').json()['run_id'], new_id)
        (self.output / 'LATEST').write_text('../outside', encoding='utf-8')
        with self.assertLogs(level='ERROR'):
            response = self.client.post('/api/v1/reload')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json()['error']['code'], 'internal')
        self.assertEqual(self.client.get('/api/v1/graph').json()['run_id'], new_id)

    def test_no_result_and_offline_check_page(self):
        empty = self.output / 'empty'
        with TestClient(create_app(empty)) as client:
            self.assertEqual(client.get('/api/v1/health').status_code, 200)
            self.assertEqual(client.get('/api/v1/overview').json()['status'], 'no_result')
            for endpoint in ['graph', 'nodes', 'top', 'clusters', 'export/nodes_roles.csv']:
                response = client.get('/api/v1/' + endpoint)
                self.assertEqual(response.status_code, 503)
                self.assertEqual(response.json()['error']['code'], 'no_result')
            self.assertEqual(client.get('/check').status_code, 200)
            self.assertNotIn('cdn', client.get('/check').text)
            self.assertEqual(client.get('/openapi.json').status_code, 200)
        self.assertEqual(self.client.post('/api/v1/assistant').json()['error']['code'], 'invalid_param')

    def test_failed_attempt_visible_and_cors(self):
        self.assertEqual(run_pipeline(Path('missing'), self.output, Path('missing')), 2)
        data = self.client.get('/api/v1/overview').json()
        self.assertEqual(data['run_id'], self.run_id)
        self.assertEqual(data['last_attempt']['status'], 'failed')
        response = self.client.get('/api/v1/health', headers={'Origin': 'http://localhost:5173'})
        self.assertEqual(response.headers['access-control-allow-origin'], 'http://localhost:5173')


if __name__ == '__main__':
    unittest.main()
