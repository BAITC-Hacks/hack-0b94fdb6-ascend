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
  const [searchError, setSearchError] = useState(false)
  const [roleFilter, setRoleFilter] = useState<Role | 'all'>('all')
  const [clusterFilter, setClusterFilter] = useState('all')
  const [clusterView, setClusterView] = useState(false)
  const selectedNode = mockNodes.find((node) => node.id === selectedId) ?? mockNodes[0]
  const filteredNodes = useMemo(() => mockNodes.filter((node) => (roleFilter === 'all' || node.role === roleFilter) && (clusterFilter === 'all' || String(node.clusterId) === clusterFilter)).sort((a, b) => b.priorityScore - a.priorityScore), [roleFilter, clusterFilter])
  const search = () => { const found = mockNodes.find((node) => node.gid.toLowerCase() === query.trim().toLowerCase()); if (found) { setSelectedId(found.id); setSearchError(false) } else setSearchError(Boolean(query.trim())) }
  const downloadCsv = (type: 'nodes' | 'clusters' | 'top') => {
    const rows = type === 'nodes'
      ? ['gid,role,role_score,cluster_id,priority_score,evidence', ...mockNodes.map((node) => `${node.gid},${node.role},${node.roleScore},${node.clusterId},${node.priorityScore},"${node.evidence.replaceAll('"', '""')}"`)]
      : type === 'clusters'
        ? ['cluster_id,n_nodes,n_seed,sum_kzt_internal,top_gids,hypothesis', '1,624,22,98200000,"703118;551920","Периферийный кластер с ограниченным числом связей"', '2,713,28,121400000,"882104;120934","Кластер со связующими узлами между потоками"', '3,911,31,146290012,"192831;203472;104882","Плотный кластер с консолидацией и распределением наблюдаемого потока"']
        : ['rank,gid,role,priority_score,why', ...[...mockNodes].sort((a, b) => b.priorityScore - a.priorityScore).map((node, index) => `${index + 1},${node.gid},${node.role},${node.priorityScore},"${node.evidence.replaceAll('"', '""')}"`)]
    const fileName = type === 'nodes' ? 'nodes_roles.csv' : type === 'clusters' ? 'clusters.csv' : 'top_nodes.csv'
    const url = URL.createObjectURL(new Blob([`\uFEFF${rows.join('\n')}`], { type: 'text/csv;charset=utf-8' }))
    const link = document.createElement('a')
    link.href = url
    link.download = fileName
    link.click()
    URL.revokeObjectURL(url)
  }
  return <div className="app-shell"><Header query={query} onQueryChange={(value) => { setQuery(value); setSearchError(false) }} onSubmit={search} searchError={searchError} onDownload={downloadCsv} /><main className="dashboard-grid"><Sidebar nodes={filteredNodes} selectedId={selectedId} roleFilter={roleFilter} clusterFilter={clusterFilter} onSelect={setSelectedId} onRoleFilter={setRoleFilter} onClusterFilter={setClusterFilter} /><NetworkGraph nodes={mockNodes} edges={mockEdges} selectedId={selectedId} onSelect={setSelectedId} query={query} clusterView={clusterView} onToggleClusterView={() => setClusterView((value) => !value)} /><NodeDetails node={selectedNode} /></main></div>
}

export default App
