import { useEffect, useMemo, useRef, useState } from 'react'
import { X, ArrowRight, BookmarkPlus, Download, Route, FileText } from 'lucide-react'
import type { GraphEdge, GraphNode } from '../types/graph'
import { money, type NodeCard } from '../api'
import { checkChronology, edgeEvidence, findDirectedPath, reportMarkdown, TRACE_LIMIT, type Evidence, type Trace } from '../investigation'

interface Props {
  open: boolean; onClose: () => void; runId: string; period: string
  nodes: GraphNode[]; edges: GraphEdge[]; selectedId: string; card: NodeCard | null
  selectedEdgeId: string | null; edgeRevision: number; onEdge: (id: string) => void; onNode: (gid: string) => void
  trace: Trace | null; onTrace: (trace: Trace | null) => void; onAsk: (question: string) => void
}

export function InvestigationPanel({ open, onClose, runId, period, nodes, edges, selectedId, card, selectedEdgeId, edgeRevision, onEdge, onNode, trace, onTrace, onAsk }: Props) {
  const [tab, setTab] = useState<'edges'|'path'|'case'>('edges')
  const [from, setFrom] = useState(selectedId), [to, setTo] = useState('')
  const [direction, setDirection] = useState('both')
  const [error, setError] = useState(''), [notice, setNotice] = useState('')
  const [items, setItems] = useState<Evidence[]>([])
  const panel = useRef<HTMLElement>(null)
  const [edgeLimit, setEdgeLimit] = useState(20)
  const edge = edges.find(e => e.id === selectedEdgeId)
  const traceEdges = trace?.edgeIds.map(id=>edges.find(e=>e.id===id)!).filter(Boolean) || []
  const chronology = checkChronology(traceEdges)
  const incident = useMemo(() => edges.filter(e =>
    (direction !== 'in' && e.source === selectedId) || (direction !== 'out' && e.target === selectedId))
    .sort((a,b) => (b.sumKzt ?? 0) - (a.sumKzt ?? 0) || a.id.localeCompare(b.id)), [edges, selectedId, direction])
  useEffect(() => { setEdgeLimit(20) }, [selectedId, direction])
  useEffect(() => { if (selectedEdgeId) setTab('edges') }, [selectedEdgeId, edgeRevision])
  useEffect(() => {
    if (!open) return
    const previous = document.activeElement
    panel.current?.focus()
    return () => { if (previous instanceof HTMLElement && previous.isConnected) previous.focus() }
  }, [open])
  function add(item: Evidence) {
    if (items.some(i => i.key === item.key)) { setNotice('Этот факт уже в досье.'); return }
    if (items.length >= 30) { setNotice('В досье уже 30 фактов. Удалите ненужные перед добавлением.'); return }
    setItems([...items, item]); setNotice('Факт добавлен в досье.')
  }
  function search() {
    setError(''); setNotice(''); onTrace(null)
    try {
      const result = findDirectedPath(nodes, edges, from.trim(), to.trim())
      if (!result) { setError(`Направленный путь до ${TRACE_LIMIT} связей не найден в этом снимке. Обратное направление может дать другой результат.`); return }
      onTrace(result)
    } catch (e) { setError(e instanceof Error ? e.message : 'Не удалось найти путь.') }
  }
  function download() {
    const url = URL.createObjectURL(new Blob([reportMarkdown(runId, period, items)], { type:'text/markdown;charset=utf-8' }))
    const link = document.createElement('a'); link.href = url; link.download = `freedom-case-${runId}.md`
    link.click(); setTimeout(() => URL.revokeObjectURL(url), 1000)
  }
  if (!open) return null
  return <aside className="investigation-panel" aria-label="Расследование" ref={panel} tabIndex={-1} onKeyDown={e=>{if(e.key==='Escape')onClose()}}>
    <header><div><p className="micro-label">ОТ СВЯЗИ К ПРОВЕРЯЕМОМУ ФАКТУ</p><h2>Рабочее досье</h2></div><button aria-label="Закрыть расследование" onClick={onClose}><X size={18}/></button></header>
    <nav aria-label="Раздел расследования">{([['edges','Связи'],['path','Цепочка'],['case',`Досье · ${items.length}`]] as const).map(([id,title])=><button key={id} aria-pressed={tab===id} onClick={()=>{setTab(id);setNotice('')}}>{title}</button>)}</nav>
    {notice && <p className="case-notice" role="status">{notice}</p>}
    {tab==='edges' && <>
      {edge && <section className="edge-card"><p className="micro-label">ВЫБРАННАЯ СВЯЗЬ</p><div className="edge-endpoints"><button onClick={()=>onNode(edge.source)}>{edge.source}</button><ArrowRight size={16}/><button onClick={()=>onNode(edge.target)}>{edge.target}</button></div>
        <strong className="edge-amount">{edge.amount}</strong><p>{edge.transactions ?? '—'} переводов · {edge.firstDate || '—'} — {edge.lastDate || '—'}</p>
        <p className="case-muted">Агрегат по направлению плательщик → получатель за наблюдаемый период.</p>
        <div className="case-actions"><button onClick={()=>add(edgeEvidence(edge))}><BookmarkPlus size={14}/> В досье</button><button onClick={()=>{setFrom(edge.source);setTo(edge.target);setTab('path')}}><Route size={14}/> Исследовать путь</button></div>
      </section>}
      <div className="case-subheading"><h3>Связи выбранного узла</h3><span>{incident.length}</span></div><p className="case-gid">{selectedId}</p>
      <label className="case-field">Направление<select value={direction} onChange={e=>setDirection(e.target.value)}><option value="both">Все связи</option><option value="in">Входящие</option><option value="out">Исходящие</option></select></label>
      <p className="case-muted">По убыванию наблюдаемой суммы. Нажмите связь для подробностей.</p>
      <div className="edge-list">{incident.slice(0,edgeLimit).map(e=><button className={edge?.id===e.id?'active':''} key={e.id} onClick={()=>onEdge(e.id)}><span>{e.source===selectedId?'→':'←'} {e.source===selectedId?e.target:e.source}</span><b>{e.amount}</b><small>{e.transactions ?? '—'} переводов</small></button>)}</div>
      {!incident.length&&<p className="case-muted">В этом направлении наблюдаемых связей нет. Это не доказывает отсутствие операций вне выборки.</p>}
      {incident.length>edgeLimit&&<button className="case-more" onClick={()=>setEdgeLimit(n=>n+20)}>Ещё 20 связей</button>}
    </>}
    {tab==='path' && <>
      <h3>Как связаны два узла?</h3><p className="case-muted">Кратчайшая направленная цепочка по числу связей. Поиск по всему снимку, до {TRACE_LIMIT} связей, независимо от фильтров графа.</p>
      <form onSubmit={e=>{e.preventDefault();search()}}><label className="case-field">Откуда<input aria-label="GID начала пути" value={from} inputMode="numeric" onChange={e=>{setFrom(e.target.value);setError('');onTrace(null)}} required/></label><button type="button" className="case-link" onClick={()=>{setFrom(selectedId);onTrace(null)}}>Взять выбранный узел</button>
        <label className="case-field">Куда<input aria-label="GID конца пути" value={to} inputMode="numeric" onChange={e=>{setTo(e.target.value);setError('');onTrace(null)}} required/></label>
        <div className="case-actions"><button className="case-primary" type="submit"><Route size={14}/> Найти цепочку</button><button type="button" onClick={()=>{setFrom(to);setTo(from);onTrace(null);setError('')}}>Поменять местами</button></div></form>
      {error&&<p className="integration-error" role="alert">{error}</p>}
      {trace && <section className="trace-result"><div className="case-subheading"><h3>Найдено связей: {trace.edgeIds.length}</h3><button onClick={()=>onTrace(null)}>Сбросить</button></div>
        <ol>{trace.nodeIds.map((gid,i)=><li key={gid}><button onClick={()=>onNode(gid)}>{gid}</button>{traceEdges[i]&&<small>↓ {traceEdges[i].amount} · {traceEdges[i].transactions ?? '—'} переводов</small>}</li>)}</ol>
        <div className={`chronology-check ${chronology.status}`}><strong>Проверка хронологии</strong><p>{chronology.message}</p></div>
        <div className="case-actions"><button onClick={()=>add({key:'path:'+trace.edgeIds.join('|'),title:'Направленная цепочка',facts:[trace.nodeIds.join(' → '),chronology.message,...traceEdges.flatMap(e=>[edgeEvidence(e).title,...edgeEvidence(e).facts])]})}><BookmarkPlus size={14}/> В досье</button>
          <button onClick={()=>{onAsk(`Объясни направленную цепочку ${trace.nodeIds.map(id=>'#'+id).join(' → ')}. Проверь связи и даты инструментами. Проверка диапазонов дат в интерфейсе: ${chronology.message} Объясни ограничения и не утверждай, что это одни и те же деньги.`);onClose()}}>Обсудить с AI</button></div>
      </section>}
    </>}
    {tab==='case' && <>
      <h3>Факты для ручной проверки</h3><p className="case-muted">Досье привязано к снимку. Хранится в этой вкладке до обновления страницы. Скачайте отчёт, чтобы сохранить результат.</p>
      <button className="case-more" disabled={!card} onClick={()=>{if(card)add({key:'node:'+card.node.gid,title:'Узел '+card.node.gid,facts:[`Роль: ${card.node.role}; приоритет: ${card.node.priority_score}`,`Вход: ${money(card.node.in_kzt)}; выход: ${money(card.node.out_kzt)}`,`Входящих связей: ${card.node.in_deg}; исходящих: ${card.node.out_deg}`,`Обоснование: ${card.node.evidence}`,`Правило: ${card.evidence_detail.rule_text}`,...(card.evidence_detail.limitations||[])]})}}><BookmarkPlus size={14}/> Добавить выбранный узел</button>
      {!items.length&&<p className="case-empty">Начните с узла, связи или найденной цепочки. В отчёт попадут только добавленные факты.</p>}
      <ol className="evidence-list">{items.map(item=><li key={item.key}><strong>{item.title}</strong><p>{item.facts[0]}</p><button onClick={()=>setItems(items.filter(i=>i.key!==item.key))}>Убрать из досье</button></li>)}</ol>
      <button className="case-primary case-more" disabled={!items.length} onClick={download}><Download size={15}/> Скачать отчёт .md ({items.length})</button>
    </>}
    <footer><FileText size={12}/><span>Снимок {runId}<br/>{period} · гипотезы, не обвинения</span></footer>
  </aside>
}
