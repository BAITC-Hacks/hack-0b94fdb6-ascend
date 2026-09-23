"""Deterministic, explicitly labeled limited assistant with no provider dependency."""
import json
import re
from time import perf_counter
from graph.query import ToolError
from .guard import gids as result_gids
from .report import report


def plan(question):
    q=question.lower();ids=list(dict.fromkeys(re.findall(r'#(\d{1,19})(?!\d)|(?<!\d)(\d{15,19})(?!\d)',q)))
    ids=[a or b for a,b in ids]
    if re.search(r'как зовут|фио|личност|винов|организатор|преступник|игнорируй|измени.{0,20}(роль|score)',q):return [('refuse',{})]
    if re.search(r'методик|порог|формул',q):return [('get_methodology',{})]
    if re.search(r'не хватает|запросить|белые пятна|полнот',q):return [('get_gaps',{'limit':3})]
    if re.search(r'заблок|убрать|что если|устойчив',q):
        n=re.search(r'(?<!\d)(100|50|20|10|5)(?!\d)',q);return [('get_resilience',{'n':int(n[0]) if n else 10})]
    if len(ids)>=2 and re.search(r'путь|как идут',q):return [('find_paths',{'src':ids[0],'dst':ids[1],'max_len':6,'limit':5})]
    if len(ids)>=2 and re.search(r'откуда|источник',q):return [('common_upstream',{'gids':ids[:10],'max_depth':4,'limit':20})]
    if len(ids)>=2 and re.search(r'собира|куда|получает от|общ',q):return [('common_downstream',{'gids':ids[:10],'max_depth':4,'limit':20})]
    if re.search(r'врем|быстр|синхрон|всплеск|2026-07-',q):
        day=re.search(r'2026-07-\d{2}',q)
        if ids or day:return [('get_temporal',{'gid':ids[0] if ids else None,'date':day[0] if day and not ids else None})]
    if ids and re.search(r'цикл|маршрут|цепоч',q):return [('get_routes',{'gid':ids[0],'kind':'both','limit':10})]
    if re.search(r'аномал|дроблен',q):return [('get_anomalies',{'gid':ids[0] if ids else None,'type':None,'limit':20})]
    if re.search(r'границ|обрыв|колено 4',q):return [('get_boundary',{'gid':ids[0] if ids else None})]
    cluster=re.search(r'кластер\s*(\d+)',q)
    if cluster:return [('get_cluster',{'cluster_id':int(cluster[1])})]
    if re.search(r'найди|найти|покажи узлы',q):
        role=next((r for word,r in [('консолид','consolidator'),('распредел','distributor'),('транзит','transit'),('координатор','coordinator')] if word in q),None)
        return [('find_nodes',{'role':role,'limit':10})]
    if re.search(r'топ|главные|первую очередь|кого провер|приоритет|\btop\b|priority|басым',q):
        count=re.search(r'(?<![\d#])([0-9]{1,3})(?![0-9])',q)
        return [('get_top',{'n':max(1,min(20,int(count[1]))) if count else 5})]
    if ids and re.search(r'кому|сосед|контрагент',q):return [('get_neighbors',{'gid':ids[0],'direction':'out' if 'кому' in q else 'both','limit':10,'sort':'sum'})]
    if ids:return [('get_node_card' if re.search(r'справк|карточк',q) else 'get_node',{'gid':g}) for g in ids[:2]]
    return []


def render(facts):
    if not facts:return 'Ассистент работает в ограниченном режиме. Примеры: «Объясни #GID», «Кого проверить первым?», «Каких данных не хватает?».'
    if any('sections' in f for f in facts):
        text='\n\n'.join(f['text'] for f in facts if 'text' in f)
        return text if len(text)<=3500 else text[:3400].rsplit('\n',1)[0]+'\nПолная карточка доступна через API карточки.'
    financial,financial_gids,common=report(facts)
    if financial_gids or common:return financial
    nodes=[f['node'] for f in facts if 'node' in f]
    if nodes:return '\n\n'.join(f"GID: #{n['gid']}\nРоль: {n.get('role','нет данных')}\nОснование: {n.get('evidence','нет данных')}" for n in nodes)
    lines=[]
    labels={'get_gaps':'Запросы данных','items':'Результаты','daily':'Оборот дня','features':'Признаки','counts':'Количество','rates':'Ставки','paths':'Пути','config':'Методика','removed':'Удалённые узлы'}
    def readable(v):
        text=json.dumps(v,ensure_ascii=False,indent=2)
        return re.sub(r'"(\d{15,19})"',r'"#\1"',text)
    for f in facts:
        if f.get('gid'):lines.append('GID: #'+f['gid'])
        if f.get('available') is False:lines.append('Дополнительный анализ недоступен в этом снимке. Перезапустите расчёт с включёнными extras.');continue
        if 'error' in f:lines.append('Запрошенные данные не найдены или параметры неверны. '+str(f['error'].get('message','')));continue
        for key in ('features','daily','items','paths','counts','rates','config','formulas','removed','status'):
            if f.get(key):lines.append(labels.get(key,key)+':\n'+readable(f[key]))
        if f.get('truncated'):lines.append('Показана только часть результатов.')
    text='\n\n'.join(lines) or 'По заданным условиям результатов не найдено.'
    return text if len(text)<=3500 else text[:3400].rsplit('\n',1)[0]+'\nВывод сокращён; уточните узел или фильтр.'


def answer(tools,question,history=None,reason=None,prior_facts=None,prior_trace=None):
    calls=plan(question)
    if not calls and history:
        previous=next((x['content'] for x in reversed(history) if x['role']=='user'), '')
        calls=plan(question+' '+previous)
    if calls and calls[0][0]=='refuse':return dict(answer='Я могу описать только структуру переводов и проверяемые признаки. Личность владельца и юридическую оценку по этому графу установить нельзя. Что проверить дальше: первичные документы и полноту выписок.',gids=[],tool_calls=[],warnings=[],mode='fallback')
    facts=list(prior_facts or []);trace=list(prior_trace or [])
    if facts:calls=[]
    for name,args in calls:
        start=perf_counter();ok=True
        try:r=tools.dispatch(name,args)
        except ToolError as exc:r={'error':{'code':exc.code,'message':str(exc)}};ok=False
        facts.append(r);trace.append(dict(name=name,args=args,ok=ok,ms=round((perf_counter()-start)*1000,3)))
    text=render(facts)
    if 'Что проверить дальше' not in text:text+='\n\nЧто проверить дальше: сверить основания и ограничения с карточкой узла и первичными выписками.'
    allowed=result_gids(facts)&set(tools.nodes)
    cited=set(re.findall(r'#(\d{1,19})(?!\d)',text))&allowed
    return dict(answer=text,gids=sorted(cited,key=int),tool_calls=trace,warnings=[reason] if reason else [],mode='fallback')
