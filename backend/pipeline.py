"""Stage, validate, and publish immutable analysis runs."""
import hashlib
import importlib
import json
import os
import platform
import shutil
import time
from datetime import datetime, timezone
from pathlib import Path
from .export import SCHEMAS, records, validate_csvs, write_csvs
from .snapshot import write_json, write_snapshot


def checksum(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def atomic_json(path, value):
    staging = path.with_suffix('.json.tmp')
    write_json(staging, value)
    os.replace(staging, path)


def publish(output, staging, run_id):
    """Rollback public files on handled publication errors. LATEST is the commit point."""
    destination = output / 'runs' / run_id
    names = [*SCHEMAS, 'LATEST', 'last_attempt.json']
    previous = {name: (output / name).read_bytes() if (output / name).exists() else None for name in names}
    os.replace(staging, destination)
    try:
        for name in SCHEMAS:
            temp = output / (name + '.tmp')
            shutil.copyfile(destination / name, temp)
            os.replace(temp, output / name)
        atomic_json(output / 'last_attempt.json', {'status': 'succeeded', 'run_id': run_id})
        marker = output / 'LATEST.tmp'
        marker.write_text(run_id + '\n', encoding='utf-8')
        os.replace(marker, output / 'LATEST')
    except Exception:
        for name, content in previous.items():
            target = output / name
            if content is None:
                target.unlink(missing_ok=True)
            else:
                temporary = output / (name + '.rollback')
                temporary.write_bytes(content)
                os.replace(temporary, target)
        raise
    finally:
        for name in names:
            (output / (name + '.tmp')).unlink(missing_ok=True)


def run_pipeline(data_dir: Path, output: Path, config_path: Path, demo=False):
    start = time.perf_counter()
    staging = None
    output.mkdir(parents=True, exist_ok=True)
    # Exclusive publisher prevents two runs from racing over root CSVs and LATEST.
    lock = output / '.pipeline.lock'
    try:
        lock_fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError:
        print('Ошибка: другой pipeline уже работает; проверьте .pipeline.lock')
        return 1
    try:
        checksums = {}
        if demo:
            from .demo import analyze
        else:
            for path in [*(data_dir / name for name in ['nodes.parquet', 'edges.parquet', 'transactions.parquet']), config_path]:
                if not path.is_file():
                    raise FileNotFoundError(f'Нет файла: {path}')
                checksums[path.name] = checksum(path)
            try:
                analyze = importlib.import_module('graph').analyze
            except (ModuleNotFoundError, AttributeError) as exc:
                raise RuntimeError('Graph Engine ещё не подключён: требуется graph.analyze(data_dir, config_path). Для проверки используйте --demo.') from exc
        result = analyze(data_dir, config_path)
        created = datetime.now(timezone.utc)
        digest = hashlib.sha256(json.dumps(checksums, sort_keys=True).encode() + (b'demo' if demo else b'')).hexdigest()[:8]
        run_id = created.strftime('%Y%m%dT%H%M%SZ') + '-' + digest
        runs = output / 'runs'
        runs.mkdir(exist_ok=True)
        # Preserve immutable snapshots if identical inputs are run within the same second.
        while (runs / run_id).exists():
            time.sleep(0.1)
            created = datetime.now(timezone.utc)
            run_id = created.strftime('%Y%m%dT%H%M%SZ') + '-' + digest
        staging = runs / (run_id + '.tmp')
        staging.mkdir()
        run = dict(result.run_meta, run_id=run_id, status='succeeded', created_at=created.isoformat(),
                   input_checksums=checksums, duration_sec=0.0,
                   machine={'os': platform.platform(), 'python': platform.python_version(),
                            'cpu': platform.processor(), 'ram_gb': _ram_gb()})
        write_csvs(staging, result.nodes, result.clusters, result.top)
        source_nodes = records(result.nodes)
        if not demo:
            import pandas as pd
            # Validate coverage against original inputs, not the analyzer's returned set.
            source_nodes = pd.read_parquet(data_dir / 'nodes.parquet').to_dict(orient='records')
            source_nodes = [dict(node, is_boundary=node['depth'] == 4) for node in source_nodes]
        validate_csvs(staging, source_nodes)
        write_snapshot(staging, result, run)
        run['duration_sec'] = round(time.perf_counter() - start, 6)
        write_snapshot(staging, result, run)
        publish(output, staging, run_id)
        print(f"{'ДЕМО: синтетические данные. ' if demo else ''}Готово: {run_id}")
        print(f"Проверки CSV пройдены. Роли: {run.get('role_counts', {})}")
        print(f"Время: {time.perf_counter() - start:.3f} с. Файлы: {output.resolve()}")
        return 0
    except Exception as exc:
        if staging is not None and staging.exists():
            shutil.rmtree(staging)
        atomic_json(output / 'last_attempt.json', {'status': 'failed', 'error': str(exc), 'created_at': datetime.now(timezone.utc).isoformat()})
        print(f'Ошибка: {exc}')
        return 2 if isinstance(exc, FileNotFoundError) or type(exc).__name__ == 'DataValidationError' else 1
    finally:
        os.close(lock_fd)
        lock.unlink(missing_ok=True)


def _ram_gb():
    if os.name == 'nt':
        import ctypes
        class MemoryStatus(ctypes.Structure):
            _fields_ = [('length', ctypes.c_ulong), ('load', ctypes.c_ulong),
                        *[(name, ctypes.c_ulonglong) for name in ['total', 'available', 'page_total', 'page_available', 'virtual_total', 'virtual_available', 'extended']]]
        status = MemoryStatus()
        status.length = ctypes.sizeof(status)
        if ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(status)):
            return round(status.total / 1024**3, 2)
    try:
        return round(os.sysconf('SC_PHYS_PAGES') * os.sysconf('SC_PAGE_SIZE') / 1024**3, 2)
    except (AttributeError, ValueError, OSError):
        return 0.0
