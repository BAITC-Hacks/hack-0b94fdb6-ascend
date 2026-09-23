"""Offline smoke demonstration. No token, backend or Telegram connection."""
import hashlib
from .bot import Bot
from .config import Config
from .engine import Snapshot, Store


def snapshot(run='demo-1', pairs=None, day=1, synthetic=True, period=None, source='offline'):
    pairs = [('100000000000000001', '100000000000000002')] if pairs is None else pairs
    graph = {'run_id': run, 'nodes': [
        {'gid': '100000000000000001', 'priority_score': .94},
        {'gid': '100000000000000002', 'priority_score': .6},
        {'gid': '100000000000000003', 'priority_score': .3}],
        'edges': [{'src': src, 'dst': dst, 'sum_kzt': 1000} for src, dst in pairs]}
    overview = {'run_id': run, 'status': 'succeeded', 'created_at': f'2026-09-{day:02d}T10:00:00Z',
                'period': period or {'from': '2026-07-01', 'to': '2026-07-31'},
                'methodology_version': 'demo-v1', '_synthetic': synthetic,
                'counts': {'nodes': 3, 'edges': len(pairs)}}
    return Snapshot.parse(graph, overview, source)


class OfflineTelegram:
    def __init__(self):
        self.messages, self.calls = [], []
        self.failure = None

    def call(self, method, **payload):
        self.calls.append((method, payload))
        return True

    def send(self, uid, text, keyboard=None):
        if self.failure:
            raise self.failure
        self.messages.append((uid, text, keyboard))

    def welcome(self, uid, text, keyboard):
        self.send(uid, text, keyboard)


class OfflineBackend:
    def __init__(self):
        self.value = snapshot()

    def snapshot(self):
        if isinstance(self.value, Exception):
            raise self.value
        return self.value


def main():
    store, telegram, backend = Store(':memory:'), OfflineTelegram(), OfflineBackend()
    bot = Bot(Config('offline-not-a-token', hashlib.sha256(b'demo-code').hexdigest()), store, telegram, backend)
    try:
        bot.activate(101, 'demo-code')
        telegram.messages.clear()
        assert bot.poll_graph() == 'baseline'
        bot.deliver()
        assert not telegram.messages
        backend.value = snapshot('demo-2', [('100000000000000001', '100000000000000002'),
                                           ('100000000000000002', '100000000000000003')], day=2)
        assert bot.poll_graph() == 'new:1'
        bot.deliver()
        assert len(telegram.messages) == 1
        bot.poll_graph(); bot.deliver()
        assert len(telegram.messages) == 1
        print('OFFLINE DEMO: активация → базовый снимок → новая связь → одно личное оповещение.')
        print('Запросов в сеть: 0. Повторов при неизменном снимке: 0.\n')
        print(telegram.messages[0][1])
    finally:
        store.close()


if __name__ == '__main__':
    main()
