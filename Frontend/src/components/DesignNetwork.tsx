import type { Language } from "../i18n"
import { translate } from "../interfaceCopy"
import { useEffect, useMemo, useRef, useState } from 'react'
import cytoscape, { type Core } from 'cytoscape'
import { Maximize2, Minus, Plus, Pause, Play, Activity, Network, Layers3 } from 'lucide-react'
import type { GraphEdge, GraphNode } from '../types/graph'
import { getClusterColor, roleMeta } from '../data/mockData'
import { riskColors, riskIndex, roleOrder, type Copy } from '../i18n'
import { attachFlowAnimation } from './flowAnimation'
import { selectGraphView } from '../graphView'
import type { Trace } from '../investigation'

type Mode = 'priority' | 'role' | 'cluster'
interface Props {
  language: Language
  limit: number
  trace: Trace | null; onClearTrace: () => void; onSelectEdge: (id:string)=>void; selectedEdgeId: string|null
  contextIds?: string[]; contextLabel?: string; onExitContext: () => void
  nodes: GraphNode[]; edges: GraphEdge[]; selectedId: string; onSelect: (id: string) => void
  t: Copy; colorMode: Mode; onColorMode: (mode: Mode) => void; motion: boolean; onMotion: () => void
}
const modeIcons = [Activity, Network, Layers3]

