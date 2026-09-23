"""Sidecar serialization kept separate from the three mandatory CSV files."""
import json
import math
from datetime import date
from pathlib import Path
import pandas as pd

IDS={'gid','src','dst','a','b','c','counterparty_gid'}

def clean(value,key=''):
    if isinstance(value,dict):return {str(k):clean(v,str(k)) for k,v in value.items()}
    if isinstance(value,(list,tuple)):return [clean(v,'gid' if key in ('gids','reached_by','top_gids') else '') for v in value]
    if hasattr(value,'item'):value=value.item()
    if value is None or value is pd.NA or isinstance(value,float) and not math.isfinite(value):return None
    if isinstance(value,date):return str(value)
    if key in IDS:return str(int(value)) if not isinstance(value,str) else value
    return value

def payload(results):
    out={'tables':{},'features':{},'documents':{}}
    for name,result in results.items():
        out['tables'].update({k:clean(v.to_dict('records')) for k,v in result.tables.items()})
        for gid,values in result.features.items():out['features'].setdefault(str(gid),{})[name]=clean(values)
        out['documents'].update(clean(result.documents))
    return out

def write(directory,results):
    target=Path(directory)/'extras';target.mkdir(exist_ok=True)
    for result in results.values():
        for name,frame in result.tables.items():
            frame=frame.copy()
            for col in IDS & set(frame.columns):frame[col]=pd.array(frame[col],dtype='Int64')
            frame.to_csv(target/(name+'.csv'),index=False,lineterminator='\n',float_format='%.8f')
        for name,doc in result.documents.items():
            if isinstance(doc,str):(target/(name+'.md')).write_text(doc,encoding='utf-8')
            else:(target/(name+'.json')).write_text(json.dumps(clean(doc),ensure_ascii=False,allow_nan=False,indent=2),encoding='utf-8')
