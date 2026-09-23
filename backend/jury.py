"""Run the shipped case snapshot without local output, secrets or recalculation."""
import argparse
import hashlib
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def check_bundle(root=ROOT):
    """Fail early on missing artifacts or inputs from a different case."""
    root = Path(root)
    output = root / 'backend/jury_snapshot'
    run_id = (output / 'LATEST').read_text(encoding='utf-8').strip()
    if not re.fullmatch(r'[0-9]{8}T[0-9]{6}Z-[0-9a-f]{8}', run_id):
        raise ValueError('Некорректный backend/jury_snapshot/LATEST')
    directory = output / 'runs' / run_id
    data = json.loads((directory / 'snapshot.json').read_text(encoding='utf-8'))
    run = data['run']
    if run['run_id'] != run_id or run['status'] != 'succeeded':
        raise ValueError('Снимок не соответствует успешному запуску в LATEST')
    for table in ['nodes', 'edges', 'clusters']:
        if len(data[table]) != run['counts'][table]:
            raise ValueError(f'Неполный снимок: {table}')
    for name in ['nodes.parquet', 'edges.parquet', 'transactions.parquet']:
        path = root / 'backend/data' / name
        if hashlib.sha256(path.read_bytes()).hexdigest() != run['input_checksums'][name]:
            raise ValueError(f'{name} не соответствует готовому расчёту')
    required = [directory / name for name in [
        'run.json', 'quality_report.json', 'nodes_roles.csv', 'clusters.csv', 'top_nodes.csv',
        'extras/coverage.json', 'extras/anomalies.csv', 'extras/chains.csv', 'extras/cycles.csv',
    ]]
    required += [root / 'backend/assets/fonts/DejaVuSans.ttf']
    mini = root / 'TelegramBot/miniapp'
    required += [mini / name for name in [
        'index.html', 'app.mjs', 'data.mjs', 'icons.mjs', 'i18n.mjs', 'styles.css', 'assets/mark.svg',
    ]]
    dist = root / 'Frontend/dist'
    html = (dist / 'index.html').read_text(encoding='utf-8')
    assets = re.findall(r'(?:src|href)=[\"\'](/assets/[^\"\']+)[\"\']', html)
    if not assets:
        raise ValueError('Frontend/dist/index.html не содержит готовую сборку сайта')
    required += [dist / asset.lstrip('/') for asset in assets]
    for path in required:
        if not path.is_file() or path.stat().st_size == 0:
            raise ValueError(f'Не хватает файла: {path.relative_to(root)}')
    return run


def main(argv=None):
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    parser = argparse.ArgumentParser(description='Freedom Graph: комплект для жюри')
    parser.add_argument('--host', default='127.0.0.1')
    parser.add_argument('--port', type=int, default=int(os.getenv('PORT', '8000')))
    parser.add_argument('--with-ai', action='store_true', help='Включить OpenAI по настройкам backend/.env или окружения')
    parser.add_argument('--check', action='store_true', help='Проверить комплект, не запускать сервер')
    args = parser.parse_args(argv)
    try:
        run = check_bundle()
    except (OSError, ValueError, KeyError) as exc:
        print(f'Комплект неполный: {exc}\nОбновите или заново скачайте весь репозиторий.', file=sys.stderr)
        return 1
    counts = run['counts']
    print(f"Комплект проверен: {counts['nodes']} узлов, {counts['edges']} связей, "
          f"{counts['transactions']} транзакций. Снимок {run['run_id']}.", flush=True)
    if args.check:
        return 0
    if args.with_ai:
        from dotenv import load_dotenv
        load_dotenv(ROOT / 'backend/.env', override=False)
    # A personal OUTPUT_DIR or .env must never silently replace the shipped case.
    os.environ['OUTPUT_DIR'] = str(ROOT / 'backend/jury_snapshot')
    os.environ['ASSISTANT_ENABLED'] = '1' if args.with_ai else '0'
    print('OpenAI: включён при наличии ключа и модели.' if args.with_ai else
          'Помощник: локальный режим по правилам; внешние AI-запросы выключены.', flush=True)
    print(f'Сайт: http://127.0.0.1:{args.port}/ | Mini App: http://127.0.0.1:{args.port}/miniapp/', flush=True)
    import uvicorn
    uvicorn.run('backend.api:app', host=args.host, port=args.port)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
