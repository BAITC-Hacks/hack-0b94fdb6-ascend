import numpy as np
import pandas as pd
from .base import ExtraResult

def run(ctx):
    cfg=ctx.cfg['anomalies'];rows=[];flags={int(g):[] for g in ctx.nodes.gid};pairs=0
    for (src,dst),group in ctx.transactions.groupby(['src','dst']):
        records=list(group.sort_values(['date','sum_kzt']).itertuples());best=None
        # Whole date windows: no arbitrary subset of transfers on the same day.
        for start in sorted(group.date.unique()):
            window=group[(group.date>=start)&(group.date<=start+pd.Timedelta(days=cfg['split_window_days']))]
            if len(window)<cfg['split_min_tx']:continue
            values=window.sum_kzt.to_numpy();cv=float(values.std()/values.mean())
            if cv<=cfg['split_cv'] and (best is None or len(values)>best[0]):best=(len(values),cv,float(values.sum()))
        if best:
            pairs+=1;flags[int(src)].append('split');flags[int(dst)].append('split')
            rows.append(dict(gid=src,anomaly_type='split_pair',feature='n_tx_window',value=best[0],reference=best[1],ratio=None,counterparty_gid=dst,description='Похожие суммы в коротком окне; дробление ниже 5 000 ₸ в данных не видно.'))
    for feature in ['in_deg','out_deg','in_kzt','out_kzt','in_tx','out_tx']:
        threshold=ctx.nodes[feature].quantile(cfg['global_quantile'])
        for _,group in ctx.nodes.groupby('depth'):
            ranks=group[feature].rank(method='max',pct=True);median=float(group[feature].median())
            for r in group[(ranks>=cfg['depth_quantile'])&(group[feature]>threshold)].itertuples():
                value=float(getattr(r,feature));flags[int(r.gid)].append('depth_outlier')
                rows.append(dict(gid=r.gid,anomaly_type='depth_outlier',feature=feature,value=value,reference=median,ratio=value/median if median else None,counterparty_gid=None,description='Выше сверстников по колену и глобального порога; при нулевой медиане отношение не определено.'))
    rows.sort(key=lambda r:(r['gid'],r['anomaly_type'],r['feature'],r['counterparty_gid'] or 0))
    for i,r in enumerate(rows):r['anomaly_id']=f'A{i+1:05}'
    frame=pd.DataFrame(rows,columns='anomaly_id gid anomaly_type feature value reference ratio counterparty_gid description'.split())
    frame['counterparty_gid']=pd.array([r['counterparty_gid'] for r in rows],dtype='Int64')
    return ExtraResult({'anomalies':frame},dict(split_pairs=pairs,n_anomalies=len(rows),round_amount_share=float((ctx.transactions.sum_kzt%1000==0).mean())),{g:{'anomaly_flags':sorted(set(v))} for g,v in flags.items()})
