"""Render selected evidence from the server snapshot, never from client prose."""
import io
import re
from html import escape
from pathlib import Path
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, StringConstraints
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import KeepTogether, Paragraph, SimpleDocTemplate, Spacer

pdfmetrics.registerFont(TTFont('Evidence', str(Path(__file__).parent / 'assets/fonts/DejaVuSans.ttf')))
pdfmetrics.registerFontFamily('Evidence', normal='Evidence', bold='Evidence', italic='Evidence', boldItalic='Evidence')

Key = Annotated[str, StringConstraints(min_length=1, max_length=260)]


class ReportRequest(BaseModel):
    model_config = ConfigDict(extra='forbid')
    run_id: str = Field(pattern=r'^[0-9]{8}T[0-9]{6}Z-[0-9a-f]{8}$')
    keys: list[Key] = Field(min_length=1, max_length=30)


LIMITATIONS = [
    'Роли и приоритеты - гипотезы для ручной проверки, а не выводы о виновности.',
    'Связи - агрегированные направленные переводы в наблюдаемом срезе.',
    'Путь показывает структурную достижимость; не доказывает движение одних и тех же денег или последовательность операций во времени.',
    'На границе обхода исходящие связи не прослежены; отсутствие пути не доказывает отсутствие финансовой связи.',
    'Межбанковские операции и переводы ниже порога исходного набора не представлены.',
    'Факты получены из указанного снимка. Отчёт составлен по выбору аналитика, без генерации LLM.',
]


def amount(value):
    return f'{value:,.2f}'.replace(',', ' ').replace('.', ',') + ' ₸'


def edge_facts(edge):
    return [f'Наблюдаемая сумма: {amount(edge["sum_kzt"])}',
            f'Число переводов: {edge["n_tx"]}',
            f'Первый перевод: {edge.get("first_date") or "нет данных"}; последний: {edge.get("last_date") or "нет данных"}']


def chronology(edges):
    if any(not e.get('first_date') or not e.get('last_date') for e in edges):
        return 'Для проверки хронологии не хватает дат. Показана только структура связей.'
    earliest = ''
    for i, edge in enumerate(edges):
        if edge['last_date'] < earliest:
            return (f'Хронология не сходится: на шаге {i + 1} последний перевод был {edge["last_date"]}, '
                    f'а предыдущие шаги требуют даты не раньше {earliest}. Эта цепочка не описывает '
                    'последовательное движение средств в наблюдаемом периоде.')
        earliest = max(earliest, edge['first_date'])
    return ('Диапазоны дат не исключают последовательность. Агрегаты не подтверждают, что по цепочке '
            'прошли одни и те же деньги; нужна проверка отдельных операций.')


def collect_evidence(snapshot, keys):
    """Reject missing/forged references and disconnected or cyclic paths."""
    nodes = {n['gid']: n for n in snapshot['nodes']}
    edges = {e['src'] + ':' + e['dst']: e for e in snapshot['edges']}
    result = []
    for key in dict.fromkeys(keys):
        if re.fullmatch(r'node:[0-9]{1,19}', key) and key[5:] in nodes:
            node = nodes[key[5:]]
            detail = node.get('evidence_detail', node)
            result.append(('Узел ' + node['gid'], [
                f'Роль: {node["role"]}; приоритет: {node["priority_score"]}',
                f'Вход: {amount(node["in_kzt"])}; выход: {amount(node["out_kzt"])}',
                f'Входящих связей: {node["in_deg"]}; исходящих: {node["out_deg"]}',
                'Обоснование: ' + node['evidence'],
                'Правило: ' + detail.get('rule_text', 'нет данных'),
                *detail.get('limitations', []),
            ]))
        elif key.startswith('edge:') and key[5:] in edges:
            edge = edges[key[5:]]
            result.append((f'Связь {edge["src"]} → {edge["dst"]}', edge_facts(edge)))
        elif key.startswith('path:'):
            ids = key[5:].split('|')
            if not 1 <= len(ids) <= 6 or any(i not in edges for i in ids):
                raise ValueError('Цепочка отсутствует в снимке или содержит более 6 связей.')
            path = [edges[i] for i in ids]
            gids = [path[0]['src']] + [e['dst'] for e in path]
            if len(set(gids)) != len(gids) or any(a['dst'] != b['src'] for a, b in zip(path, path[1:])):
                raise ValueError('Указанные связи не образуют направленную цепочку без циклов.')
            facts = [' → '.join(gids), chronology(path)]
            for edge in path:
                facts.extend([f'{edge["src"]} → {edge["dst"]}', *edge_facts(edge)])
            result.append(('Направленная цепочка', facts))
        else:
            raise ValueError('Выбранный факт отсутствует в снимке. Обновите данные и соберите досье заново.')
    return result


