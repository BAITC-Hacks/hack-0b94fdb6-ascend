import json
import urllib.error
import urllib.request
import uuid
from pathlib import Path


class ServiceError(Exception):
    """Never include URL, response bodies, tokens or user data in exception text."""
    def __init__(self, service, code=0, retry_after=5):
        super().__init__(f'{service}: запрос не выполнен (код {code}).')
        self.code = code
        try:
            self.retry_after = max(1, min(int(retry_after), 3600))
        except (ValueError, TypeError, OverflowError):
            self.retry_after = 5


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None


def request_json(url, *, data=None, headers=None, service='API', timeout=20):
    request = urllib.request.Request(url, data=data, headers=headers or {})
    try:
        with urllib.request.build_opener(NoRedirect()).open(request, timeout=timeout) as response:
            raw = response.read(32 * 1024 * 1024 + 1)
            if len(raw) > 32 * 1024 * 1024:
                raise ServiceError(service)
            return json.loads(raw)
    except urllib.error.HTTPError as error:
        retry = 5
        if error.code == 429:
            try:
                retry = json.loads(error.read(65536)).get('parameters', {}).get('retry_after', 5)
            except (ValueError, AttributeError):
                pass
        raise ServiceError(service, error.code, retry) from None
    except (OSError, ValueError) as error:
        raise ServiceError(service) from None


class Telegram:
    def __init__(self, token):
        self._base = f'https://api.telegram.org/bot{token}/'

    def call(self, method, **payload):
        result = request_json(self._base + method, data=json.dumps(payload).encode(),
                              headers={'Content-Type': 'application/json'}, service='Telegram', timeout=35)
        if not isinstance(result, dict) or not result.get('ok'):
            raise ServiceError('Telegram', result.get('error_code', 0) if isinstance(result, dict) else 0)
        return result['result']

    def send(self, chat_id, text, keyboard=None):
        return self.call('sendMessage', chat_id=chat_id, text=text, parse_mode='HTML',
                         protect_content=True, link_preview_options={'is_disabled': True},
                         reply_markup=keyboard or {'inline_keyboard': []})

    def welcome(self, chat_id, text, keyboard):
        path = Path(__file__).parent / 'design' / 'assets' / 'brand.png'
        boundary = 'FG' + uuid.uuid4().hex
        fields = {'chat_id': str(chat_id), 'caption': text, 'parse_mode': 'HTML',
                  'protect_content': 'true', 'reply_markup': json.dumps(keyboard)}
        chunks = []
        for key, value in fields.items():
            chunks.append(f'--{boundary}\r\nContent-Disposition: form-data; name="{key}"\r\n\r\n{value}\r\n'.encode())
        chunks.extend([f'--{boundary}\r\nContent-Disposition: form-data; name="photo"; filename="brand.png"\r\nContent-Type: image/png\r\n\r\n'.encode(), path.read_bytes(), f'\r\n--{boundary}--\r\n'.encode()])
        result = request_json(self._base + 'sendPhoto', data=b''.join(chunks),
                              headers={'Content-Type': f'multipart/form-data; boundary={boundary}'}, service='Telegram')
        if not isinstance(result, dict) or not result.get('ok'):
            raise ServiceError('Telegram')


class Backend:
    def __init__(self, base, token=''):
        self.base = base
        self.headers = {'Authorization': f'Bearer {token}'} if token else {}

    def get(self, endpoint):
        return request_json(self.base + '/api/v1/' + endpoint, headers=self.headers, service='Backend')

    def snapshot(self):
        before = self.get('overview')
        graph = self.get('graph')
        after = self.get('overview')
        if not before.get('run_id') or before.get('run_id') != graph.get('run_id') or graph.get('run_id') != after.get('run_id'):
            raise ValueError('Снимок сменился во время чтения. Повторим позже.')
        from .engine import Snapshot
        return Snapshot.parse(graph, after, self.base)
