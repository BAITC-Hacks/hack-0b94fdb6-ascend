import argparse
import os
import time
from .config import Config, ROOT
from .engine import Store
from .transport import Telegram, Backend, ServiceError
from .bot import Bot, COMMANDS


def main():
    parser = argparse.ArgumentParser(description='Freedom Graph — automatic personal Telegram notifications')
    parser.add_argument('--configure', action='store_true', help='Publish bot commands and description, then exit')
    args = parser.parse_args()
    os.umask(0o077)
    config = Config.from_env()
    telegram = Telegram(config.token)
    me = telegram.call('getMe')
    if str(me.get('username', '')).lower() != 'freedomgraphbot':
        raise ValueError('Токен должен относиться к @FreedomGraphbot.')
    if args.configure:
        telegram.call('setMyCommands', commands=COMMANDS)
        telegram.call('setMyDescription', description='Freedom Graph · личный мониторинг новых финансовых связей. Активируйте доступ кодом команды и получайте оповещения автоматически в этом чате. Сигналы требуют проверки и не являются выводом о нарушении.')
        telegram.call('setMyShortDescription', short_description='Freedom Graph · мониторинг новых связей для аналитиков L2')
        if config.miniapp_url:
            telegram.call('setChatMenuButton', menu_button={'type': 'web_app', 'text': 'Freedom Graph', 'web_app': {'url': config.miniapp_url}})
        print('Команды и описание настроены.')
        return
    if telegram.call('getWebhookInfo').get('url'):
        raise ValueError('У бота уже настроен webhook. Остановите существующий обработчик; автоматически он не удаляется.')
    state = ROOT / 'state'
    state.mkdir(mode=0o700, exist_ok=True)
    # OS lock is released after crashes; no unsafe manual lock-file deletion needed.
    import fcntl
    with (state / 'process.lock').open('w') as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise ValueError('Бот уже запущен на этом компьютере.') from None
        store = Store(state / 'bot.sqlite3')
        bot = Bot(config, store, telegram, Backend(config.backend, config.backend_token))
        try:
            next_poll = 0
            print('Бот запущен: личная активация /start → /activate КОД → автоматические оповещения.')
            while True:
                now = time.monotonic()
                if now >= next_poll:
                    print('Проверка снимка:', bot.poll_graph())
                    next_poll = now + config.poll_seconds
                try:
                    bot.deliver()
                    updates = telegram.call('getUpdates', offset=int(store.get('offset', '0')), timeout=10,
                                            allowed_updates=['message', 'callback_query'])
                    for update in updates:
                        try:
                            bot.handle(update)
                        except ServiceError as error:
                            if error.code != 403:
                                raise
                            # A user blocking the bot must not stall all later updates.
                            message = update.get('message', {})
                            uid = message.get('from', {}).get('id')
                            if isinstance(uid, int) and uid > 0:
                                store.subscribe(uid, False)
                        except (KeyError, TypeError, AttributeError):
                            print('Пропущено некорректное обновление Telegram (содержимое скрыто).')
                        with store.db:
                            store.put('offset', update['update_id'] + 1)
                except ServiceError as error:
                    print(str(error))
                    if error.code in {401, 409}:
                        raise ValueError('Проверьте токен и отсутствие другого запущенного обработчика.') from None
                    time.sleep(min(error.retry_after, 30))
        finally:
            store.close()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nБот остановлен. Состояние сохранено.')
    except (ValueError, ServiceError) as error:
        print(str(error))
        raise SystemExit(1)
