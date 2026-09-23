import { ArrowDownLeft, ArrowUpRight, CircleHelp, Network, ShieldAlert } from 'lucide-react'
import type { ReactNode } from 'react'
import type { GraphNode } from '../types/graph'
import { roleMeta } from '../data/mockData'

export function NodeDetails({ node }: { node: GraphNode }) {
  const role = roleMeta[node.role]
  return <aside className="details-panel"><div className="details-header"><div><p className="eyebrow">SELECTED ENTITY</p><h2>Node Details</h2></div><span className="status-pill"><span /> Monitored</span></div><div className="entity-card"><div className="entity-top"><div className="entity-icon" style={{ color: role.color, background: `${role.color}18` }}><Network size={21} /></div><div><span className="entity-gid">GID {node.gid}</span><span className="entity-role" style={{ color: role.color }}>{role.label}</span></div><div className="cluster-pill">Cluster #{node.clusterId}</div></div><div className="score-row"><div><span>Role confidence</span><strong>{node.roleScore}%</strong></div><div><span>Priority score</span><strong>{node.priorityScore}%</strong></div></div></div><div className="metrics-grid"><Metric icon={<ArrowDownLeft size={15} />} label="Incoming" value={node.incoming.toString()} /><Metric icon={<ArrowUpRight size={15} />} label="Outgoing" value={node.outgoing.toString()} /><Metric label="Received" value={node.received} /><Metric label="Sent" value={node.sent} /></div><section className="evidence-card"><div className="evidence-heading"><div className="evidence-icon"><ShieldAlert size={16} /></div><div><p className="eyebrow">EXPLAINABILITY</p><h3>Why this role?</h3></div><CircleHelp size={15} className="muted-icon" /></div><p>{node.evidence}</p><div className="evidence-tags"><span>{node.incoming} inbound paths</span><span>{node.outgoing} outbound paths</span></div></section><div className="details-note">Scores are analytical hypotheses based on observed network structure. Review supporting transactions before action.</div></aside>
}

function Metric({ icon, label, value }: { icon?: ReactNode; label: string; value: string }) { return <div className="metric"><div className="metric-label">{icon}{label}</div><strong>{value}</strong></div> }
