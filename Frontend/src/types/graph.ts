export type Role = 'consolidator' | 'transit' | 'distributor' | 'terminal' | 'coordinator' | 'peripheral'

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
}

export interface GraphEdge {
  id: string
  source: string
  target: string
  amount: string
  label?: string
}
