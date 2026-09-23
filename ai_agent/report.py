"""Render financial facts directly from tool outputs; never from model prose."""
from decimal import Decimal


def amount(value):
    if value is None:
        return 'нет данных'
    return format(Decimal(str(value)), ',f').rstrip('0').rstrip('.') if '.' in str(value) else format(int(value), ',')


def report(facts):
    blocks, nodes, common = [], [], False
    for fact in facts:
        if 'requested_sources' in fact:
            common = True
            total, depth = fact['requested_sources'], fact['max_depth']
            if fact['exact_intersection']:
                blocks.append(f'Найдены общие достижимые узлы для всех {total} источников в пределах {depth} шагов.')
            else:
                blocks.append(f'Общего достижимого узла для всех {total} источников в пределах {depth} шагов не найдено. Ниже — только частичные совпадения; это не общий получатель всей группы.')
            blocks.append(fact['limitation'])
            for item in fact['items'][:3]:
                nodes.append((item['node'], f"Достижим из {item['matched_sources']} из {total} источников. Суммы ниже — весь оборот узла, не сумма переводов от этой группы."))
        elif 'node' in fact:
            nodes.append((fact['node'], ''))
        elif 'items' in fact:
            for item in fact['items'][:3]:
                nodes.append((item.get('node', item), ''))
        elif 'nodes' in fact:
            nodes.extend((n, '') for n in fact['nodes'][:3])
        if fact.get('truncated'):
            blocks.append('Выдача ограничена: показана только часть результатов.')
    seen = set()
    for node, context in nodes:
        gid = node.get('gid')
        if gid in seen or gid is None or 'in_kzt' not in node or 'out_kzt' not in node:
            continue
        if len(seen) >= 3:
            break
        seen.add(gid)
        text = (f"GID: #{gid}\nРоль: {node.get('role', 'нет данных')}\n"
                f"Вход: {amount(node['in_kzt'])} ₸; выход: {amount(node['out_kzt'])} ₸.\n"
                f"Отправителей: {node.get('in_deg', 'нет данных')}; получателей: {node.get('out_deg', 'нет данных')}.\n"
                f"Соответствие роли: {node.get('role_score', 'нет данных')}; приоритет: {node.get('priority_score', 'нет данных')}.\n"
                f"Основание: {str(node.get('evidence', 'Объяснение роли в снимке отсутствует.'))[:500]}\n" + context)
        blocks.append(text.strip())
    if seen:
        if len({n.get('gid') for n, _ in nodes}) > len(seen):
            blocks.append('В ответе показаны первые три финансовые карточки из полученных результатов.')
        blocks.append('Ограничения: анализ наблюдаемого среза, а не всей финансовой деятельности. Роли — гипотезы; внешние поступления и продолжение цепочек могут отсутствовать в данных.')
    return '\n\n'.join(dict.fromkeys(blocks)), seen, common
