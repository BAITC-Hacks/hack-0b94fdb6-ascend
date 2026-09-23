import type { GraphNode, Role } from './types/graph'

export const API = (import.meta.env.VITE_API_BASE_URL || '/api/v1').replace(/\/$/, '')
export async function api<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(API + path, init)
  const body = await response.json()
  if (!response.ok) throw new Error(body.error?.message || `HTTP ${response.status}`)
  return body as T
}
export type NodeShort = { gid: string; role: Role; role_score: number; priority_score: number; priority_rank: number; cluster_id: number; depth: number; is_seed: boolean; is_boundary: boolean; is_isolated: boolean; x: number; y: number }
export type NodeDetail = NodeShort & { in_deg: number; out_deg: number; in_kzt: number; out_kzt: number; evidence: string }
export type Cluster = { cluster_id: number; n_nodes: number; n_seed: number; sum_kzt_internal: number; top_gids: string[]; hypothesis: string }
export type Overview = { run_id: string | null; _synthetic?: boolean; counts?: { nodes: number; edges: number; clusters: number }; period?: { from: string; to: string }; last_attempt?: { status: string; error?: string } }
export type GraphResponse = { run_id: string; nodes: NodeShort[]; edges: { src: string; dst: string; sum_kzt: number }[] }
export type NodeCard = { node: NodeDetail; evidence_detail: { rule_text: string; limitations: string[]; values: Record<string, unknown> } }
export const money = (value: number) => new Intl.NumberFormat('ru-RU', { maximumFractionDigits: 2 }).format(value) + ' ₸'
export function adaptNode(n: NodeShort, detail?: NodeDetail): GraphNode {
  if (typeof n.gid !== 'string') throw new Error('API вернул gid не строкой')
  return { id: n.gid, gid: n.gid, role: n.role, roleScore: n.role_score, priorityScore: n.priority_score,
    clusterId: n.cluster_id, incoming: detail?.in_deg ?? 0, outgoing: detail?.out_deg ?? 0,
    received: detail ? money(detail.in_kzt) : '—', sent: detail ? money(detail.out_kzt) : '—',
    evidence: detail?.evidence ?? '', x: n.x, y: n.y, isSeed: n.is_seed, isBoundary: n.is_boundary, isIsolated: n.is_isolated }
}