export function DesignNetwork({ language, nodes, edges, selectedId, onSelect, t, colorMode, onColorMode, motion, onMotion, limit, contextIds, contextLabel, onExitContext, trace, onClearTrace, onSelectEdge, selectedEdgeId }: Props) {
  const tr = (text: string, values: Record<string,string|number> = {}) => translate(language,text,values)
  const container = useRef<HTMLDivElement>(null)
  const flowCanvas = useRef<HTMLCanvasElement>(null)
  const graph = useRef<Core | null>(null)
  const topology = useRef('')
  const [view, setView] = useState<'top'|'neighbors'|'all'>('neighbors')
  const previousLimit = useRef(limit)
  // Loading more from the priority list also returns the canvas to that list.
  useEffect(() => {
    if (previousLimit.current !== limit) setView('top')
    previousLimit.current = limit
  }, [limit])
  const visible = useMemo(() => (contextIds || trace) ? { nodes, edges } : selectGraphView(nodes, edges, selectedId, view, limit), [nodes, edges, selectedId, view, limit, contextIds, trace])
  const handler = useRef(onSelect)
  handler.current = onSelect
  const edgeHandler = useRef(onSelectEdge)
  edgeHandler.current = onSelectEdge

  useEffect(() => {
    if (!container.current) return
    const cy = cytoscape({
      container: container.current, elements: [], layout: { name: 'preset' },
      minZoom: .02, maxZoom: 3, pixelRatio: Math.min(window.devicePixelRatio, 2),
      style: [
        { selector: 'node', style: {
          'background-color': 'data(color)', 'background-opacity': 1,
          shape: 'ellipse',
          'border-width': 0, width: 16, height: 16, label: '', color: '#b9c3d9',
          'font-size': 12, 'min-zoomed-font-size': 9, 'text-valign': 'bottom', 'text-margin-y': 8,
          'text-background-color': '#0b1120', 'text-background-opacity': .9, 'text-background-padding': '4px',
        } },
        { selector: 'node:selected', style: { width: 28, height: 28, 'border-color': '#bdadff', 'border-width': 1.5,
          'font-weight': 600, color: '#fff', 'overlay-color': 'data(color)', 'overlay-opacity': .09, 'overlay-padding': 12 } },
        { selector: 'node:selected, node.hovered', style: { label: 'data(label)' } },
        { selector: 'node.seed', style: { 'border-width': 3, 'border-color': '#ecedb8' } },
        { selector: 'node.boundary', style: { 'border-width': 2, 'border-style': 'dashed', 'border-color': '#afbab0' } },
        { selector: 'node.isolated', style: { 'background-opacity': 0, 'border-width': 1, 'border-color': '#afbab0' } },
        { selector: 'edge', style: { width: 1.5, 'line-color': 'data(color)', 'target-arrow-color': 'data(color)',
          'target-arrow-shape': 'triangle', 'arrow-scale': .75, 'curve-style': 'unbundled-bezier',
          'control-point-distances': 22, 'control-point-weights': .5, opacity: .22 } },
        { selector: 'node.priority-focus', style: { width:26, height:26, 'border-color':'#c2b5ff', 'border-width':3, 'border-style':'solid' } },
        { selector: 'edge.context-link', style: { opacity:.4 } },
        { selector: 'node.context', style: { opacity: .35 } },
        { selector: 'edge.focused', style: { width: 2.2, opacity: .75 } },
        { selector: 'edge.trace-edge', style: { width:2.5, opacity:1, 'curve-style':'straight', 'line-color':'#b6a0f4', 'target-arrow-color':'#b6a0f4' } },
        { selector: 'edge.inspected', style: { width:4, opacity:1, 'line-color':'#f0d187', 'target-arrow-color':'#f0d187' } },
        { selector: 'node.trace-node', style: { label:'data(label)', opacity:1, 'text-valign':'center', 'text-halign':'right', 'text-margin-x':14, 'text-margin-y':0, 'font-size':11 } },
        { selector: 'edge.hovered', style: { width: 3, opacity: 1, label: 'data(amount)', color: '#eef0fa',
          'font-size': 12, 'text-background-color': '#10182a', 'text-background-opacity': 1, 'text-background-padding': '5px' } },
      ],
    })
    graph.current = cy
    cy.on('tap', 'edge', event => edgeHandler.current(event.target.id()))
    cy.on('tap', 'node', event => handler.current(event.target.id()))
    cy.on('mouseover', 'node', event => event.target.addClass('hovered'))
    cy.on('mouseout', 'node', event => event.target.removeClass('hovered'))
    cy.on('mouseover', 'edge', event => event.target.addClass('hovered'))
    cy.on('mouseout', 'edge', event => event.target.removeClass('hovered'))
    const observer = new ResizeObserver(() => { cy.resize(); cy.fit(undefined, 28) })
    observer.observe(container.current)
    return () => { observer.disconnect(); cy.destroy(); graph.current = null; topology.current = '' }
  }, [])

  useEffect(() => {
    const cy = graph.current
    if (!cy) return
    const color = (node: GraphNode) => colorMode === 'priority' ? riskColors[riskIndex(node.priorityScore)]
      : colorMode === 'cluster' ? getClusterColor(node.clusterId) : roleMeta[node.role].color
    const byId = new Map(visible.nodes.map(node => [node.id, node]))
    const signature = (trace ? 'trace:' + trace.nodeIds.join(',') : '') + visible.nodes.map(n=>n.id).sort().join(',') + '|' + visible.edges.map(e=>e.id).sort().join(',')
    const changed = signature !== topology.current
    const positions = new Map<string, {x:number; y:number}>()
    if (!changed) cy.nodes().forEach(n => { positions.set(n.id(), n.position()) })
    cy.batch(() => {
      cy.elements().remove()
      cy.add([
        ...visible.nodes.map(node => ({ data: { id: node.id, label: node.gid, color: color(node) }, classes: [node.isSeed?'seed':'',node.isBoundary?'boundary':'',node.isIsolated?'isolated':'',trace?'trace-node':''].join(' '), position: positions.get(node.id) || { x: node.x, y: node.y } })),
        ...visible.edges.filter(edge => byId.has(edge.source) && byId.has(edge.target)).map(edge => ({ data: { ...edge, color: color(byId.get(edge.source)!) }, classes:trace?'trace-edge':'' })),
      ])
    })
    if (changed && visible.nodes.length) {
      // Layout only the visible subgraph; large overviews use a cheap grid.
      if (trace) {
        trace.nodeIds.forEach((id,i)=>cy.getElementById(id).position({x:0,y:i*110}))
        cy.fit(undefined, 60)
        if(cy.zoom()>1.4)cy.zoom({level:1.4,renderedPosition:{x:cy.width()/2,y:cy.height()/2}})
      } else cy.layout(visible.nodes.length <= (contextIds ? 600 : 300)
          ? { name:'cose', animate:false, randomize:false, fit:true, padding:40, nodeRepulsion:8000, idealEdgeLength:90, nodeOverlap:20, componentSpacing:100, numIter:350 }
          : { name:'grid', fit:true, padding:40, avoidOverlap:true }).run()
    }
    topology.current = signature
  }, [visible, colorMode])

  useEffect(() => {
    const cy = graph.current
    if (!cy) return
    cy.nodes().unselect().removeClass('context'); cy.edges().removeClass('focused')
    const node = cy.getElementById(selectedId)
    node.select(); node.connectedEdges().addClass('focused')
    if (node.length && !contextIds && !trace) { cy.nodes().addClass('context'); node.closedNeighborhood().removeClass('context') }
    cy.nodes().removeClass('priority-focus trace-node'); cy.edges().removeClass('context-link trace-edge inspected')
    if(trace){cy.nodes().addClass('trace-node');cy.edges().addClass('trace-edge')}
    if(selectedEdgeId)cy.getElementById(selectedEdgeId).addClass('inspected')
    if(contextIds) { contextIds.forEach(id=>cy.getElementById(id).addClass('priority-focus')); cy.edges().addClass('context-link') }
  }, [selectedId, visible, colorMode, contextIds, trace, selectedEdgeId])

  useEffect(() => {
    if (!graph.current || !flowCanvas.current || !container.current) return
    return attachFlowAnimation(graph.current, flowCanvas.current, container.current, motion && visible.nodes.length <= 100)
  }, [motion, visible.nodes.length])

  const zoomBy = (step: number) => {
    const cy = graph.current
    if (cy) cy.zoom({ level: Math.max(.02, Math.min(3, cy.zoom() * (step > 0 ? 1.5 : 1/1.5))), renderedPosition: { x: cy.width() / 2, y: cy.height() / 2 } })
  }

  return <div className="design-network">
    <div className="network-toolbar">
      <div className="view-modes">{(['priority', 'role', 'cluster'] as Mode[]).map((mode, index) => {
        const Icon = modeIcons[index]
        return <button key={mode} aria-pressed={colorMode === mode} onClick={() => onColorMode(mode)}><Icon size={12}/>{[t.signals, t.roles, t.clusters][index]}</button>
      })}</div>
      <div className="network-controls">
        {!contextIds && !trace && <><button className="neighborhood-button" aria-label={tr("Связи выбранного узла")} aria-pressed={view==='neighbors'} onClick={() => setView(v=>v==='neighbors'?'top':'neighbors')}>{tr("Связи узла")}</button>
        <button className="full-graph-button" aria-pressed={view==='all'} onClick={() => setView(v=>v==='all'?'top':'all')}>{view==='all'?tr("Топ-{n}",{n:limit}):tr("Все узлы")}</button></>}
        {trace && <button className="full-graph-button" onClick={onClearTrace}>{tr("Вернуться к сети")}</button>}
        {contextIds && <button className="full-graph-button" onClick={onExitContext}>{tr("Сбросить уровень")}</button>}
        <button disabled={visible.nodes.length > 100} aria-label={motion ? t.pause : t.play} aria-pressed={motion} onClick={onMotion}>{motion ? <Pause size={14}/> : <Play size={14}/>}</button>
        <button aria-label={t.zoomOut} onClick={() => zoomBy(-.2)}><Minus size={15}/></button>
        <button aria-label={t.zoomIn} onClick={() => zoomBy(.2)}><Plus size={15}/></button>
        <button aria-label={t.fit} onClick={() => graph.current?.fit(undefined, 28)}><Maximize2 size={15}/></button>
      </div>
    </div>
    {trace && <div className="graph-context-note"><b>{tr("Направленная цепочка · {n} связей", {n:trace.edgeIds.length})}</b><span>{tr("Нажмите на связь, чтобы открыть факты")}</span></div>}
    {contextIds && <div className="graph-context-note"><span><b>{contextLabel}: {contextIds.length}</b> · {tr("все непосредственные соседи и связи между ними")}</span><span>{tr("Обведённые узлы — выбранный уровень")}</span></div>}
    <div className="network-viewport">
      <div className="cy-container" ref={container}/>
      <canvas ref={flowCanvas} className="flow-canvas" aria-hidden="true"/>
      {!visible.nodes.length && <div className="graph-empty">{t.empty}</div>}
    </div>
    {colorMode !== 'priority' && <div className="network-artwork-legend" aria-label={colorMode === 'role' ? t.roles : t.clusters}>
      {colorMode === 'role' ? roleOrder.map((role, index) => <span key={role}><i className="legend-dot" style={{background:roleMeta[role].color}}/>{t.role[index]}</span>)
        : [...new Set(visible.nodes.map(node => node.clusterId))].sort((a, b) => a - b).map(id => <span key={id}><i className="legend-dot" style={{background:getClusterColor(id)}}/>{t.cluster} #{id}</span>)}
    </div>}
    <div className="network-bottom"><span><i/>{t.direction}</span><span>{trace?tr('Цепочка')+' · ':contextIds?tr('Полное окружение')+' · ':view==='neighbors'?tr('Связи узла')+' · ':view==='top'?tr('Приоритетные')+' · ':''}{tr('{visible} из {total} узлов · {edges} связей',{visible:visible.nodes.length,total:nodes.length,edges:visible.edges.length})}</span></div>
  </div>
}
