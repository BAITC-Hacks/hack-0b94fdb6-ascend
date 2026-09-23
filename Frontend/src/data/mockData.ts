import type { GraphEdge, GraphNode } from '../types/graph'

export const mockNodes: GraphNode[] = [
  { id: 'n192831', gid: '192831', role: 'consolidator', roleScore: 91, priorityScore: 94, clusterId: 3, incoming: 14, outgoing: 2, received: '₸8.3M', sent: '₸7.9M', evidence: 'Receives funds from 14 unique clients and sends most of the volume to only two recipients.', x: 50, y: 49 },
  { id: 'n203472', gid: '203472', role: 'transit', roleScore: 87, priorityScore: 91, clusterId: 3, incoming: 8, outgoing: 8, received: '₸5.1M', sent: '₸5.0M', evidence: 'High-throughput pass-through behavior with a median holding time under 4 hours.', x: 63, y: 33 },
  { id: 'n104882', gid: '104882', role: 'distributor', roleScore: 83, priorityScore: 86, clusterId: 3, incoming: 3, outgoing: 11, received: '₸4.7M', sent: '₸4.6M', evidence: 'Splits incoming volume across 11 counterparties in a balanced fan-out pattern.', x: 75, y: 58 },
  { id: 'n882104', gid: '882104', role: 'coordinator', roleScore: 78, priorityScore: 79, clusterId: 2, incoming: 9, outgoing: 7, received: '₸3.2M', sent: '₸3.1M', evidence: 'Bridges two dense clusters and repeatedly reconnects the same transaction paths.', x: 32, y: 28 },
  { id: 'n441095', gid: '441095', role: 'terminal', roleScore: 74, priorityScore: 71, clusterId: 3, incoming: 5, outgoing: 0, received: '₸2.6M', sent: '₸0', evidence: 'Receives funds from a concentrated set of sources with no observed outgoing flow.', x: 88, y: 35 },
  { id: 'n703118', gid: '703118', role: 'peripheral', roleScore: 61, priorityScore: 54, clusterId: 1, incoming: 1, outgoing: 2, received: '₸740K', sent: '₸612K', evidence: 'Low-degree participant at the edge of cluster activity.', x: 17, y: 68 },
  { id: 'n319420', gid: '319420', role: 'transit', roleScore: 69, priorityScore: 63, clusterId: 3, incoming: 4, outgoing: 5, received: '₸1.9M', sent: '₸1.8M', evidence: 'Moves value onward within a short time window across a recurring path.', x: 42, y: 70 },
  { id: 'n551920', gid: '551920', role: 'peripheral', roleScore: 56, priorityScore: 49, clusterId: 1, incoming: 2, outgoing: 1, received: '₸510K', sent: '₸405K', evidence: 'Small-volume connection to a high-priority neighborhood.', x: 25, y: 50 },
  { id: 'n902441', gid: '902441', role: 'distributor', roleScore: 72, priorityScore: 68, clusterId: 3, incoming: 2, outgoing: 7, received: '₸2.1M', sent: '₸2.0M', evidence: 'Routes value to multiple endpoints with a repeatable distribution pattern.', x: 65, y: 73 },
  { id: 'n120934', gid: '120934', role: 'terminal', roleScore: 66, priorityScore: 59, clusterId: 2, incoming: 3, outgoing: 0, received: '₸1.2M', sent: '₸0', evidence: 'Endpoint node with consistent inbound activity and no outgoing transfers.', x: 78, y: 19 },
]

export const mockEdges: GraphEdge[] = [
  { id: 'e1', source: 'n551920', target: 'n192831', amount: '₸510K' }, { id: 'e2', source: 'n703118', target: 'n192831', amount: '₸740K' }, { id: 'e3', source: 'n882104', target: 'n192831', amount: '₸1.8M' }, { id: 'e4', source: 'n192831', target: 'n203472', amount: '₸3.2M' }, { id: 'e5', source: 'n192831', target: 'n104882', amount: '₸4.7M' }, { id: 'e6', source: 'n203472', target: 'n441095', amount: '₸1.5M' }, { id: 'e7', source: 'n203472', target: 'n104882', amount: '₸1.8M' }, { id: 'e8', source: 'n319420', target: 'n192831', amount: '₸1.9M' }, { id: 'e9', source: 'n104882', target: 'n441095', amount: '₸900K' }, { id: 'e10', source: 'n104882', target: 'n902441', amount: '₸1.1M' }, { id: 'e11', source: 'n902441', target: 'n120934', amount: '₸620K' }, { id: 'e12', source: 'n902441', target: 'n441095', amount: '₸810K' }, { id: 'e13', source: 'n882104', target: 'n319420', amount: '₸640K' }, { id: 'e14', source: 'n319420', target: 'n902441', amount: '₸450K' },
]

export const roleMeta = {
  consolidator: { label: 'Consolidator', color: '#a78bfa' }, transit: { label: 'Transit', color: '#60a5fa' }, distributor: { label: 'Distributor', color: '#fb923c' }, terminal: { label: 'Terminal', color: '#4ade80' }, coordinator: { label: 'Coordinator', color: '#f87171' }, peripheral: { label: 'Peripheral', color: '#8b92a1' },
} as const
