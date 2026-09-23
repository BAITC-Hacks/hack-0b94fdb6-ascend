"""Cross-platform first launch. Only Python is needed before running this file."""
import argparse
import os
from pathlib import Path
import subprocess
import sys
import venv

ROOT = Path(__file__).resolve().parent


def main():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    if sys.version_info < (3, 11):
        print('Нужен Python 3.11 или новее. Проверенная версия: Python 3.12.', file=sys.stderr)
        return 1
    parser = argparse.ArgumentParser(description='Установка и запуск Freedom Graph для жюри', add_help=False)
    parser.add_argument('--skip-install', action='store_true')
    args, server_args = parser.parse_known_args()
    from backend.jury import check_bundle, main as jury_main
    if '--check' in server_args or '--help' in server_args or '-h' in server_args:
        return jury_main(server_args)
    # Check files before downloading dependencies.
    try:
        check_bundle()
    except (OSError, ValueError, KeyError) as exc:
        print(f'Комплект неполный: {exc}', file=sys.stderr)
        return 1
    environment = ROOT / '.jury-venv'
    python = environment / ('Scripts/python.exe' if os.name == 'nt' else 'bin/python')
    if not python.is_file():
        print('Создаю локальное окружение .jury-venv ...', flush=True)
        venv.EnvBuilder(with_pip=True).create(environment)
    if not args.skip_install:
        print('Устанавливаю зависимости; для первой установки нужен интернет ...', flush=True)
        subprocess.run([str(python), '-m', 'pip', 'install', '--disable-pip-version-check', '--no-cache-dir',
                        '-r', str(ROOT / 'backend/requirements-assistant.txt')], cwd=ROOT, check=True)
    return subprocess.call([str(python), '-m', 'backend.jury', *server_args], cwd=ROOT)


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        pass
    except (OSError, subprocess.CalledProcessError) as exc:
        print(f'Запуск прерван: {exc}\nПроверьте Python, интернет и сообщение установки выше.', file=sys.stderr)
        raise SystemExit(1)
