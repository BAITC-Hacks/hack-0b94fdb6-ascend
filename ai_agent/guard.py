"""Post-check identifiers and approximate financial numbers; not a semantic proof."""
import json
import re
from decimal import Decimal

FORBIDDEN=re.compile(r'организатор|преступник|виновен|наркоторговец|отмывание доказано',re.I)

def gids(value):
    found=set()
    if isinstance(value,dict):
        for k,v in value.items():
            if k in ('gid','src','dst','a','b','c','counterparty_gid') and isinstance(v,str):found.add(v)
            elif k in ('gids','top_gids','reached_by','path'):
                if isinstance(v,list):found.update(x for x in v if isinstance(x,str))
                elif isinstance(v,str):found.update(re.findall(r'\d{15,19}',v))
            else:found.update(gids(v))
    elif isinstance(value,list):
        for v in value:found.update(gids(v))
    return found

def numeric(text):
    text=re.sub(r'#?\b\d{15,19}\b','',text)
    text=re.sub(r'\b[0-9]{1,3}(?:,[0-9]{3}){2,}(?:\.[0-9]+)?\b',lambda m:m[0].replace(',',''),text)
    values=[]
    pattern=r'(?<![\w])([0-9]+(?:[ \u00a0\u202f][0-9]{3})*(?:[.,][0-9]+)?(?:[eE][+-]?[0-9]+)?)\s*(млн|тыс|млрд)?'
    for m in re.finditer(pattern,text):
        n=Decimal(re.sub(r'[ \u00a0\u202f]','',m[1]).replace(',','.'))
        n*= {'тыс':1000,'млн':1000000,'млрд':1000000000,None:1}[m[2]]
        values.append(n)
    return values

def check(answer,facts,known):
    cited=set(re.findall(r'#(\d{1,19})(?!\d)',answer));mentioned=set(re.findall(r'(?<!\d)\d{15,19}(?!\d)',answer))
    allowed=gids(facts)&set(known)
    warnings=[]
    if not cited<=allowed or not mentioned<=cited:warnings.append('В ответе есть неподтверждённый GID.')
    if FORBIDDEN.search(answer):warnings.append('Недопустимая обвинительная формулировка.')
    source=numeric(json.dumps(facts,ensure_ascii=False));bad=[]
    for n in numeric(answer):
        if n>=1000 and not any(abs(n-v)<=abs(v)*Decimal('.01') for v in source):bad.append(str(n))
    if bad:warnings.append('Неподтверждённые числа: '+', '.join(sorted(set(bad))))
    hard=not answer.strip() or len(answer)>4000 or not cited<=allowed or not mentioned<=cited or bool(FORBIDDEN.search(answer)) or bool(bad)
    return hard,warnings,cited
