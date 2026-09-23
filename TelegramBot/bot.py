import hashlib
import hmac
import time
from html import escape
from .messages import WELCOME, menu, alert, alert_buttons
from .transport import ServiceError

COMMANDS = [
    {'command': 'start', 'description': 'Freedom Graph · начать работу'},
    {'command': 'activate', 'description': 'Активировать личные уведомления кодом команды'},
    {'command': 'status', 'description': 'Состояние моего мониторинга'},
    {'command': 'alerts', 'description': 'Мои последние оповещения'},
    {'command': 'pause', 'description': 'Пауза моих оповещений'},
    {'command': 'resume', 'description': 'Возобновить мои оповещения'},
    {'command': 'stop', 'description': 'Отключить подписку и выйти'},
]


class Bot:
    def __init__(self, config, store, telegram, backend):
        self.config, self.store, self.telegram, self.backend = config, store, telegram, backend
        self.healthy = False
        self.last_success = None
        self.rate_limits = {}

    def authorized(self, uid):
        row = self.store.db.execute('SELECT epoch FROM identities WHERE uid=?', (uid,)).fetchone()
        return bool(row and hmac.compare_digest(row[0], self.config.access_hash))

    def activate(self, uid, code):
        now = time.time()
        row = self.store.db.execute('SELECT count,until FROM attempts WHERE uid=?', (uid,)).fetchone()
        if row and row['count'] >= 5 and row['until'] > now:
            self.telegram.send(uid, '🔒 Слишком много попыток. Повторите через 15 минут.')
            return
        valid = hmac.compare_digest(hashlib.sha256(code.encode()).hexdigest(), self.config.access_hash)
        if not valid:
            count = row['count'] + 1 if row and row['until'] > now else 1
            with self.store.db:
                self.store.db.execute('INSERT OR REPLACE INTO attempts VALUES (?,?,?)', (uid, count, now + 900))
            self.telegram.send(uid, '🔒 Код не принят. Получите код активации у команды.')
            return
        if not self.authorized(uid):
            self.store.subscribe(uid, False)
        with self.store.db:
            self.store.db.execute('INSERT OR REPLACE INTO identities VALUES (?,?)', (uid, self.config.access_hash))
            self.store.db.execute('DELETE FROM attempts WHERE uid=?', (uid,))
        self.store.subscribe(uid, True)
        self.telegram.send(uid, f'🟢 <b>Личный мониторинг активирован</b>\n\nTelegram ID: <code>{uid}</code>\n'
                           'Доступ подтверждён кодом команды. Новые оповещения будут приходить сюда автоматически — '
                           'запрашивать их каждый раз не нужно.\n\n'
                           'Первый снимок — база сравнения. Ожидаем новые изменения, а не рассылаем старые связи.', menu(self.config.dashboard, self.config.miniapp_url))

    def poll_graph(self):
        try:
            allowed = {row[0] for row in self.store.db.execute('SELECT uid FROM identities WHERE epoch=?', (self.config.access_hash,))}
            result = self.store.ingest(self.backend.snapshot(), allowed, self.config.min_priority, self.config.allow_real)
            self.healthy, self.last_success = True, time.time()
            return result
        except (ServiceError, ValueError, KeyError, TypeError, OverflowError, AttributeError):
            self.healthy = False
            return 'unavailable'

    def deliver(self):
        if not self.healthy:
            return
        rows = self.store.db.execute('''SELECT d.event,d.uid FROM deliveries d
          JOIN subscribers s ON s.uid=d.uid JOIN identities i ON i.uid=d.uid
          WHERE d.sent=0 AND s.active=1 AND i.epoch=? AND d.retry_at<=?
          ORDER BY d.rowid LIMIT 10''', (self.config.access_hash, time.time())).fetchall()
        for row in rows:
            uid = row['uid']
            # A previous send in this batch may have disabled a blocked subscriber.
            active = self.store.db.execute('SELECT active FROM subscribers WHERE uid=?', (uid,)).fetchone()
            if not active or not active[0]:
                continue
            event = self.store.event(row['event'])
            try:
                self.telegram.send(uid, alert(event, self.config.include_details), alert_buttons(event, self.config.dashboard))
            except ServiceError as error:
                with self.store.db:
                    self.store.db.execute('UPDATE deliveries SET attempts=attempts+1,retry_at=? WHERE event=? AND uid=?',
                                          (time.time() + max(30, error.retry_after), event['id'], uid))
                if error.code == 403:
                    self.store.subscribe(uid, False)
                if error.code == 401:
                    raise
                if error.code == 429:
                    with self.store.db:
                        self.store.db.execute('UPDATE deliveries SET retry_at=MAX(retry_at,?) WHERE sent=0', (time.time() + error.retry_after,))
                    break
                continue
            with self.store.db:
                self.store.db.execute('UPDATE deliveries SET sent=1 WHERE event=? AND uid=?', (event['id'], uid))

    def status(self, uid):
        row = self.store.db.execute('SELECT active FROM subscribers WHERE uid=?', (uid,)).fetchone()
        mode = 'Включены автоматически' if row and row[0] else 'Пауза'
        source = '✅ Доступен' if self.healthy else '⚠️ Ожидание проверенного снимка'
        checked = time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime(self.last_success)) if self.last_success else 'Ещё не проверен после запуска'
        return (f'📡 <b>Личный мониторинг</b>\n\nОповещения: <b>{mode}</b>\n'
                f'Источник: {source}\nИнтервал: {self.config.poll_seconds} сек.\n'
                f'Последняя проверка: {checked}\n\n'
                'Оповещения появляются после публикации нового снимка backend.\n'
                'GID и суммы: ' + ('включены в конфигурации' if self.config.include_details else 'скрыты'))

    def handle(self, update):
        callback = update.get('callback_query')
        message = callback.get('message', {}) if callback else update.get('message', {})
        sender = callback.get('from', {}) if callback else message.get('from', {})
        chat, uid = message.get('chat', {}), sender.get('id')
        # Identity comes only from Telegram, never from user text or callback data.
        if not isinstance(uid, int) or uid <= 0 or sender.get('is_bot') or chat.get('type') != 'private' or chat.get('id') != uid:
            return
        text = message.get('text', '')
        command = callback.get('data', '') if callback else text.split(' ', 1)[0].split('@', 1)[0].lstrip('/')
        if callback:
            self.telegram.call('answerCallbackQuery', callback_query_id=callback['id'])
        now = time.monotonic()
        if now - self.rate_limits.get(uid, -10) < 1:
            return
        if len(self.rate_limits) > 10000:
            self.rate_limits.clear()
        self.rate_limits[uid] = now
        if command == 'start':
            self.telegram.welcome(uid, WELCOME, menu(self.config.dashboard, self.config.miniapp_url) if self.authorized(uid) else {'inline_keyboard': []})
            return
        if command == 'activate' and not callback:
            code = text.partition(' ')[2].strip()
            if not code:
                self.telegram.send(uid, '🔑 Отправьте /activate КОД из приглашения команды. Токен самого бота сюда вводить нельзя.')
                return
            try:
                self.telegram.call('deleteMessage', chat_id=uid, message_id=message['message_id'])
            except (ServiceError, KeyError):
                pass
            self.activate(uid, code)
            return
        if not self.authorized(uid):
            self.telegram.send(uid, '🔒 Сначала активируйте доступ: /activate КОД. Ваш Telegram ID будет определён автоматически.')
            return
        if command in {'pause', 'resume', 'stop'}:
            self.store.subscribe(uid, command == 'resume')
            if command == 'stop':
                with self.store.db:
                    self.store.db.execute('DELETE FROM identities WHERE uid=?', (uid,))
            self.telegram.send(uid, {'pause': '⏸ Ваши оповещения на паузе. Пропущенные события не будут отправлены задним числом.',
                                      'resume': '▶️ Ваши автоматические оповещения включены.',
                                      'stop': '🔒 Подписка отключена, доступ завершён. Для возврата нужна новая активация.'}[command])
        elif command.startswith('ack:'):
            event_id = command[4:]
            own = self.store.db.execute('SELECT 1 FROM deliveries WHERE event=? AND uid=? AND sent=1', (event_id, uid)).fetchone()
            if own:
                with self.store.db:
                    self.store.db.execute('INSERT OR IGNORE INTO reviews VALUES (?,?)', (event_id, uid))
                self.telegram.send(uid, f'✓ <b>Принято к проверке</b>\n<code>FG-{escape(event_id)}</code>\nВаша отметка сохранена; это не закрытие расследования.')
        elif command == 'status':
            self.telegram.send(uid, self.status(uid), menu(self.config.dashboard, self.config.miniapp_url))
        elif command == 'alerts':
            events = self.store.latest(uid)
            text = '📋 <b>Ваши последние оповещения</b>\n\n' + ('\n'.join(f'• <code>FG-{escape(e["id"])}</code> · {e["count"]} связей' for e in events) if events else 'Доставленных оповещений пока нет.')
            self.telegram.send(uid, text, menu(self.config.dashboard, self.config.miniapp_url))
