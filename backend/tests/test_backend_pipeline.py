import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from backend.demo import analyze
from backend.export import SCHEMAS, gid, validate_csvs, write_csvs
from backend.pipeline import run_pipeline


class PipelineTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parent)
        self.addCleanup(self.temp.cleanup)
        self.output = Path(self.temp.name) / 'output'

    def run_demo(self):
        return run_pipeline(Path('missing'), self.output, Path('missing.yaml'), demo=True)

    def test_deterministic_csv_and_exact_json_gid(self):
        self.assertEqual(self.run_demo(), 0)
        first = {name: (self.output / name).read_bytes() for name in SCHEMAS}
        old_run = (self.output / 'LATEST').read_text().strip()
        self.assertEqual(self.run_demo(), 0)
        for name in SCHEMAS:
            self.assertEqual(first[name], (self.output / name).read_bytes())
        self.assertTrue((self.output / 'runs' / old_run).is_dir())
        current = (self.output / 'LATEST').read_text().strip()
        snapshot = json.loads((self.output / 'runs' / current / 'snapshot.json').read_text(encoding='utf-8'))
        self.assertEqual(snapshot['nodes'][0]['gid'], '900000000000000000')
        self.assertTrue(snapshot['run']['_synthetic'])

    def test_missing_inputs_preserve_published_result(self):
        self.assertEqual(self.run_demo(), 0)
        before = {name: (self.output / name).read_bytes() for name in [*SCHEMAS, 'LATEST']}
        self.assertEqual(run_pipeline(Path('missing'), self.output, Path('missing.yaml')), 2)
        self.assertEqual(before, {name: (self.output / name).read_bytes() for name in before})
        self.assertEqual(json.loads((self.output / 'last_attempt.json').read_text())['status'], 'failed')

    def test_publication_failure_rolls_back(self):
        self.assertEqual(self.run_demo(), 0)
        before = {name: (self.output / name).read_bytes() for name in [*SCHEMAS, 'LATEST']}
        import backend.pipeline as pipeline
        original = pipeline.os.replace
        def fail_latest(src, dst):
            if Path(src).name == 'LATEST.tmp':
                raise OSError('injected publication failure')
            return original(src, dst)
        with patch('backend.pipeline.os.replace', side_effect=fail_latest):
            self.assertEqual(self.run_demo(), 1)
        self.assertEqual(before, {name: (self.output / name).read_bytes() for name in before})

    def test_rejects_corrupt_written_csv(self):
        result = analyze(None, None)
        self.output.mkdir()
        write_csvs(self.output, result.nodes, result.clusters, result.top)
        path = self.output / 'nodes_roles.csv'
        path.write_text(path.read_text(encoding='utf-8').replace('0.3000', 'nan'), encoding='utf-8')
        with self.assertRaises(ValueError):
            validate_csvs(self.output, result.nodes)

    def test_rejects_float_gid(self):
        with self.assertRaises(ValueError):
            gid(900000000000000000.0)

    def test_rejects_boundary_terminal_and_duplicate_gid(self):
        result = analyze(None, None)
        self.output.mkdir()
        result.nodes[0].update(is_boundary=True, role='terminal')
        write_csvs(self.output, result.nodes, result.clusters, result.top)
        with self.assertRaises(ValueError):
            validate_csvs(self.output, result.nodes)
        result = analyze(None, None)
        result.nodes[1]['gid'] = result.nodes[0]['gid']
        write_csvs(self.output, result.nodes, result.clusters, result.top)
        with self.assertRaises(ValueError):
            validate_csvs(self.output, result.nodes)


if __name__ == '__main__':
    unittest.main()
