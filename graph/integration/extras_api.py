"""Optional router owned by Graph+AI, mounted before the frontend catch-all."""
from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from graph.query import SnapshotTools, ToolError


def install(app,get_snapshot):
    router=APIRouter(prefix='/api/v1');cache={'snapshot':None,'tools':None}
    def tools():
        snap=get_snapshot()
        if snap is None:return None
        if cache['snapshot'] is not snap:cache.update(snapshot=snap,tools=SnapshotTools(snap))
        return cache['tools']
    def call(name,**args):
        t=tools()
        if t is None:return dict(items=[],available=False,total=0,truncated=False)
        try:return dict(getattr(t,name)(**args),source='snapshot:'+str(t.run.get('run_id','unknown')))
        except ToolError as e:return JSONResponse({'error':{'code':e.code,'message':str(e),'details':{}}},status_code=404 if e.code=='not_found' else 400)
    @router.get('/nodes/{gid}/card')
    def card(gid:str,ai:int=Query(0,ge=0,le=1)):
        r=call('get_node_card',gid=gid)
        if ai and isinstance(r,dict):r['warnings']=['Используется проверенная template-карточка; AI-перефразирование опционально.']
        return r
    @router.get('/boundary')
    def boundary():return call('get_boundary',gid=None)
    @router.get('/boundary/{gid}')
    def boundary_node(gid:str):return call('get_boundary',gid=gid)
    @router.get('/temporal/daily')
    def daily():
        t=tools();rows=t._table('daily_flow') if t else []
        return dict(items=rows,total=len(rows),truncated=False,available=bool(t and 'daily_flow' in t.extras.get('tables',{})))
    @router.get('/temporal/events')
    def events(gid:str|None=None,date:str|None=None,type:str|None=None,limit:int=Query(20,ge=1,le=100)):
        t=tools()
        if t is None:return dict(items=[],available=False,total=0,truncated=False)
        if gid is not None:
            try:t.gid(gid)
            except ToolError as e:return JSONResponse({'error':{'code':e.code,'message':str(e)}},status_code=404)
        rows=[r for r in t._table('temporal_events') if (gid is None or r['gid']==gid) and (date is None or r['date']==date) and (type is None or r['event_type']==type)]
        return t._list(rows,limit,'temporal_events' in t.extras.get('tables',{}))
    @router.get('/routes')
    def routes(gid:str,kind:str='both',limit:int=Query(10,ge=1,le=10)):return call('get_routes',gid=gid,kind=kind,limit=limit)
    @router.get('/anomalies')
    def anomalies(gid:str|None=None,type:str|None=None,limit:int=Query(20,ge=1,le=20)):return call('get_anomalies',gid=gid,type=type,limit=limit)
    @router.get('/resilience')
    def resilience():return call('get_resilience',n=None)
    @router.get('/gaps')
    def gaps():return call('get_gaps',limit=10)
    @router.get('/coverage')
    def coverage():
        t=tools();doc=t.extras.get('documents',{}).get('coverage') if t else None
        return dict(coverage=doc,available=doc is not None)
    @router.get('/methodology')
    def methodology():return call('get_methodology')
    # Replace only this router's own paths when the standalone snapshot adapter overrides backend.
    paths={r.path for r in router.routes}
    app.router.routes[:]=[r for r in app.router.routes if getattr(r,'path',None) not in paths]
    app.router.routes[0:0]=router.routes;app.openapi_schema=None
    return router
