"""Interactive local launcher; no credentials in arguments or shell history."""
import subprocess
import sys
from .config import ROOT
from .setup import main as setup


def main():
    print('Freedom Graph · запуск личных оповещений', flush=True)
    if not (ROOT / '.env').exists():
        print('Один раз вставьте НОВЫЙ токен из BotFather. Ввод скрыт.', flush=True)
        setup()
    configured = subprocess.run([sys.executable, '-m', 'TelegramBot', '--configure'], cwd=ROOT.parent)
    if configured.returncode:
        print('Настройка Telegram не завершена. Бот не запущен.', flush=True)
        return configured.returncode
    print('Не закрывайте это окно: оно поддерживает работу бота. Остановка: Ctrl+C.', flush=True)
    return subprocess.run([sys.executable, '-u', '-m', 'TelegramBot'], cwd=ROOT.parent).returncode


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print('\nЗапуск остановлен пользователем.')
        raise SystemExit(130)
