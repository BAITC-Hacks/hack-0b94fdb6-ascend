import type { GraphNode, GraphEdge } from './types/graph'

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
