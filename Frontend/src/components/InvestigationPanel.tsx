import type { Language } from "../i18n"
import { translate } from "../interfaceCopy"
import { useEffect, useMemo, useRef, useState } from 'react'
import { X, ArrowRight, BookmarkPlus, Download, Route, FileText } from 'lucide-react'
import type { GraphEdge, GraphNode } from '../types/graph'
import { API, money, type NodeCard } from '../api'
import { checkChronology, edgeEvidence, findDirectedPath, reportMarkdown, TRACE_LIMIT, type Evidence, type Trace } from '../investigation'

interface Props {
  language: Language
  open: boolean; onClose: () => void; runId: string; period: string
  nodes: GraphNode[]; edges: GraphEdge[]; selectedId: string; card: NodeCard | null
  selectedEdgeId: string | null; edgeRevision: number; onEdge: (id: string) => void; onNode: (gid: string) => void
  trace: Trace | null; onTrace: (trace: Trace | null) => void; onAsk: (question: string) => void
}

export function InvestigationPanel({ language, open, onClose, runId, period, nodes, edges, selectedId, card, selectedEdgeId, edgeRevision, onEdge, onNode, trace, onTrace, onAsk }: Props) {
  const tr = (text: string, values: Record<string,string|number> = {}) => translate(language,text,values)
  const [tab, setTab] = useState<'edges'|'path'|'case'>('edges')
  const [from, setFrom] = useState(selectedId), [to, setTo] = useState('')
  const [direction, setDirection] = useState('both')
  const [error, setError] = useState(''), [notice, setNotice] = useState('')
  const [items, setItems] = useState<Evidence[]>([])
  const [downloading, setDownloading] = useState(false)
  const [downloadError, setDownloadError] = useState('')
  const panel = useRef<HTMLElement>(null)
  const [edgeLimit, setEdgeLimit] = useState(20)
  const edge = edges.find(e => e.id === selectedEdgeId)
  const traceEdges = trace?.edgeIds.map(id=>edges.find(e=>e.id===id)!).filter(Boolean) || []
  const chronology = checkChronology(traceEdges)
  const chronologyText = chronology.status==='conflict' && 'step' in chronology
    ? tr('Хронология не сходится: на шаге {step} последний перевод был {last}, а предыдущие шаги требуют даты не раньше {earliest}. Эта цепочка не описывает последовательное движение средств в наблюдаемом периоде.', {step:chronology.step!, last:chronology.lastDate!, earliest:chronology.earliest!})
    : tr(chronology.message)
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
    if (items.some(i => i.key === item.key)) { setNotice("Этот факт уже в досье."); return }
    if (items.length >= 30) { setNotice("В досье уже 30 фактов. Удалите ненужные перед добавлением."); return }
    setItems([...items, item]); setNotice("Факт добавлен в досье.")
  }
  function search() {
    setError(''); setNotice(''); onTrace(null)
    try {
      const result = findDirectedPath(nodes, edges, from.trim(), to.trim())
      if (!result) { setError(tr("Направленный путь до {n} связей не найден в этом снимке. Обратное направление может дать другой результат.", {n:TRACE_LIMIT})); return }
      onTrace(result)
    } catch (e) { setError(e instanceof Error ? e.message : tr("Не удалось найти путь.")) }
  }
  function download() {
    const url = URL.createObjectURL(new Blob([reportMarkdown(runId, period, items)], { type:'text/markdown;charset=utf-8' }))
    const link = document.createElement('a'); link.href = url; link.download = `freedom-case-${runId}.md`
    link.click(); setTimeout(() => URL.revokeObjectURL(url), 1000)
  }
  async function downloadPdf() {
    if (downloading || !items.length) return
    setDownloading(true); setDownloadError('')
    try {
      const response = await fetch(API + '/export/report.pdf', {
        method:'POST', headers:{'Content-Type':'application/json'},
        body:JSON.stringify({run_id:runId, keys:items.map(item=>item.key)}),
        signal:AbortSignal.timeout(30000),
      })
      if (!response.ok) {
        const body = await response.json().catch(()=>null)
        throw new Error(response.status===404 ? tr("PDF-экспорт пока недоступен на сервере.") : body?.error?.message || tr("Не удалось сформировать PDF."))
      }
      if (!response.headers.get('content-type')?.includes('application/pdf')) throw new Error(tr("Сервер не вернул PDF. Попробуйте ещё раз."))
      const url = URL.createObjectURL(await response.blob())
      const link = document.createElement('a'); link.href=url; link.download=`freedom-case-${runId}.pdf`
      link.click(); setTimeout(()=>URL.revokeObjectURL(url),1000)
      setNotice("PDF сформирован. Файл передан браузеру для скачивания.")
    } catch (e) {
      setDownloadError(e instanceof Error && e.name==='TimeoutError' ? tr("Сервер не успел сформировать PDF. Попробуйте ещё раз.") : e instanceof Error ? e.message : tr("Не удалось скачать PDF."))
    } finally { setDownloading(false) }
  }
  if (!open) return null
  return <aside className="investigation-panel" aria-label={tr("Расследование")} ref={panel} tabIndex={-1} onKeyDown={e=>{if(e.key==='Escape')onClose()}}>
    <header><div><p className="micro-label">{tr("ОТ СВЯЗИ К ПРОВЕРЯЕМОМУ ФАКТУ")}</p><h2>{tr("Рабочее досье")}</h2></div><button aria-label={tr("Закрыть расследование")} onClick={onClose}><X size={18}/></button></header>
    <nav aria-label={tr("Раздел расследования")}>{([['edges',tr("Связи")],['path',tr("Цепочка")],['case',tr("Досье · {n}", {n:items.length})]] as const).map(([id,title])=><button key={id} aria-pressed={tab===id} onClick={()=>{setTab(id);setNotice('')}}>{title}</button>)}</nav>
    {notice && <p className="case-notice" role="status">{tr(notice)}</p>}
    {tab==='edges' && <>
      {edge && <section className="edge-card"><p className="micro-label">{tr("ВЫБРАННАЯ СВЯЗЬ")}</p><div className="edge-endpoints"><button onClick={()=>onNode(edge.source)}>{edge.source}</button><ArrowRight size={16}/><button onClick={()=>onNode(edge.target)}>{edge.target}</button></div>
        <strong className="edge-amount">{edge.amount}</strong><p>{tr("{n} переводов", {n:edge.transactions ?? '—'})} · {edge.firstDate || '—'} — {edge.lastDate || '—'}</p>
        <p className="case-muted">{tr("Агрегат по направлению плательщик → получатель за наблюдаемый период.")}</p>
        <div className="case-actions"><button onClick={()=>add(edgeEvidence(edge))}><BookmarkPlus size={14}/>{tr("В досье")}</button><button onClick={()=>{setFrom(edge.source);setTo(edge.target);setTab('path')}}><Route size={14}/>{tr("Исследовать путь")}</button></div>
      </section>}
      <div className="case-subheading"><h3>{tr("Связи выбранного узла")}</h3><span>{incident.length}</span></div><p className="case-gid">{selectedId}</p>
      <label className="case-field">{tr("Направление")}<select value={direction} onChange={e=>setDirection(e.target.value)}><option value="both">{tr("Все связи")}</option><option value="in">{tr("Входящие")}</option><option value="out">{tr("Исходящие")}</option></select></label>
      <p className="case-muted">{tr("По убыванию наблюдаемой суммы. Нажмите связь для подробностей.")}</p>
      <div className="edge-list">{incident.slice(0,edgeLimit).map(e=><button className={edge?.id===e.id?'active':''} key={e.id} onClick={()=>onEdge(e.id)}><span>{e.source===selectedId?'→':'←'} {e.source===selectedId?e.target:e.source}</span><b>{e.amount}</b><small>{tr("{n} переводов", {n:e.transactions ?? '—'})}</small></button>)}</div>
      {!incident.length&&<p className="case-muted">{tr("В этом направлении наблюдаемых связей нет. Это не доказывает отсутствие операций вне выборки.")}</p>}
      {incident.length>edgeLimit&&<button className="case-more" onClick={()=>setEdgeLimit(n=>n+20)}>{tr("Ещё 20 связей")}</button>}
    </>}
    {tab==='path' && <>
      <h3>{tr("Как связаны два узла?")}</h3><p className="case-muted">{tr("Кратчайшая направленная цепочка по числу связей. Поиск по всему снимку, до {n} связей, независимо от фильтров графа.", {n:TRACE_LIMIT})}</p>
      <form onSubmit={e=>{e.preventDefault();search()}}><label className="case-field">{tr("Откуда")}<input aria-label={tr("GID начала пути")} value={from} inputMode="numeric" onChange={e=>{setFrom(e.target.value);setError('');onTrace(null)}} required/></label><button type="button" className="case-link" onClick={()=>{setFrom(selectedId);onTrace(null)}}>{tr("Взять выбранный узел")}</button>
        <label className="case-field">{tr("Куда")}<input aria-label={tr("GID конца пути")} value={to} inputMode="numeric" onChange={e=>{setTo(e.target.value);setError('');onTrace(null)}} required/></label>
        <div className="case-actions"><button className="case-primary" type="submit"><Route size={14}/>{tr("Найти цепочку")}</button><button type="button" onClick={()=>{setFrom(to);setTo(from);onTrace(null);setError('')}}>{tr("Поменять местами")}</button></div></form>
      {error&&<p className="integration-error" role="alert">{tr(error)}</p>}
      {trace && <section className="trace-result"><div className="case-subheading"><h3>{tr("Найдено связей: {n}", {n:trace.edgeIds.length})}</h3><button onClick={()=>onTrace(null)}>{tr("Сбросить")}</button></div>
        <ol>{trace.nodeIds.map((gid,i)=><li key={gid}><button onClick={()=>onNode(gid)}>{gid}</button>{traceEdges[i]&&<small>↓ {traceEdges[i].amount} · {tr("{n} переводов", {n:traceEdges[i].transactions ?? '—'})}</small>}</li>)}</ol>
        <div className={`chronology-check ${chronology.status}`}><strong>{tr("Проверка хронологии")}</strong><p>{chronologyText}</p></div>
        <div className="case-actions"><button onClick={()=>add({key:'path:'+trace.edgeIds.join('|'),title:'Направленная цепочка',facts:[trace.nodeIds.join(' → '),chronology.message,...traceEdges.flatMap(e=>[edgeEvidence(e).title,...edgeEvidence(e).facts])]})}><BookmarkPlus size={14}/>{tr("В досье")}</button>
          <button onClick={()=>{onAsk(tr("Объясни направленную цепочку {path}. Проверь связи и даты инструментами. Проверка хронологии: {check}. Объясни ограничения и не утверждай, что это одни и те же деньги.", {path:trace.nodeIds.map(id=>'#'+id).join(' → '),check:chronologyText}));onClose()}}>{tr("Обсудить с AI")}</button></div>
      </section>}
    </>}
    {tab==='case' && <>
      <h3>{tr("Факты для ручной проверки")}</h3><p className="case-muted">{tr("Досье привязано к снимку. Хранится в этой вкладке до обновления страницы. Скачайте отчёт, чтобы сохранить результат.")}</p>
      <button className="case-more" disabled={!card} onClick={()=>{if(card)add({key:'node:'+card.node.gid,title:'Узел '+card.node.gid,facts:[`Роль: ${card.node.role}; приоритет: ${card.node.priority_score}`,`Вход: ${money(card.node.in_kzt)}; выход: ${money(card.node.out_kzt)}`,`Входящих связей: ${card.node.in_deg}; исходящих: ${card.node.out_deg}`,`Обоснование: ${card.node.evidence}`,`Правило: ${card.evidence_detail.rule_text}`,...(card.evidence_detail.limitations||[])]})}}><BookmarkPlus size={14}/>{tr("Добавить выбранный узел")}</button>
      {!items.length&&<p className="case-empty">{tr("Начните с узла, связи или найденной цепочки. В отчёт попадут только добавленные факты.")}</p>}
      <ol className="evidence-list">{items.map(item=><li key={item.key}><strong>{item.title.replace(/^Узел /,tr("Узел")+" ").replace(/^Связь /,tr("Связь")+" ").replace(/^Направленная цепочка$/,tr("Направленная цепочка"))}</strong><p>{item.facts[0]}</p><button onClick={()=>setItems(items.filter(i=>i.key!==item.key))}>{tr("Убрать из досье")}</button></li>)}</ol>
      {downloadError&&<p className="integration-error" role="alert">{tr(downloadError)}</p>}
      <button className="case-primary case-more" disabled={!items.length || downloading} aria-busy={downloading} onClick={downloadPdf}><Download size={15}/> {downloading?tr("Готовим PDF…"):tr("Скачать PDF ({n})", {n:items.length})}</button>
      <button className="case-link case-more" disabled={!items.length} onClick={download}>{tr("Скачать текст .md")}</button>
    </>}
    <footer><FileText size={12}/><span>{tr("Снимок")} {runId}<br/>{period} · {tr("гипотезы, не обвинения")}</span></footer>
  </aside>
}
