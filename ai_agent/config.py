"""Explicit local configuration; never print secrets or execute shell syntax."""
import os
from pathlib import Path

KEYS = {'ASSISTANT_ENABLED', 'OPENAI_API_KEY', 'OPENAI_MODEL'}


def load_env(path):
    # Only an explicitly selected file is read; process environment has precedence.
    values = {}
    for number, line in enumerate(Path(path).read_text(encoding='utf-8-sig').splitlines(), 1):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        key, sep, value = line.partition('=')
        key, value = key.strip(), value.strip()
        if not sep or key not in KEYS:
            raise ValueError(f'Некорректная строка конфигурации {number}; разрешены только {", ".join(sorted(KEYS))}')
        if len(value) >= 2 and value[0] == value[-1] and value[0] in ('"', "'"):
            value = value[1:-1]
        values[key] = value
    for key, value in values.items():
        os.environ.setdefault(key, value)


def enabled():
    return os.getenv('ASSISTANT_ENABLED') == '1' and bool(os.getenv('OPENAI_API_KEY')) and bool(os.getenv('OPENAI_MODEL'))
