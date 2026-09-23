import json
from copy import deepcopy

def bounded(result,limit=8000):
    result=deepcopy(result)
    def lists(value):
        found=[]
        if isinstance(value,dict):
            for k,v in value.items():
                if isinstance(v,list) and v:found.append(v)
                found.extend(lists(v))
        elif isinstance(value,list):
            for v in value:found.extend(lists(v))
        return found
    while len(json.dumps(result,ensure_ascii=False,allow_nan=False))>limit:
        candidates=lists(result)
        if not candidates:
            # A pathological text field cannot bypass the wire-size budget.
            return {'source':result.get('source'),'truncated':True,'available':False,'warning':'Результат слишком велик; уточните запрос.'}
        largest=max(candidates,key=lambda a:len(json.dumps(a,ensure_ascii=False)))
        largest.pop();result['truncated']=True
    result.setdefault('truncated',False)
    return result