def render_pdf(snapshot, evidence):
    stream = io.BytesIO()
    run = snapshot['run']
    run_id = run['run_id']
    doc = SimpleDocTemplate(stream, pagesize=A4, leftMargin=44, rightMargin=44,
                            topMargin=64, bottomMargin=58, title='Freedom Graph - Досье исследования',
                            author='Freedom Graph', pageCompression=1)
    body = ParagraphStyle('body', fontName='Evidence', fontSize=9, leading=14,
                          textColor=colors.HexColor('#28324b'), spaceAfter=7, splitLongWords=True)
    title = ParagraphStyle('title', parent=body, fontSize=22, leading=28, spaceAfter=16,
                           textColor=colors.HexColor('#26194f'))
    heading = ParagraphStyle('heading', parent=body, fontSize=12, leading=18,
                             spaceBefore=14, spaceAfter=8, keepWithNext=True, textColor=colors.HexColor('#4e378b'))
    muted = ParagraphStyle('muted', parent=body, fontSize=8, leading=12, textColor=colors.HexColor('#626c80'))

    def p(text, style=body):
        # Snapshot evidence is text, not ReportLab's XML markup.
        return Paragraph(escape(str(text)).replace('\n', '<br/>'), style)

    story = [p('Досье исследования', title), p('Снимок: ' + run_id, muted),
             p(f'Период: {run["period"]["from"]} - {run["period"]["to"]}', muted),
             p(f'Выбрано фактов: {len(evidence)}', muted), Spacer(1, 8)]
    if run.get('_synthetic'):
        story.append(p('ДЕМО - СИНТЕТИЧЕСКИЕ ДАННЫЕ', heading))
    story.append(p(LIMITATIONS[0]))
    for i, (label, facts) in enumerate(evidence, 1):
        story.append(p(f'{i:02d}. {label}', heading))
        if label == 'Направленная цепочка':
            story.extend(p(fact) for fact in facts[:2])
            for start in range(2, len(facts), 4):
                # Keep each transfer's endpoints, amount and dates on one page.
                story.append(KeepTogether([p(fact) for fact in facts[start:start + 4]]))
        else:
            story.extend(p(fact) for fact in facts)
    story.append(p('Ограничения наблюдения', heading))
    story.extend(p(text) for text in LIMITATIONS[1:])

    def decorate(canvas, _doc):
        canvas.saveState()
        canvas.setStrokeColor(colors.HexColor('#dcd8e8'))
        canvas.line(44, A4[1] - 43, A4[0] - 44, A4[1] - 43)
        canvas.setFont('Evidence', 9)
        canvas.setFillColor(colors.HexColor('#4e378b'))
        canvas.drawString(44, A4[1] - 32, 'FREEDOM GRAPH / ИССЛЕДОВАНИЕ СВЯЗЕЙ')
        canvas.setFont('Evidence', 7)
        canvas.setFillColor(colors.HexColor('#626c80'))
        canvas.drawString(44, 32, run_id)
        canvas.drawRightString(A4[0] - 44, 32, f'Страница {canvas.getPageNumber()}')
        canvas.restoreState()

    doc.build(story, onFirstPage=decorate, onLaterPages=decorate)
    return stream.getvalue()
