import { useEffect, useRef } from 'react'
import CytoscapeComponent from 'react-cytoscapejs'
import { type Core } from 'cytoscape'
import { Activity, CircleDotDashed, Maximize2, Minus, Plus, RotateCcw, ScanSearch } from 'lucide-react'
import type { GraphEdge, GraphNode } from '../types/graph'
import { getClusterColor, getSignalMeta, roleMeta } from '../data/mockData'

interface NetworkGraphProps {
  nodes: GraphNode[]
  edges: GraphEdge[]
  selectedId: string
  onSelect: (id: string) => void
  query: string
  clusterView: boolean
  onToggleClusterView: () => void
}

export function NetworkGraph({ nodes, edges, selectedId, onSelect, query, clusterView, onToggleClusterView }: NetworkGraphProps) {
  const cyRef = useRef<Core | null>(null)
  const resetViewport = () => {
    const cy = cyRef.current
    if (!cy) return
    cy.viewport({ zoom: 1, pan: { x: 0, y: 0 } })
  }

  useEffect(() => {
    if (!query || !cyRef.current) return
    const found = nodes.find((node) => node.gid.toLowerCase() === query.trim().toLowerCase())
    if (!found) return
    const target = cyRef.current.$(`#${found.id}`)
    target.select()
    cyRef.current.animate({ center: { eles: target }, zoom: 1.5 }, { duration: 450 })
  }, [query, nodes])

  useEffect(() => {
    const cy = cyRef.current
    if (!cy) return
    cy.nodes().unselect()
    cy.$(`#${selectedId}`).select()
  }, [selectedId])

  const nodeById = new Map(nodes.map((node) => [node.id, node]))
  const elements = [
    ...nodes.map((node) => {
      const signal = getSignalMeta(node.priorityScore)
      return { data: { id: node.id, label: node.gid, color: clusterView ? getClusterColor(node.clusterId) : roleMeta[node.role].color, signalColor: signal.color, size: node.priorityScore >= .85 ? 29 : node.priorityScore >= .70 ? 24 : 20 }, position: { x: node.x * 7.8, y: node.y * 5.4 } }
    }),
    ...edges.map((edge) => {
      const source = nodeById.get(edge.source)
      return { data: { id: edge.id, source: edge.source, target: edge.target, amount: edge.amount, color: source ? (clusterView ? getClusterColor(source.clusterId) : roleMeta[source.role].color) : '#46505e' } }
    }),
  ]

  const selectedNode = nodeById.get(selectedId)
  return <section className="graph-panel">
    <div className="graph-topbar"><div><p className="eyebrow">НАБЛЮДАЕМАЯ СЕТЬ</p><h2>Топология переводов <span className="live-dot" /> <span className="live-label">LIVE</span></h2></div><div className="graph-actions"><button className={`graph-view-toggle ${clusterView ? 'is-active' : ''}`} onClick={onToggleClusterView} aria-pressed={clusterView}><CircleDotDashed size={14} />{clusterView ? 'Кластеры' : 'Роли'}</button><button className="icon-button" onClick={resetViewport} aria-label="Показать весь граф"><Maximize2 size={16} /></button><button className="icon-button" onClick={() => cyRef.current?.zoom((cyRef.current?.zoom() ?? 1) + 0.2)} aria-label="Увеличить"><Plus size={16} /></button><button className="icon-button" onClick={() => cyRef.current?.zoom(Math.max(.4, (cyRef.current?.zoom() ?? 1) - 0.2))} aria-label="Уменьшить"><Minus size={16} /></button><button className="icon-button" onClick={() => { cyRef.current?.reset(); resetViewport() }} aria-label="Сбросить вид"><RotateCcw size={15} /></button></div></div>
    <div className="graph-stage"><div className="graph-scan" aria-hidden="true" /><div className="graph-telemetry" aria-hidden="true"><span className="graph-telemetry__status"><Activity size={13} /> Мониторинг потоков</span><span className="graph-telemetry__packet graph-telemetry__packet--one" /><span className="graph-telemetry__packet graph-telemetry__packet--two" /><span className="graph-telemetry__packet graph-telemetry__packet--three" /></div><div className="graph-focus-card"><span className="graph-focus-card__icon"><ScanSearch size={14} /></span><div><span>Текущий фокус</span><strong>{selectedNode ? `GID ${selectedNode.gid}` : 'Нет выбора'}</strong></div></div><div className="graph-canvas"><CytoscapeComponent cy={(cy: Core) => { cyRef.current = cy; if (cy.data('interactionsBound')) return; cy.data('interactionsBound', true); const normalizeViewport = () => cy.viewport({ zoom: 1, pan: { x: 0, y: 0 } }); cy.one('layoutstop', normalizeViewport); cy.on('tap', 'node', (event: any) => onSelect(event.target.id())); cy.on('mouseover', 'edge', (event: any) => event.target.addClass('is-hovered')); cy.on('mouseout', 'edge', (event: any) => event.target.removeClass('is-hovered')) }} elements={elements} stylesheet={[{ selector: 'node', style: { 'background-color': 'data(color)', label: 'data(label)', color: '#eef3f4', 'font-size': 10, 'font-family': 'ui-sans-serif, system-ui, sans-serif', 'text-valign': 'bottom', 'text-margin-y': 9, width: 'data(size)', height: 'data(size)', 'border-width': 3, 'border-color': 'data(signalColor)' } }, { selector: 'node:selected', style: { 'border-width': 5, 'border-color': '#f4fbfa', width: 32, height: 32, 'font-size': 12, 'font-weight': 700 } }, { selector: 'edge', style: { width: 1.4, 'line-color': 'data(color)', 'target-arrow-color': 'data(color)', 'target-arrow-shape': 'triangle', 'curve-style': 'bezier', opacity: .42, label: 'data(amount)', color: '#7e8c98', 'font-size': 8, 'text-background-color': '#0d1118', 'text-background-opacity': .85, 'text-background-padding': 3 } }, { selector: 'edge.is-hovered', style: { width: 2.5, opacity: .95, color: '#e9eff2', 'font-size': 9 } }]} layout={{ name: 'preset', fit: false, padding: 0 }} style={{ width: '100%', height: '100%' }} /></div></div>
    <div className="graph-footer"><span><i className="edge-swatch" /> плательщик → получатель</span><span><i className="node-swatch" /> {clusterView ? 'кластер + сигнал приоритета' : 'роль + сигнал приоритета'}</span><span className="graph-hint">Колесо — масштаб · перетаскивание — перемещение</span></div>
  </section>
}
