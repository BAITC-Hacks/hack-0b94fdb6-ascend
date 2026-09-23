import { SlidersHorizontal } from 'lucide-react'
import type { GraphNode, Role } from '../types/graph'
import { formatScore, roleMeta } from '../data/mockData'
import { EntitySignalIcon, SignalBadge } from './EntitySignalIcon'

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
    <div className="panel-heading"><div><p className="eyebrow">ПРИОРИТЕТ ПРОВЕРКИ</p><h2>Top-N узлов</h2></div><span className="count-badge">{nodes.length}</span></div>
    <p className="panel-description">Клиенты с наиболее значимым аналитическим сигналом в наблюдаемой сети.</p>
    <div className="filter-row"><div className="select-wrap"><SlidersHorizontal size={14} /><select value={roleFilter} onChange={(e) => onRoleFilter(e.target.value as Role | 'all')}><option value="all">Все роли</option>{Object.entries(roleMeta).map(([key, meta]) => <option key={key} value={key}>{meta.label}</option>)}</select></div><select className="compact-select" value={clusterFilter} onChange={(e) => onClusterFilter(e.target.value)}><option value="all">Кластеры</option><option value="1">#1</option><option value="2">#2</option><option value="3">#3</option></select></div>
    {nodes.length ? <div className="nodes-list">{nodes.map((node, index) => <button className={`priority-node ${selectedId === node.id ? 'is-selected' : ''}`} key={node.id} onClick={() => onSelect(node.id)}><span className="rank">{String(index + 1).padStart(2, '0')}</span><EntitySignalIcon priorityScore={node.priorityScore} size={29} animate={selectedId === node.id} /><span className="node-copy"><span className="node-gid">GID {node.gid}</span><span className="node-role"><i style={{ backgroundColor: roleMeta[node.role].color }} />{roleMeta[node.role].label}</span></span><span className="priority-score"><strong>{formatScore(node.priorityScore)}</strong><SignalBadge priorityScore={node.priorityScore} /></span></button>)}</div> : <div className="empty-filter">Нет узлов с выбранными фильтрами. Сбросьте роль или кластер.</div>}
    <div className="legend"><p className="eyebrow">ЛЕГЕНДА РОЛЕЙ</p><div className="legend-grid">{Object.entries(roleMeta).map(([key, meta]) => <span key={key}><i style={{ backgroundColor: meta.color }} />{meta.label}</span>)}</div></div>
  </aside>
}
