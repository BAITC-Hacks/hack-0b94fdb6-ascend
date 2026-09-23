import os
import re
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent


def load_env(path=ROOT / '.env'):
    if not path.exists():
        return
    for line in path.read_text(encoding='utf-8').splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        key, separator, value = line.partition('=')
        if not separator or not re.fullmatch(r'[A-Z_]+', key):
            raise ValueError('Некорректная строка в TelegramBot/.env')
        os.environ.setdefault(key, value.strip())


def safe_url(value, *, public=False):
    parts = urlsplit(value)
    local = parts.hostname in {'127.0.0.1', 'localhost', '::1'}
    if (not parts.hostname or parts.username or parts.password or parts.query or parts.fragment
            or parts.scheme not in {'http', 'https'} or (parts.scheme != 'https' and (public or not local))):
        raise ValueError('Нужен HTTPS URL без пароля/параметров; HTTP разрешён только для локального backend.')
    return value.rstrip('/')


@dataclass(frozen=True)
class Config:
    token: str = field(repr=False)
    access_hash: str = field(repr=False)
    backend: str = 'http://127.0.0.1:8000'
    backend_token: str = field(default='', repr=False)
    dashboard: str = ''
    poll_seconds: int = 60
    min_priority: float = 0
    allow_real: bool = False
    include_details: bool = False
    miniapp_url: str = ''

    @classmethod
    def from_env(cls):
        load_env()
        token = os.getenv('TELEGRAM_BOT_TOKEN', '')
        if not re.fullmatch(r'\d+:[A-Za-z0-9_-]{25,}', token):
            raise ValueError('Сначала сохраните новый токен локально через TelegramBot/setup.py.')
        access_hash = os.getenv('TEAM_ACCESS_HASH', '')
        if not re.fullmatch(r'[a-f0-9]{64}', access_hash):
            raise ValueError('Настройте код активации команды через TelegramBot/setup.py.')
        interval = int(os.getenv('POLL_SECONDS', '60'))
        priority = float(os.getenv('MIN_PRIORITY', '0'))
        if not 15 <= interval <= 3600 or not 0 <= priority <= 1:
            raise ValueError('POLL_SECONDS: 15–3600; MIN_PRIORITY: 0–1.')
        dashboard = os.getenv('DASHBOARD_URL', '')
        miniapp = os.getenv('MINIAPP_URL', '')
        return cls(token, access_hash, safe_url(os.getenv('BACKEND_URL', 'http://127.0.0.1:8000')),
                   os.getenv('BACKEND_API_TOKEN', ''), safe_url(dashboard, public=True) if dashboard else '',
                   interval, priority, os.getenv('ALLOW_REAL_DATA') == '1', os.getenv('INCLUDE_CLIENT_DETAILS') == '1',
                   safe_url(miniapp, public=True) if miniapp else '')
