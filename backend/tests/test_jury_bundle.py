"""Acceptance checks against the exact organizer-data bundle shipped in Git."""
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient
from backend.api import create_app
from backend.jury import ROOT, check_bundle


class JuryBundleTests(unittest.TestCase):
    def test_bundle_and_missing_inputs(self):
        run = check_bundle()
        self.assertEqual(run['counts']['nodes'], 2248)
        self.assertEqual(run['counts']['edges'], 3119)
        self.assertEqual(run['counts']['transactions'], 4840)
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(OSError):
                check_bundle(Path(directory))
        read_bytes = Path.read_bytes

        def corrupt_input(path):
            return b'incomplete download' if path.name == 'nodes.parquet' else read_bytes(path)

        with patch.object(Path, 'read_bytes', corrupt_input):
            with self.assertRaisesRegex(ValueError, 'nodes.parquet'):
                check_bundle()

    def test_real_case_site_exports_and_local_assistant(self):
        with patch.dict(os.environ, {'ASSISTANT_ENABLED': '0', 'OPENAI_API_KEY': '', 'OPENAI_MODEL': ''}):
            with TestClient(create_app(ROOT / 'backend/jury_snapshot')) as client:
                health = client.get('/api/v1/health').json()
                self.assertTrue(health['run_id'])
                self.assertFalse(health['assistant_enabled'])
                self.assertEqual(client.get('/').status_code, 200)
                graph = client.get('/api/v1/graph').json()
                self.assertEqual(len(graph['nodes']), 2248)
                self.assertEqual(len(graph['edges']), 3119)
                top = client.get('/api/v1/top?n=10').json()['items']
                gid = top[0]['gid']
                self.assertEqual(client.get('/api/v1/nodes/' + gid).json()['node']['gid'], gid)
                for name in ['nodes_roles.csv', 'clusters.csv', 'top_nodes.csv']:
                    response = client.get('/api/v1/export/' + name)
                    self.assertEqual(response.status_code, 200)
                    self.assertIn('attachment', response.headers['content-disposition'])
                pdf = client.post('/api/v1/export/report.pdf', json={
                    'run_id': health['run_id'], 'keys': ['node:' + gid],
                })
                self.assertEqual(pdf.status_code, 200)
                self.assertTrue(pdf.content.startswith(b'%PDF-'))
                for question in ['Выбери 10 приоритетных узлов', 'Select 10 priority nodes. Answer in English.',
                                 'Басымдығы жоғары 10 түйінді таңда. Қазақ тілінде жауап бер.']:
                    chat = client.post('/api/v1/assistant', json={'question': question}).json()
                    self.assertEqual(chat['run_id'], health['run_id'])
                    self.assertEqual(chat['gids'], [row['gid'] for row in top])
                    self.assertEqual(chat['mode'], 'fallback')
                self.assertEqual(client.get('/api/v1/coverage').json()['available'], True)
                self.assertEqual(client.get('/miniapp/').status_code, 200)
                module = client.get('/miniapp/app.mjs')
                self.assertEqual(module.status_code, 200)
                self.assertIn('javascript', module.headers['content-type'])
                self.assertEqual(client.get('/miniapp/.env').status_code, 404)
                self.assertEqual(client.get('/backend/data/nodes.parquet').status_code, 404)


if __name__ == '__main__':
    unittest.main()
