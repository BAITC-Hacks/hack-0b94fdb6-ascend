from collections import deque
import numpy as np
import pandas as pd
from .base import ExtraResult

def run(ctx):
    tx=ctx.transactions; cfg=ctx.cfg['temporal']; features={}; events=[]
    incoming={g:v.sort_values(['date','src','sum_kzt']) for g,v in tx.groupby('dst')}
    outgoing={g:v.sort_values(['date','dst','sum_kzt']) for g,v in tx.groupby('src')}
    empty=tx.iloc[:0]
    for n in ctx.nodes.itertuples():
        ins=incoming.get(n.gid,empty); outs=outgoing.get(n.gid,empty)
        queue=deque(); arrivals=list(ins.itertuples()); i=0; matched=0; holds=[]; matched_days={}
        for out in outs.itertuples():
            while i<len(arrivals) and arrivals[i].date<=out.date:
                a=arrivals[i]; queue.append([a.date,int(round(a.sum_kzt*100))]); i+=1
            while queue and (out.date-queue[0][0]).days>cfg['fast_pass_days']: queue.popleft()
            need=int(round(out.sum_kzt*100))
            while need and queue:
                date,available=queue[0]; take=min(available,need); need-=take; matched+=take
                holds.append(((out.date-date).days,take)); matched_days[out.date]=matched_days.get(out.date,0)+take
                queue[0][1]-=take
                if not queue[0][1]: queue.popleft()
        median=None
        if matched:
            acc=0
            for lag,weight in sorted(holds):
                acc+=weight
                if acc>=matched/2: median=lag; break
        both=pd.concat([ins,outs]); counts=both.groupby('date').size(); active=len(counts)
        burst_score=float(counts.max()/counts.mean()) if active else 0
        f=dict(fast_matched_kzt=matched/100,fast_pass_share=matched/100/n.in_kzt if n.in_kzt else 0,median_hold_days=median,
               burst_score=burst_score,burst=bool(active and counts.max()>=cfg['burst_min_tx'] and burst_score>=cfg['burst_ratio']),active_days=active,
               first_date=str(both.date.min()) if active else None,last_date=str(both.date.max()) if active else None)
        f['fast_transit']=bool(f['fast_pass_share']>=cfg['fast_share'] and matched/100>=cfg['fast_min_kzt'] and not n.is_seed)
        for kind,sub,other,minimum in [('in',ins,'src',cfg['sync_in_min']),('out',outs,'dst',cfg['sync_out_min'])]:
            by=sub.groupby('date')[other].nunique(); f['max_senders_same_day' if kind=='in' else 'max_recipients_same_day']=int(by.max()) if len(by) else 0
            f[f'sync_{kind}_days']=int((by>=minimum).sum())
            for date,num in by[by>=minimum].items():
                day=sub[sub.date==date]; parties=sorted(set(day[other]))
                events.append(dict(event_type='sync_'+kind,gid=n.gid,date=str(date),n_counterparties=int(num),sum_kzt=float(day.sum_kzt.sum()),counterparties=';'.join(map(str,parties[:20])),description='Синхронные переводы в один день; порядок внутри дня неизвестен.'))
        if f['fast_transit']:
            for date,value in sorted(matched_days.items()):
                events.append(dict(event_type='fast_transit',gid=n.gid,date=str(date),n_counterparties=0,sum_kzt=value/100,counterparties='',description='FIFO-сопоставление сумм, не доказательство движения одних и тех же денег.'))
        if f['burst']:
            for date,count in counts.items():
                if count>=cfg['burst_min_tx'] and count/counts.mean()>=cfg['burst_ratio']:
                    day=both[both.date==date]
                    events.append(dict(event_type='burst',gid=n.gid,date=str(date),n_counterparties=len(set(day.src)|set(day.dst))-1,sum_kzt=float(day.sum_kzt.sum()),counterparties='',description='Всплеск относительно среднего по активным дням.'))
        features[int(n.gid)]=f
    rows=[]
    period=ctx.config['reference_period']
    for dt in pd.date_range(period['from'],period['to']):
        day=tx[tx.date==dt.date()]
        rows.append(dict(date=str(dt.date()),n_tx=len(day),sum_kzt=float(day.sum_kzt.sum()),n_active_nodes=len(set(day.src)|set(day.dst))))
    daily=pd.DataFrame(rows); med=daily.sum_kzt.median(); mad=(daily.sum_kzt-med).abs().median();daily['is_spike']=daily.sum_kzt>med+cfg['spike_mad']*mad
    events.sort(key=lambda r:(r['date'],r['gid'],r['event_type']))
    for i,r in enumerate(events):r['event_id']=f'T{i+1:05}'
    columns='event_id event_type gid date n_counterparties sum_kzt counterparties description'.split()
    summary=dict(fast_share_half=sum(f['fast_pass_share']>=cfg['fast_share'] for f in features.values()),fast_share_half_nonseed=sum(features[int(r.gid)]['fast_pass_share']>=cfg['fast_share'] for r in ctx.nodes.itertuples() if not r.is_seed),fast_transit=sum(f['fast_transit'] for f in features.values()),sync_in=sum(r['event_type']=='sync_in' for r in events),sync_out=sum(r['event_type']=='sync_out' for r in events),sync_in_nodes=len({r['gid'] for r in events if r['event_type']=='sync_in'}))
    return ExtraResult({'temporal_events':pd.DataFrame(events,columns=columns),'daily_flow':daily},summary,features)
