export type Role = 'consolidator' | 'transit' | 'distributor' | 'terminal' | 'coordinator' | 'peripheral'
export type SignalLevel = 'high' | 'elevated' | 'review' | 'background'

export interface SignalMeta {
  level: SignalLevel
  label: string
  shortLabel: string
  color: string
  softColor: string
}

export interface GraphNode {
  id: string
  gid: string
  role: Role
  roleScore: number
  priorityScore: number
  clusterId: number
  incoming: number
  outgoing: number
  received: string
  sent: string
  evidence: string
  x: number
  y: number
  highlighted?: boolean
  isSeed?: boolean
  isBoundary?: boolean
  isIsolated?: boolean
}

export interface GraphEdge {
  id: string
  source: string
  target: string
  amount: string
  label?: string
  sumKzt?: number
  transactions?: number
  firstDate?: string | null
  lastDate?: string | null
}
