import pandas as pd
from .base import ExtraResult

def run(ctx):
    n=ctx.nodes; c=ctx.cfg['boundary']; tx=ctx.transactions
    deg=lambda v: 0 if v==1 else 1 if v==2 else 2 if v<=4 else 3
    money=lambda v: sum(v>=x for x in c['money_bins'])
    reference=n[(~n.is_seed)&n.depth.between(1,3)&(n.in_deg>0)]
    groups={}
    for r in reference.itertuples():
        groups.setdefault((deg(r.in_deg),money(r.in_kzt)),[]).append(r.out_deg>0)
    rates=[]
    for d in range(4):
        for b in range(4):
            vals=groups.get((d,b),[])
            rates.append(dict(profile_bucket=f'{d}:{b}',n_reference=len(vals),n_onward=sum(vals),p_onward=sum(vals)/len(vals) if vals else None))
    last=tx.groupby('dst').date.max().to_dict(); rows=[]; before={'sink_like':0,'unknown':0,'likely_onward':0}; late_count=0
    for r in n.itertuples():
        if not r.is_boundary and r.out_deg!=0: continue
        d,b=deg(r.in_deg),money(r.in_kzt); vals=list(groups.get((d,b),[])); raw=sum(vals)/len(vals) if vals else None
        if r.is_boundary:
            status='unknown' if raw is None else 'likely_onward' if raw>=c['likely'] else 'sink_like' if raw<=c['sink'] else 'unknown'
            before[status]+=1
        merged=[b]
        for lower in range(b-1,-1,-1):
            if len(vals)>=c['min_bucket']: break
            vals+=groups.get((d,lower),[]); merged.append(lower)
        p=sum(vals)/len(vals) if len(vals)>=c['min_bucket'] else None
        date=last.get(r.gid); late=date is not None and str(date)>=c['late_from']
        if r.is_boundary and late: late_count+=1
        status='observed_sink' if not r.is_boundary else 'unknown' if p is None else 'likely_onward' if p>=c['likely'] else 'sink_like' if p<=c['sink'] else 'unknown'
        if late and status=='sink_like': status='unknown'
        rows.append(dict(gid=r.gid,depth=r.depth,in_deg=r.in_deg,in_kzt=r.in_kzt,profile_bucket=f'{d}:{b}',merged_buckets=','.join(map(str,merged)),p_onward=p,bucket_size=len(vals),last_in_date=str(date) if date else None,late_inflow=late,boundary_status=status))
    frame=pd.DataFrame(rows)
    return ExtraResult({'boundary':frame,'boundary_rates':pd.DataFrame(rates)},dict(n_reference=len(reference),n_boundary=int(n.is_boundary.sum()),raw_status_counts=before,late_inflow=late_count),{int(r['gid']):r for r in rows})
