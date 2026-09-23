import type { GraphNode, GraphEdge } from './types/graph'

/** One-hop union, including every real edge between the included nodes. */
export function selectNodeContext(nodes: GraphNode[], edges: GraphEdge[], focusIds: string[]) {
  const focus = new Set(focusIds)
  const included = new Set(focus)
  for (const edge of edges) {
    if (focus.has(edge.source) || focus.has(edge.target)) {
      included.add(edge.source)
      included.add(edge.target)
    }
  }
  const shown = nodes.filter(n => included.has(n.id))
  const ids = new Set(shown.map(n => n.id))
  return { nodes: shown, edges: edges.filter(e => ids.has(e.source) && ids.has(e.target)) }
}

/** Bound the actual Cytoscape dataset, not merely the visibility of its elements. */
export function selectGraphView(nodes: GraphNode[], edges: GraphEdge[], selectedId: string, mode: 'top' | 'neighbors' | 'all', limit = 100) {
  if (mode === 'all') return { nodes, edges }
  const neighbors = new Set([selectedId])
  if (mode === 'neighbors') for (const edge of edges) {
    if (edge.source === selectedId) neighbors.add(edge.target)
    if (edge.target === selectedId) neighbors.add(edge.source)
  }
  const candidates = nodes.filter(n => mode !== 'neighbors' || neighbors.has(n.id))
    .sort((a, b) => b.priorityScore - a.priorityScore || a.id.localeCompare(b.id))
  const selected = candidates.find(n => n.id === selectedId)
  const shown = selected
    ? [selected, ...candidates.filter(n => n.id !== selectedId).slice(0, limit - 1)]
    : candidates.slice(0, limit)
  const ids = new Set(shown.map(n => n.id))
  return { nodes: shown, edges: edges.filter(e => ids.has(e.source) && ids.has(e.target)) }
}
