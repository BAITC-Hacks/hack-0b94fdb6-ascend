"""Run locally in your terminal. Never sends the token anywhere."""
import getpass
import os
import re
import secrets
import hashlib
from pathlib import Path


def main():
    destination = Path(__file__).parent / '.env'
    if destination.exists():
        raise SystemExit('TelegramBot/.env уже существует. Измените его локально; файл не будет перезаписан.')
    token = getpass.getpass('Новый токен после /revoke (ввод скрыт): ').strip()
    if not re.fullmatch(r'\d+:[A-Za-z0-9_-]{25,}', token):
        raise SystemExit('Некорректный формат токена. Ничего не сохранено.')
    code = secrets.token_urlsafe(24)
    code_hash = hashlib.sha256(code.encode()).hexdigest()
    template = (Path(__file__).parent / '.env.example').read_text()
    content = template.replace('TELEGRAM_BOT_TOKEN=\n', f'TELEGRAM_BOT_TOKEN={token}\n').replace('TEAM_ACCESS_HASH=\n', f'TEAM_ACCESS_HASH={code_hash}\n')
    descriptor = os.open(destination, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(descriptor, 'w') as output:
        output.write(content)
    print('Сохранено локально в TelegramBot/.env. Токен не выводится и исключён из Git.')
    print('Код активации команды (показывается один раз, передайте только коллегам):', code)
    print('В личном чате бота: /start, затем /activate КОД. ID определяется автоматически.')
    print('Далее: python3 -m TelegramBot --configure')


if __name__ == '__main__':
    main()
