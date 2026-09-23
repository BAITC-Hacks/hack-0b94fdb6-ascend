/** Contract 2.0 -> current Frontend/src/types/graph.ts view models.
 * Keep raw scores in [0,1] in API/state; multiply only for this percent-based view.
 * /graph NodeShort lacks flows/evidence: hydrate a selected node from /nodes/{gid}.
 */
export interface ContractNode {
  gid: string; role: 'consolidator' | 'transit' | 'distributor' | 'terminal' | 'coordinator' | 'peripheral';
  role_score: number; priority_score: number; cluster_id: number;
  in_deg?: number; out_deg?: number; in_kzt?: number; out_kzt?: number;
  evidence?: string; x: number; y: number;
}
export interface ContractEdge { src: string; dst: string; sum_kzt: number; n_tx: number }
const money = (n?: number) => n === undefined ? '—' : new Intl.NumberFormat('ru-RU', {
  style: 'currency', currency: 'KZT', maximumFractionDigits: 2,
}).format(n);
export function toGraphNode(n: ContractNode) {
  return {
    id: n.gid, gid: n.gid, role: n.role,
    roleScore: n.role_score * 100, priorityScore: n.priority_score * 100,
    clusterId: n.cluster_id, incoming: n.in_deg ?? 0, outgoing: n.out_deg ?? 0,
    received: money(n.in_kzt), sent: money(n.out_kzt),
    evidence: n.evidence ?? 'Откройте карточку для рассчитанного обоснования',
    x: n.x, y: n.y,
  };
}
export function toGraphEdge(e: ContractEdge) {
  return {id: `${e.src}:${e.dst}`, source: e.src, target: e.dst,
    amount: money(e.sum_kzt), label: `${e.n_tx} переводов`};
}
