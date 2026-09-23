import argparse
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description='Backend и AI-ассистент на одном локальном сайте')
    source = parser.add_mutually_exclusive_group()
    source.add_argument('--output', type=Path, help='Папка опубликованного backend-результата с LATEST')
    source.add_argument('--snapshot', type=Path, help='Отдельный graph snapshot.json; только для проверки агента')
    parser.add_argument('--env-file', type=Path, help='Явный локальный .env, который не попадает в Git')
    parser.add_argument('--port', type=int, default=8000)
    args = parser.parse_args()
    from .config import load_env, enabled
    try:
        if args.env_file:
            load_env(args.env_file)
        from .app import create_app
        app = create_app(args.output, snapshot_path=args.snapshot)
    except (OSError, ValueError):
        parser.exit(2, 'Не удалось прочитать конфигурацию или снимок. Проверьте пути и формат.\n')
    print('Ассистент включён' if enabled() else 'Ассистент отключён: нужны флаг, API-ключ и модель')
    print(f'Откройте http://127.0.0.1:{args.port}/assistant')
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=args.port)


if __name__ == '__main__':
    main()
