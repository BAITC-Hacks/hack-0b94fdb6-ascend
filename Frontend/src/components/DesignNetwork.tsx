import { useEffect, useRef } from 'react'
import cytoscape, { type Core } from 'cytoscape'
import { Maximize2, Minus, Plus, Pause, Play, Activity, Network, Layers3 } from 'lucide-react'
import type { GraphEdge, GraphNode } from '../types/graph'
import { getClusterColor, roleMeta } from '../data/mockData'
import { riskColors, riskIndex, roleOrder, type Copy } from '../i18n'
import { getNodeArtwork, getClusterArtwork, roleArtwork } from '../data/networkArtwork'
import { KazakhstanMap } from './KazakhstanMap'
import { attachFlowAnimation } from './flowAnimation'

type Mode = 'priority' | 'role' | 'cluster'
interface Props {
  nodes: GraphNode[]; edges: GraphEdge[]; selectedId: string; onSelect: (id: string) => void
  t: Copy; colorMode: Mode; onColorMode: (mode: Mode) => void; motion: boolean; onMotion: () => void
}
const modeIcons = [Activity, Network, Layers3]

export function DesignNetwork({ nodes, edges, selectedId, onSelect, t, colorMode, onColorMode, motion, onMotion }: Props) {
  const container = useRef<HTMLDivElement>(null)
  const mapScene = useRef<SVGGElement>(null)
  const flowCanvas = useRef<HTMLCanvasElement>(null)
  const graph = useRef<Core | null>(null)
  const handler = useRef(onSelect)
  handler.current = onSelect

  useEffect(() => {
    if (!container.current) return
    const cy = cytoscape({
      container: container.current, elements: [], layout: { name: 'preset' },
      minZoom: .25, maxZoom: 3, pixelRatio: Math.min(window.devicePixelRatio, 2),
      style: [
        { selector: 'node', style: {
          'background-color': '#102019', 'background-opacity': 0, 'background-image': 'data(portrait)', 'background-fit': 'contain',
          shape: 'round-rectangle',
          'border-width': 0, width: 38, height: 38, label: 'data(label)', color: '#c4d6c9',
          'font-size': 12, 'text-valign': 'bottom', 'text-margin-y': 8,
          'text-background-color': '#0a1710', 'text-background-opacity': .9, 'text-background-padding': '4px',
        } },
        { selector: 'node:selected', style: { width: 48, height: 48, 'border-color': '#d8edbb', 'border-width': 1.5,
          'font-weight': 600, color: '#fff', 'overlay-color': 'data(color)', 'overlay-opacity': .09, 'overlay-padding': 12 } },
        { selector: 'edge', style: { width: 1.2, 'line-color': 'data(color)', 'target-arrow-color': 'data(color)',
          'target-arrow-shape': 'triangle', 'arrow-scale': .75, 'curve-style': 'unbundled-bezier',
          'control-point-distances': 35, 'control-point-weights': .5, opacity: .3 } },
        { selector: 'edge.focused', style: { width: 2.2, opacity: .75 } },
        { selector: 'edge.hovered', style: { width: 3, opacity: 1, label: 'data(amount)', color: '#effff5',
          'font-size': 12, 'text-background-color': '#091711', 'text-background-opacity': 1, 'text-background-padding': '5px' } },
      ],
    })
    graph.current = cy
    cy.on('tap', 'node', event => handler.current(event.target.id()))
    cy.on('mouseover', 'edge', event => event.target.addClass('hovered'))
    cy.on('mouseout', 'edge', event => event.target.removeClass('hovered'))
    const syncMap = () => {
      const pan = cy.pan()
      mapScene.current?.setAttribute('transform', `translate(${pan.x} ${pan.y}) scale(${cy.zoom()})`)
    }
    cy.on('pan zoom resize', syncMap)
    const observer = new ResizeObserver(() => { cy.resize(); cy.fit(undefined, 28); syncMap() })
    observer.observe(container.current)
    return () => { observer.disconnect(); cy.destroy(); graph.current = null }
  }, [])

  useEffect(() => {
    const cy = graph.current
    if (!cy) return
    const color = (node: GraphNode) => colorMode === 'priority' ? riskColors[riskIndex(node.priorityScore)]
      : colorMode === 'cluster' ? getClusterColor(node.clusterId) : roleMeta[node.role].color
    const byId = new Map(nodes.map(node => [node.id, node]))
    cy.batch(() => {
      cy.elements().remove()
      cy.add([
        ...nodes.map(node => ({ data: { id: node.id, label: node.gid, color: color(node), portrait: getNodeArtwork(node, colorMode) }, position: { x: node.x * 8, y: node.y * 6 } })),
        ...edges.filter(edge => byId.has(edge.source) && byId.has(edge.target)).map(edge => ({ data: { ...edge, color: color(byId.get(edge.source)!) } })),
      ])
    })
    cy.fit(undefined, 28)
  }, [nodes, edges, colorMode])

  useEffect(() => {
    const cy = graph.current
    if (!cy) return
    cy.nodes().unselect(); cy.edges().removeClass('focused')
    const node = cy.getElementById(selectedId)
    node.select(); node.connectedEdges().addClass('focused')
    if (node.length) cy.stop().animate({ center: { eles: node } }, { duration: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 0 : 350 })
  }, [selectedId, nodes, edges, colorMode])

  useEffect(() => {
    if (!graph.current || !flowCanvas.current || !container.current) return
    return attachFlowAnimation(graph.current, flowCanvas.current, container.current, motion)
  }, [motion])

  const zoomBy = (step: number) => {
    const cy = graph.current
    if (cy) cy.zoom({ level: Math.max(.25, Math.min(3, cy.zoom() + step)), renderedPosition: { x: cy.width() / 2, y: cy.height() / 2 } })
  }

  return <div className="design-network">
    <div className="network-toolbar">
      <div className="view-modes">{(['priority', 'role', 'cluster'] as Mode[]).map((mode, index) => {
        const Icon = modeIcons[index]
        return <button key={mode} aria-pressed={colorMode === mode} onClick={() => onColorMode(mode)}><Icon size={12}/>{[t.signals, t.roles, t.clusters][index]}</button>
      })}</div>
      <div className="network-controls">
        <button aria-label={motion ? t.pause : t.play} aria-pressed={motion} onClick={onMotion}>{motion ? <Pause size={14}/> : <Play size={14}/>}</button>
        <button aria-label={t.zoomOut} onClick={() => zoomBy(-.2)}><Minus size={15}/></button>
        <button aria-label={t.zoomIn} onClick={() => zoomBy(.2)}><Plus size={15}/></button>
        <button aria-label={t.fit} onClick={() => graph.current?.fit(undefined, 28)}><Maximize2 size={15}/></button>
      </div>
    </div>
    <div className="network-viewport">
      <KazakhstanMap sceneRef={mapScene}/>
      <div className="map-aura" aria-hidden="true"/>
      <div className="cy-container" ref={container}/>
      <canvas ref={flowCanvas} className="flow-canvas" aria-hidden="true"/>
      {!nodes.length && <div className="graph-empty">{t.empty}</div>}
    </div>
    {colorMode !== 'priority' && <div className="network-artwork-legend" aria-label={colorMode === 'role' ? t.roles : t.clusters}>
      {colorMode === 'role' ? roleOrder.map((role, index) => <span key={role}><img src={roleArtwork[role]} alt="" width="24" height="24"/>{t.role[index]}</span>)
        : [...new Set(nodes.map(node => node.clusterId))].sort((a, b) => a - b).map(id => <span key={id}><img src={getClusterArtwork(id)} alt="" width="24" height="24"/>{t.cluster} #{id}</span>)}
    </div>}
    <div className="network-bottom"><span><i/>{t.direction}</span><span>{nodes.length} {t.nodes.toLowerCase()} · {edges.length} {t.edges.toLowerCase()}</span></div>
  </div>
}
