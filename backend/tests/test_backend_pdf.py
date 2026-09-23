import json
import tempfile
import unittest
from pathlib import Path

from fastapi.testclient import TestClient
from backend.api import create_app
from backend.pipeline import run_pipeline
from backend.report_pdf import collect_evidence, chronology, render_pdf


class ReportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.addClassCleanup(cls.temp.cleanup)
        cls.output = Path(cls.temp.name)
        assert run_pipeline(Path('missing'), cls.output, Path('missing'), demo=True) == 0
        cls.run_id = (cls.output / 'LATEST').read_text().strip()
        path = cls.output / 'runs' / cls.run_id / 'snapshot.json'
        cls.snapshot = json.loads(path.read_text(encoding='utf-8'))
        cls.ids = [n['gid'] for n in cls.snapshot['nodes'][:4]]
        cls.snapshot['edges'] = [dict(src=cls.ids[a], dst=cls.ids[b], sum_kzt=12345.67, n_tx=2,
                                    first_date=first, last_date=last) for a, b, first, last in [
            (0, 1, '2026-07-20', '2026-07-28'), (1, 2, '2026-07-03', '2026-07-03'),
            (3, 0, '2026-07-01', '2026-07-30')]]
        path.write_text(json.dumps(cls.snapshot), encoding='utf-8')

    def setUp(self):
        self.client = self.enterContext(TestClient(create_app(self.output)))
        self.edge = ':'.join(self.ids[:2])

    def post(self, keys, **extra):
        return self.client.post('/api/v1/export/report.pdf', json={'run_id': self.run_id, 'keys': keys, **extra})

    def test_pdf_download_and_server_facts(self):
        response = self.post(['node:' + self.ids[0], 'edge:' + self.edge])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['content-type'], 'application/pdf')
        self.assertEqual(response.headers['cache-control'], 'no-store')
        self.assertIn(self.run_id + '.pdf', response.headers['content-disposition'])
        self.assertTrue(response.content.startswith(b'%PDF-'))
        self.assertGreater(len(response.content), 10000)  # Embedded Cyrillic font.
        facts = collect_evidence(self.snapshot, ['edge:' + self.edge])[0][1]
        self.assertIn('Наблюдаемая сумма: 12 345,67 ₸', facts)

    def test_stale_missing_and_client_prose_rejected(self):
        self.assertEqual(self.post(['node:' + self.ids[0]], run_id='20000101T000000Z-00000000').status_code, 409)
        for keys in [[], ['node:999'], ['edge:' + ':'.join(reversed(self.ids[:2]))], ['node:' + self.ids[0]] * 31]:
            self.assertEqual(self.post(keys).status_code, 400)
        self.assertEqual(self.post(['node:' + self.ids[0]], facts=['forged amount']).status_code, 400)

    def test_paths_are_directed_contiguous_and_chronology_checked(self):
        path = 'path:' + self.edge + '|' + ':'.join(self.ids[1:3])
        facts = collect_evidence(self.snapshot, [path])[0][1]
        self.assertIn('Хронология не сходится', facts[1])
        self.assertIn('2026-07-20', facts[1])
        for ids in [[self.edge, ':'.join([self.ids[3], self.ids[0]])], [self.edge] * 7]:
            self.assertEqual(self.post(['path:' + '|'.join(ids)]).status_code, 400)
        self.assertIn('не подтверждают', chronology(self.snapshot['edges'][:1]))
        self.assertIn('не хватает дат', chronology([dict(first_date=None, last_date=None)]))

    def test_long_content_markup_and_max_selection_render(self):
        facts = collect_evidence(self.snapshot, ['node:' + n['gid'] for n in self.snapshot['nodes']])
        facts[0][1].append('<script> & <b>не разметка</b> ' * 150)
        self.assertTrue(render_pdf(self.snapshot, facts).startswith(b'%PDF-'))

    def test_duplicate_references_deduplicated(self):
        self.assertEqual(len(collect_evidence(self.snapshot, ['edge:' + self.edge] * 2)), 1)


if __name__ == '__main__':
    unittest.main()
