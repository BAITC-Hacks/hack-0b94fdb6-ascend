import hashlib
import os
import tempfile
import unittest
import ssl
from dataclasses import replace
from pathlib import Path
from .bot import Bot
from .config import Config, safe_url
from .demo import snapshot, OfflineBackend, OfflineTelegram
from .engine import Store
from .messages import alert, WELCOME, menu
from .transport import ServiceError, tls_context

A, B, C = ('100000000000000001', '100000000000000002', '100000000000000003')


class BotTests(unittest.TestCase):
    def setUp(self):
        self.store = Store(':memory:')
        self.addCleanup(self.store.close)
        self.telegram, self.backend = OfflineTelegram(), OfflineBackend()
        self.config = Config('offline-not-a-token', hashlib.sha256(b'test-code').hexdigest())
        self.bot = Bot(self.config, self.store, self.telegram, self.backend)

    def command(self, uid, text, **chat):
        self.bot.rate_limits.clear()
        self.bot.handle({'message': {'message_id': 1, 'from': {'id': uid},
                                    'chat': {'id': uid, 'type': 'private', **chat}, 'text': text}})

    def activate(self, uid=101):
        self.command(uid, '/activate test-code')
        self.telegram.messages.clear()

    def new_event(self):
        self.bot.poll_graph()
        self.backend.value = snapshot('new', [(A, B), (B, C)], day=2)
        return self.bot.poll_graph()

    def test_start_requires_activation(self):
        self.command(101, '/start')
        self.assertIn('/activate', self.telegram.messages[-1][1])
        self.assertFalse(self.bot.authorized(101))

    def test_public_navigation_does_not_expose_monitoring_actions(self):
        self.bot.config = replace(self.config, dashboard='https://example.com', miniapp_url='https://mini.example.com')
        self.command(101, '/start')
        buttons = [b for row in self.telegram.messages[-1][2]['inline_keyboard'] for b in row]
        self.assertTrue(any(b.get('url') == 'https://example.com' for b in buttons))
        self.assertTrue(any(b.get('web_app', {}).get('url') == 'https://mini.example.com' for b in buttons))
        self.assertFalse(any('callback_data' in b for b in buttons))
        self.assertFalse(self.bot.authorized(101))

    def test_no_site_link_until_published(self):
        self.assertEqual(menu(authenticated=False), {'inline_keyboard': []})

    def test_identity_and_personal_automatic_delivery(self):
        self.activate(101); self.activate(202)
        self.assertEqual(self.new_event(), 'new:1')
        self.bot.deliver()
        self.assertEqual([m[0] for m in self.telegram.messages], [101, 202])
        self.assertEqual(len(self.store.latest(101)), 1)
        self.assertEqual(self.store.latest(303), [])

    def test_first_snapshot_silent_and_repeat_dedup(self):
        self.activate()
        self.assertEqual(self.bot.poll_graph(), 'baseline')
        self.bot.deliver(); self.assertEqual(self.telegram.messages, [])
        self.new_event(); self.bot.deliver()
        self.assertEqual(self.bot.poll_graph(), 'unchanged')
        self.bot.deliver(); self.assertEqual(len(self.telegram.messages), 1)

    def test_invalid_code_and_lockout(self):
        for _ in range(5):
            self.command(101, '/activate wrong')
        self.command(101, '/activate test-code')
        self.assertFalse(self.bot.authorized(101))
        self.assertIn('15 минут', self.telegram.messages[-1][1])

    def test_no_group_or_spoofed_identity(self):
        self.command(101, '/activate test-code', id=-10, type='supergroup')
        self.command(101, '/activate test-code', id=202)
        self.assertEqual(self.telegram.messages, [])
        self.assertFalse(self.bot.authorized(101))

    def test_pause_is_personal(self):
        self.activate(101); self.activate(202)
        self.command(101, '/pause'); self.telegram.messages.clear()
        self.new_event(); self.bot.deliver()
        self.assertEqual([m[0] for m in self.telegram.messages], [202])
        self.command(101, '/resume'); self.telegram.messages.clear()
        self.bot.deliver(); self.assertEqual(self.telegram.messages, [])

    def test_stop_revokes_resume(self):
        self.activate(); self.command(101, '/stop'); self.command(101, '/resume')
        self.assertFalse(self.bot.authorized(101))
        self.assertIn('Сначала активируйте', self.telegram.messages[-1][1])

    def test_code_rotation_blocks_old_sessions_and_pending(self):
        self.activate(); self.new_event()
        self.bot.config = replace(self.config, access_hash='0' * 64)
        self.assertFalse(self.bot.authorized(101))
        self.bot.deliver(); self.assertEqual(self.telegram.messages, [])

    def test_new_subscriber_no_historical_delivery(self):
        self.new_event(); self.activate(); self.bot.deliver()
        self.assertEqual(self.telegram.messages, [])

    def test_unavailable_source_holds_pending(self):
        self.activate(); self.new_event()
        self.backend.value = ServiceError('Backend')
        self.assertEqual(self.bot.poll_graph(), 'unavailable')
        self.bot.deliver(); self.assertEqual(self.telegram.messages, [])
        self.assertEqual(self.store.get('run'), 'new')

    def test_transient_failure_keeps_outbox(self):
        self.activate(); self.new_event()
        self.telegram.failure = ServiceError('Telegram', 429, 60)
        self.bot.deliver()
        row = self.store.db.execute('SELECT * FROM deliveries').fetchone()
        self.assertEqual(row['sent'], 0); self.assertEqual(row['attempts'], 1)
        self.telegram.failure = None
        with self.store.db:
            self.store.db.execute('UPDATE deliveries SET retry_at=0')
        self.bot.deliver(); self.assertEqual(len(self.telegram.messages), 1)

    def test_blocked_user_paused(self):
        self.activate(); self.new_event()
        self.telegram.failure = ServiceError('Telegram', 403)
        self.bot.deliver()
        self.assertEqual(self.store.db.execute('SELECT active FROM subscribers').fetchone()[0], 0)

    def test_redacted_by_default(self):
        self.activate(); self.new_event(); self.bot.deliver()
        text = self.telegram.messages[-1][1]
        for gid in (A, B, C):
            self.assertNotIn(gid, text)
        self.assertIn('СИНТЕТИЧЕСКИЕ', text)
        self.assertLess(len(text), 4096)
        self.assertLess(len(WELCOME), 1024)
        self.assertIn(B, alert(self.store.latest(101)[0], details=True))

    def test_ack_only_own_delivered_event(self):
        self.activate(101); self.new_event(); self.bot.deliver(); self.activate(202)
        event = self.store.latest(101)[0]['id']
        self.command(202, '/ack:' + event)
        self.assertEqual(self.store.db.execute('SELECT COUNT(*) FROM reviews').fetchone()[0], 0)
        self.command(101, '/ack:' + event)
        self.assertEqual(self.store.db.execute('SELECT COUNT(*) FROM reviews').fetchone()[0], 1)

    def test_real_data_disabled(self):
        self.backend.value = snapshot(synthetic=False)
        self.assertEqual(self.bot.poll_graph(), 'unavailable')
        self.assertEqual(self.store.get('run'), '')

    def test_mutated_run_and_rollback_rejected(self):
        self.bot.poll_graph()
        self.backend.value = snapshot(pairs=[(A, C)])
        self.assertEqual(self.bot.poll_graph(), 'unavailable')
        self.backend.value = snapshot('second', day=2); self.bot.poll_graph()
        self.backend.value = snapshot()
        self.assertEqual(self.bot.poll_graph(), 'unavailable')
        self.assertEqual(self.store.get('run'), 'second')

    def test_scope_change_silent_baseline(self):
        self.activate(); self.bot.poll_graph()
        self.backend.value = snapshot('second', [(A, C)], day=2, period={'from': '2026-08-01', 'to': '2026-08-31'})
        self.assertEqual(self.bot.poll_graph(), 'baseline')
        self.bot.deliver(); self.assertEqual(self.telegram.messages, [])

    def test_direction_and_reappearing_edges(self):
        self.bot.poll_graph()
        self.backend.value = snapshot('second', [(B, A)], day=2)
        self.assertEqual(self.bot.poll_graph(), 'new:1')
        self.backend.value = snapshot('third', [(A, B), (B, A)], day=3)
        self.assertEqual(self.bot.poll_graph(), 'new:0')

    def test_threshold_filters_events(self):
        self.bot.config = replace(self.config, min_priority=.8)
        self.assertEqual(self.new_event(), 'new:0')

    def test_restart_persists_identity_and_outbox(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'bot.sqlite3'
            store = Store(path)
            bot = Bot(self.config, store, self.telegram, self.backend)
            bot.activate(101, 'test-code'); bot.poll_graph()
            self.backend.value = snapshot('second', [(B, C)], day=2); bot.poll_graph()
            store.close()
            store = Store(path)
            try:
                bot = Bot(self.config, store, self.telegram, self.backend)
                self.assertTrue(bot.authorized(101))
                self.telegram.messages.clear(); bot.poll_graph(); bot.deliver()
                self.assertEqual(len(self.telegram.messages), 1)
                if os.name != 'nt':  # Windows uses ACLs, not POSIX permission bits.
                    self.assertEqual(path.stat().st_mode & 0o777, 0o600)
            finally:
                store.close()

    def test_urls_and_sanitized_error(self):
        for url in ('http://example.com', 'https://x.test/?token=secret', 'https://user:secret@x.test'):
            with self.assertRaises(ValueError):
                safe_url(url)
        self.assertEqual(safe_url('http://127.0.0.1:8000/'), 'http://127.0.0.1:8000')
        self.assertEqual(ServiceError('Telegram', 429, None).retry_after, 5)

    def test_tls_keeps_certificate_and_hostname_verification(self):
        context = tls_context()
        self.assertTrue(context.check_hostname)
        self.assertEqual(context.verify_mode, ssl.CERT_REQUIRED)

    def test_miniapp_is_optional_and_uses_web_app_button(self):
        self.assertFalse(any('web_app' in button for row in menu()['inline_keyboard'] for button in row))
        button = menu(miniapp_url='https://example.com/miniapp')['inline_keyboard'][0][0]
        self.assertEqual(button['web_app']['url'], 'https://example.com/miniapp')
        for value in ('http://127.0.0.1:5175', 'http://example.com', 'https://example.com/?token=secret'):
            with self.assertRaises(ValueError):
                safe_url(value, public=True)


if __name__ == '__main__':
    unittest.main()
