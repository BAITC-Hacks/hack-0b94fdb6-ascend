"""Extra tools read precomputed snapshot data only."""
from collections import Counter
import re
import networkx as nx


class ExtraQueries:
    def _table(self, name):
        return self.extras.get('tables', {}).get(name, [])

    def _features(self, gid):
        return self.extras.get('features', {}).get(gid, {})

    def _list(self, items, limit=20, available=True):
        return dict(items=items[:limit],total=len(items),truncated=len(items)>limit,available=available)

    def find_nodes(self, role=None, cluster_id=None, depth=None, is_seed=None, min_in_deg=None, min_out_deg=None, min_in_kzt=None, flag=None, sort='priority', limit=20):
        from .query import integer,ToolError
        integer(limit,1,20)
        if sort not in ('priority','in_kzt','in_deg','out_deg'):raise ToolError('invalid_param','Неверная сортировка')
        flags=('fast_transit','burst','split','depth_outlier','boundary_likely_onward','external_inflow')
        if flag is not None and flag not in flags:raise ToolError('invalid_param','Неизвестный флаг')
        if role is not None and role not in ('coordinator','consolidator','distributor','transit','terminal','peripheral'):raise ToolError('invalid_param','Неизвестная роль')
        if depth is not None:integer(depth,0,4)
        if cluster_id is not None:integer(cluster_id,0,max(self.clusters,default=0))
        if is_seed is not None and type(is_seed) is not bool:raise ToolError('invalid_param','is_seed должен быть bool')
        for v in (min_in_deg,min_out_deg,min_in_kzt):
            if v is not None and (type(v) not in (int,float) or v<0):raise ToolError('invalid_param','Порог должен быть неотрицательным числом')
        found=[]
        for gid in self.nodes:
            n=self.node(gid);f=self._features(gid)
            if any(v is not None and n.get(k)!=v for k,v in [('role',role),('cluster_id',cluster_id),('depth',depth),('is_seed',is_seed)]):continue
            if any(v is not None and n.get(k,0)<v for k,v in [('in_deg',min_in_deg),('out_deg',min_out_deg),('in_kzt',min_in_kzt)]):continue
            if flag:
                yes=n.get('external_inflow',False) if flag=='external_inflow' else f.get('boundary',{}).get('boundary_status')=='likely_onward' if flag=='boundary_likely_onward' else flag in f.get('anomalies',{}).get('anomaly_flags',[]) if flag in ('split','depth_outlier') else f.get('temporal',{}).get(flag,False)
                if not yes:continue
            found.append(n)
        key='priority_score' if sort=='priority' else sort
        found.sort(key=lambda n:(-n.get(key,0),int(n['gid'])))
        return self._list(found,limit)

    def get_temporal(self,gid=None,date=None):
        from .query import ToolError
        if (gid is None)==(date is None):raise ToolError('invalid_param','Нужен ровно один параметр: gid или date')
        events=self._table('temporal_events')
        if gid is not None:
            self.gid(gid);f=self._features(gid).get('temporal',{})
            return dict(gid=gid,features=f,**self._list([r for r in events if r['gid']==gid],20,'temporal_events' in self.extras.get('tables',{})))
        if not isinstance(date,str) or not re.fullmatch(r'2026-07-(0[1-9]|[12][0-9]|3[01])',date):raise ToolError('invalid_param','Ожидается дата июля 2026 YYYY-MM-DD')
        return dict(daily=next((r for r in self._table('daily_flow') if r['date']==date),None),**self._list([r for r in events if r['date']==date],20,'daily_flow' in self.extras.get('tables',{})))

    def get_routes(self,gid,kind='both',limit=10):
        from .query import integer,ToolError
        self.gid(gid);integer(limit,1,10)
        if kind not in ('cycles','chains','both'):raise ToolError('invalid_param','kind: cycles/chains/both')
        rows=[]
        if kind in ('cycles','both'):rows.extend(dict(r,kind='cycle') for r in self._table('cycles') if gid in r['path'].split('→'))
        if kind in ('chains','both'):rows.extend(dict(r,kind='chain') for r in self._table('chains') if gid in (r['a'],r['b'],r['c']))
        return dict(limitation='Даты не доказывают движение одних и тех же средств.',**self._list(rows,limit,'cycles' in self.extras.get('tables',{})))

    def get_anomalies(self,gid=None,type=None,limit=20):
        from .query import integer,ToolError
        integer(limit,1,20)
        if gid is not None:self.gid(gid)
        if type not in (None,'split_pair','depth_outlier'):raise ToolError('invalid_param','Неизвестный тип аномалии')
        rows=[r for r in self._table('anomalies') if (gid is None or gid in (r['gid'],r.get('counterparty_gid'))) and (type is None or r['anomaly_type']==type)]
        return self._list(rows,limit,'anomalies' in self.extras.get('tables',{}))

    def get_resilience(self,n=None):
        from .query import ToolError
        if n is not None and (type(n) is not int or n not in (5,10,20,50,100)):raise ToolError('invalid_param','n: 5/10/20/50/100')
        rows=[r for r in self._table('resilience') if n is None or r['n_removed']==n]
        removed=[dict(r,gids=r['gids'].split(';') if r['gids'] else []) for r in self._table('resilience_removed') if (n is None or r['n_removed']==n) and r['strategy']=='priority']
        return dict(removed=removed,**self._list(rows,18,'resilience' in self.extras.get('tables',{})))

    def get_gaps(self,limit=10):
        from .query import integer
        integer(limit,1,10)
        rows=[dict(r,gids=r['gids'].split(';') if r['gids'] else []) for r in self._table('gaps')]
        return self._list(rows,limit,'gaps' in self.extras.get('tables',{}))

    def get_boundary(self,gid=None):
        if gid is not None:
            self.gid(gid);f=self._features(gid).get('boundary',{})
            return dict(gid=gid,status=f,available=bool(f))
        rows=self._table('boundary')
        return dict(counts=dict(Counter(r['boundary_status'] for r in rows if r['depth']==4)),rates=self._table('boundary_rates'),available='boundary' in self.extras.get('tables',{}))

    def get_methodology(self):
        return dict(config=self.run.get('config',{}),version=self.run.get('methodology_version'),formulas={'priority':'sum(weighted nonzero percentile features + role_weight*role_score*priority_weights.role) * seed_factor; divide by maximum over all nodes','role_score':'base: min(1, strength/2); coordinator: mean(min(1, ratio/2)); peripheral: 1 - 0.5*min(1,strength); isolate=config.isolated_role_score; boundary multiplies config.boundary_factor'},limitation='Score не является вероятностью виновности.')

    def get_node_card(self,gid):
        self.gid(gid);node=self.node(gid);raw=self.nodes[gid];extra=self._features(gid)
        detail=raw.get('evidence_detail',raw)
        sections={'role':{k:detail.get(k,node.get(k)) for k in ('role','role_score','priority_score','priority_rank','rule_id','rule_text','thresholds','values','alternatives')},'limitations':detail.get('limitations',[])}
        if not node.get('is_isolated'):
            sections['flows']={k:node.get(k) for k in ('in_kzt','out_kzt','in_tx','out_tx','pass_through')}
            sections['flows'].update(first_date=extra.get('temporal',{}).get('first_date'),last_date=extra.get('temporal',{}).get('last_date'),incoming=self.get_neighbors(gid,'in',3),outgoing=self.get_neighbors(gid,'out',3))
            reachable=nx.single_source_shortest_path(self.g,gid,cutoff=4)
            candidates=[g for g in reachable if g!=gid and self.nodes[g]['role'] in ('coordinator','consolidator')]
            target=min(candidates,key=lambda g:(len(reachable[g]),-self.nodes[g]['priority_score'],int(g))) if candidates else None
            sections['links']=dict(cluster_id=node.get('cluster_id'),cluster=self.clusters.get(node.get('cluster_id')),nearest_hub=target,path=reachable[target] if target else [],n_nbr_clusters=node.get('n_nbr_clusters'))
            for name in ('temporal','routes','anomalies','boundary'):
                if extra.get(name):sections[name]=dict(extra[name])
            if 'routes' in sections:sections['routes']['examples']=self.get_routes(gid,'both',3)
            if 'anomalies' in sections:sections['anomalies']['examples']=self.get_anomalies(gid,None,3)
            requests=[r['suggested_request'] for r in self._table('gaps') if gid in r['gids'].split(';')][:3]
            sections['next_steps']=requests or ['Проверить полноту контрагентов и операций за пределами среза.']
        from ai_agent.report import report
        text=report([{'node':node}])[0] or f"GID: #{gid}\nОснование: {node.get('evidence','Нет данных')}"
        if node.get('is_isolated'):text=f"GID: #{gid}\nРоль: {node.get('role')}\nСоответствие роли: {node.get('role_score')}\nОснование: {node.get('evidence')}\nОграничения: изолированный узел в наблюдаемом срезе; данных для вывода о финансовой деятельности недостаточно."
        import json
        for name,label in [('role','Правило и альтернативы'),('links','Связи'),('temporal','Время'),('routes','Маршруты'),('anomalies','Аномалии'),('boundary','Граница'),('next_steps','Что проверить дальше')]:
            if name in sections:
                text+='\n\n'+label+': '+json.dumps(sections[name],ensure_ascii=False)
        return dict(gid=gid,sections=sections,text=text,mode='template')
