import { SlidersHorizontal } from 'lucide-react'
import type { GraphNode, Role } from '../types/graph'
import { roleMeta } from '../data/mockData'

interface SidebarProps {
  nodes: GraphNode[]
  selectedId: string
  roleFilter: Role | 'all'
  clusterFilter: string
  onSelect: (id: string) => void
  onRoleFilter: (value: Role | 'all') => void
  onClusterFilter: (value: string) => void
}

export function Sidebar({ nodes, selectedId, roleFilter, clusterFilter, onSelect, onRoleFilter, onClusterFilter }: SidebarProps) {
  return <aside className="sidebar">
    <div className="panel-heading"><div><p className="eyebrow">WATCHLIST</p><h2>Priority Nodes</h2></div><span className="count-badge">{nodes.length}</span></div>
    <p className="panel-description">Highest-signal entities across the transaction network.</p>
    <div className="filter-row"><div className="select-wrap"><SlidersHorizontal size={14} /><select value={roleFilter} onChange={(e) => onRoleFilter(e.target.value as Role | 'all')}><option value="all">All roles</option>{Object.entries(roleMeta).map(([key, meta]) => <option key={key} value={key}>{meta.label}</option>)}</select></div><select className="compact-select" value={clusterFilter} onChange={(e) => onClusterFilter(e.target.value)}><option value="all">All clusters</option><option value="1">#1</option><option value="2">#2</option><option value="3">#3</option></select></div>
    <div className="nodes-list">{nodes.map((node, index) => <button className={`priority-node ${selectedId === node.id ? 'is-selected' : ''}`} key={node.id} onClick={() => onSelect(node.id)}><span className="rank">{String(index + 1).padStart(2, '0')}</span><span className="node-copy"><span className="node-gid">GID {node.gid}</span><span className="node-role"><i style={{ backgroundColor: roleMeta[node.role].color }} />{roleMeta[node.role].label}</span></span><span className="priority-score"><strong>{node.priorityScore}</strong><small>priority</small></span></button>)}</div>
    <div className="legend"><p className="eyebrow">ROLE LEGEND</p><div className="legend-grid">{Object.entries(roleMeta).map(([key, meta]) => <span key={key}><i style={{ backgroundColor: meta.color }} />{meta.label}</span>)}</div></div>
  </aside>
}
