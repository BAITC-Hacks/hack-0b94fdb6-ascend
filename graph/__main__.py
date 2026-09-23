"""Standalone handoff verification/export. Production publication belongs to backend."""
import argparse
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import sys
from . import analyze, DEFAULT_CONFIG, DataValidationError
from .serialization import snapshot, json_value


def csv_payloads(result):
    nodes = result.nodes.sort_values(['priority_score', 'gid'], ascending=[False, True])[
        ['gid', 'role', 'role_score', 'cluster_id', 'priority_score', 'evidence']].copy()
    nodes['role_score'] = nodes.role_score.map(lambda x: f'{x:.4f}')
    nodes['priority_score'] = nodes.priority_score.map(lambda x: f'{x:.6f}')
    clusters = result.clusters.sort_values('cluster_id')[
        ['cluster_id', 'n_nodes', 'n_seed', 'sum_kzt_internal', 'top_gids', 'hypothesis']].copy()
    clusters['top_gids'] = clusters.top_gids.map(';'.join)
    clusters['sum_kzt_internal'] = clusters.sum_kzt_internal.map(lambda x: f'{x:.2f}')
    top = result.top.head(result.run_meta['config']['top_n']).copy()
    top['priority_score'] = top.priority_score.map(lambda x: f'{x:.6f}')
    return {name: df.to_csv(index=False, lineterminator='\n').encode('utf-8') for name, df in
            [('nodes_roles.csv', nodes), ('clusters.csv', clusters), ('top_nodes.csv', top)]}


def main():
    parser = argparse.ArgumentParser(description='Проверка Graph Engine и отдельная выгрузка для передачи backend')
    parser.add_argument('--data', required=True, type=Path)
    parser.add_argument('--config', type=Path, default=DEFAULT_CONFIG)
    parser.add_argument('--output', type=Path, help='Новая папка; существующий результат не перезаписывается')
    parser.add_argument('--verify-repeat', action='store_true')
    args = parser.parse_args()
    try:
        result = analyze(args.data, args.config)
        payloads = csv_payloads(result)
        if args.verify_repeat:
            other = analyze(args.data, args.config)
            import pandas as pd
            for name in ('nodes', 'edges', 'clusters', 'top'):
                pd.testing.assert_frame_equal(getattr(result, name), getattr(other, name))
            from .extras.export import payload
            if payload(result.extras) != payload(other.extras):
                raise RuntimeError('Повторный расчёт extras дал другой результат')
            if payloads != csv_payloads(other):
                raise RuntimeError('Повторный расчёт дал другие CSV')
        if args.output:
            if args.output.exists():
                raise ValueError('Папка --output уже существует; выберите новую папку')
            timestamp = datetime.now(timezone.utc)
            digest = sha256(json.dumps({'inputs': result.run_meta['input_checksums'], 'config': result.run_meta['config']}, sort_keys=True).encode()).hexdigest()[:8]
            run = dict(result.run_meta, run_id=timestamp.strftime('%Y%m%dT%H%M%SZ') + '-' + digest,
                       status='succeeded', created_at=timestamp.isoformat())
            jsons = {'snapshot.json': snapshot(result, run), 'run.json': run, 'quality_report.json': result.quality}
            payloads.update({name: json.dumps(json_value(value), ensure_ascii=False, allow_nan=False, indent=2).encode('utf-8') for name, value in jsons.items()})
            # Each new standalone export appears only once all files are ready.
            import tempfile
            import shutil
            args.output.parent.mkdir(parents=True, exist_ok=True)
            temporary = Path(tempfile.mkdtemp(prefix='.graph-', dir=args.output.parent))
            try:
                for name, content in payloads.items():
                    (temporary / name).write_bytes(content)
                from .extras.export import write
                write(temporary, result.extras)
                temporary.rename(args.output)
            finally:
                if temporary.exists():
                    shutil.rmtree(temporary)
        print(json.dumps({'counts': result.run_meta['counts'], 'role_counts': result.run_meta['role_counts'],
                          'duration_sec': result.run_meta['duration_sec'], 'repeat_verified': args.verify_repeat,
                          'warnings': result.quality['warnings']}, ensure_ascii=True, indent=2))
        return 0
    except DataValidationError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    except Exception as exc:
        print(f'Ошибка расчёта: {exc}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
