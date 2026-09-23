from html import escape

WELCOME = ('🟢 <b>FREEDOM GRAPH</b>\n'
           '<b>Мониторинг новых связей · L2</b>\n\n'
           'После активации оповещения приходят автоматически сюда, в ваш личный чат. '
           'Первый снимок становится базой — существующие связи не создают тревоги.\n\n'
           'Для первого входа отправьте /activate КОД, полученный у команды. '
           'Telegram ID определяется автоматически.\n\n'
           '🔎 Новая связь — повод для проверки, а не вывод о нарушении.')


def menu(dashboard='', miniapp_url=''):
    rows = [[{'text': '📡 Статус', 'callback_data': 'status'}, {'text': '📋 Последние', 'callback_data': 'alerts'}],
            [{'text': '⏸ Пауза', 'callback_data': 'pause'}, {'text': '▶ Возобновить', 'callback_data': 'resume'}]]
    if dashboard:
        rows.append([{'text': '↗ Открыть MoneyGraph', 'url': dashboard}])
    if miniapp_url:
        rows.insert(0, [{'text': 'Открыть Freedom Graph · Mini App', 'web_app': {'url': miniapp_url}}])
    return {'inline_keyboard': rows}


def alert(event, details=False):
    score = event['priority']
    symbol = '🔴' if score >= .9 else '🟠' if score >= .75 else '🟡' if score >= .6 else '🟢' if score >= .5 else '🔵'
    heading = '🧪 <b>ДЕМО · СИНТЕТИЧЕСКИЕ ДАННЫЕ</b>\n\n' if event['synthetic'] else ''
    text = (f'{heading}{symbol} <b>Новые связи для проверки</b>\n'
            f'<b>Freedom Graph · Аналитика L2</b>\n\n'
            f'Связей в уведомлении: <b>{event["count"]}</b>\n'
            f'Всего новых в снимке: <b>{event["total_new"]}</b>\n'
            f'Макс. приоритет узла: <b>{round(score * 100)}/100</b>\n\n'
            '<b>Что изменилось</b>\n'
            'В опубликованном графе появились пары «плательщик → получатель», '
            'которые ранее не наблюдались в текущем периоде и методологии.\n')
    if details:
        text += '\n<b>Примеры направленных связей</b>\n'
        for edge in event['samples']:
            text += f'<code>{escape(edge["src"])} → {escape(edge["dst"])}</code>\n'
            text += f'Объём в снимке: {edge["sum_kzt"]:,.2f} ₸\n'
        if event['count'] > len(event['samples']):
            text += f'Ещё связей: {event["count"] - len(event["samples"])}\n'
    else:
        text += '\n🔒 GID и суммы не передаются в Telegram.\n'
    text += ('\n<b>Следующий шаг</b>\nПроверьте связь и контекст в системе банка. '
             'Изменение графа само по себе не подтверждает нарушение.\n\n'
             f'<code>FG-{escape(event["id"])}</code>\n'
             f'<i>Период: {escape(event["period"]["from"])} — {escape(event["period"]["to"])}</i>')
    return text


def alert_buttons(event, dashboard=''):
    rows = [[{'text': '✓ Принято к проверке', 'callback_data': 'ack:' + event['id']}]]
    if dashboard:
        rows.append([{'text': '↗ Открыть MoneyGraph', 'url': dashboard}])
    return {'inline_keyboard': rows}
