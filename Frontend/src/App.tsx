import { useMemo, useState } from 'react'
import { Header } from './components/Header'
import { NetworkGraph } from './components/NetworkGraph'
import { NodeDetails } from './components/NodeDetails'
import { Sidebar } from './components/Sidebar'
import { mockEdges, mockNodes } from './data/mockData'
import type { Role } from './types/graph'
import './styles.css'

function App() {
  const [selectedId, setSelectedId] = useState(mockNodes[0].id)
  const [query, setQuery] = useState('')
  const [roleFilter, setRoleFilter] = useState<Role | 'all'>('all')
  const [clusterFilter, setClusterFilter] = useState('all')
  const selectedNode = mockNodes.find((node) => node.id === selectedId) ?? mockNodes[0]
  const filteredNodes = useMemo(() => mockNodes.filter((node) => (roleFilter === 'all' || node.role === roleFilter) && (clusterFilter === 'all' || String(node.clusterId) === clusterFilter)).sort((a, b) => b.priorityScore - a.priorityScore), [roleFilter, clusterFilter])
  const search = () => { const found = mockNodes.find((node) => node.gid.toLowerCase() === query.trim().toLowerCase()); if (found) setSelectedId(found.id) }
  return <div className="app-shell"><Header query={query} onQueryChange={setQuery} onSubmit={search} /><main className="dashboard-grid"><Sidebar nodes={filteredNodes} selectedId={selectedId} roleFilter={roleFilter} clusterFilter={clusterFilter} onSelect={setSelectedId} onRoleFilter={setRoleFilter} onClusterFilter={setClusterFilter} /><NetworkGraph nodes={mockNodes} edges={mockEdges} selectedId={selectedId} onSelect={setSelectedId} query={query} /><NodeDetails node={selectedNode} /></main></div>
}

export default App
