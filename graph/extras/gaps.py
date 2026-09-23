import pandas as pd
from .base import ExtraResult

def run(ctx):
    n=ctx.nodes.set_index('gid',drop=False);b=ctx.table('boundary','boundary');a=ctx.table('anomalies','anomalies');cfg=ctx.cfg['gaps']
    rows=[]
    def add(kind,ids,reason,request,limit=None):
        ids=list(dict.fromkeys(int(v) for v in ids))
        if limit:ids=ids[:limit]
        if not ids:return
        importance=sum(float(n.loc[g,'priority_score']) for g in ids)*cfg['weights'][kind]
        rows.append(dict(gap_id=kind,gap_type=kind,importance=importance,n_nodes=len(ids),gids=';'.join(map(str,ids[:50])),reason=reason,suggested_request=request))
    order=n.sort_values('priority_rank').index
    boundary=set(b.loc[(b.boundary_status=='likely_onward')|(b.gid.isin(n[n.priority_rank<=100].index)), 'gid']) if len(b) else set()
    add('G_BOUNDARY',[g for g in order if g in boundary and n.loc[g,'is_boundary']], 'Обрыв наблюдения на границе','Исходящие переводы за июль–август: продолжение цепочки за 4-м коленом',50)
    last_dates=ctx.transactions.groupby('dst').date.max()
    add('G_LATE',[int(g) for g,d in last_dates.items() if str(d)>=ctx.cfg['boundary']['late_from']],'Вход в конце периода','Операции за август: деньги могли уйти после окончания периода')
    external=n[n.external_inflow].copy();external['difference']=external.out_kzt-external.in_kzt
    add('G_EXTERNAL',external.sort_values(['difference','priority_rank'],ascending=[False,True]).index,'Выход превышает наблюдаемый вход','Входящие переводы, включая межбанковские и пополнения наличными',50)
    add('G_SEED_IN',n[n.is_seed].index,'Входящие seed неполные','Входящие поступления seed за июль')
    add('G_SEED_SILENT',n[n.is_seed&(n.out_deg==0)].index,'Seed без исходящих в срезе','Полная выписка seed: другие банки и снятие наличных')
    sinks=set(b.loc[b.boundary_status=='observed_sink','gid']) if len(b) else set()
    add('G_SINK',[g for g in order if g in sinks and n.loc[g,'in_kzt']>=cfg['sink_min_kzt']],'Наблюдаемый сток','Межбанковские исходящие и снятие наличных',50)
    threshold=set()
    if len(a):
        for r in a[a.anomaly_type=='split_pair'].itertuples():threshold.update([int(r.gid),int(r.counterparty_gid)])
    tx=ctx.transactions
    for gid in n.index:
        part=tx[(tx.src==gid)|(tx.dst==gid)]
        if len(part) and part.sum_kzt.between(5000,10000,inclusive='left').mean()>=cfg['small_share']:threshold.add(gid)
    add('G_THRESHOLD',[g for g in order if g in threshold],'Нижний порог выгрузки скрывает мелкие переводы','Переводы ниже 5 000 ₸ по указанным узлам и парам')
    rows.sort(key=lambda r:(-r['importance'],r['gap_id']))
    turnover=float(tx.sum_kzt.sum());bounds=set(n[n.is_boundary].index)
    coverage=dict(boundary_share=len(bounds)/len(n) if len(n) else 0,boundary_flow_share=float(tx[tx.dst.isin(bounds)].sum_kzt.sum())/turnover if turnover else 0,observed_sink_flow_share=float(tx[tx.dst.isin(sinks)].sum_kzt.sum())/turnover if turnover else 0,seed_without_out=int((n.is_seed&(n.out_deg==0)).sum()),isolated=int(n.is_isolated.sum()),small_tx_share=float(tx.sum_kzt.between(5000,10000,inclusive='left').mean()) if len(tx) else 0)
    return ExtraResult({'gaps':pd.DataFrame(rows,columns='gap_id gap_type importance n_nodes gids reason suggested_request'.split())},dict(n_requests=len(rows)),documents={'coverage':coverage})
