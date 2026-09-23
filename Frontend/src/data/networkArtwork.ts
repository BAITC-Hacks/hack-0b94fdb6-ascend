import type { GraphNode } from '../types/graph'
import { priorityArtwork } from './visualAssets'
import { riskIndex } from '../i18n'
import { getClusterColor } from './mockData'
import { signalPalette } from './palette'
import risk from '../assets/role-cluster/roles/risk.png'
import caution from '../assets/role-cluster/roles/sanction.png'
import entity from '../assets/role-cluster/roles/company.png'
import transaction from '../assets/role-cluster/roles/transaction.png'
import verification from '../assets/role-cluster/roles/verification.png'
import redGroup from '../assets/role-cluster/clusters/red.png'
import orangeGroup from '../assets/role-cluster/clusters/orange.png'
import yellowGroup from '../assets/role-cluster/clusters/yellow.png'
import greenGroup from '../assets/role-cluster/clusters/green.png'
import cyanGroup from '../assets/role-cluster/clusters/cyan.png'

export type NetworkColorMode = 'priority' | 'role' | 'cluster'

// Graphic motifs, not new classifications: no sanction, company, KYC or guilt claims.
export const roleArtwork: Record<GraphNode['role'], string> = {
  consolidator: yellowGroup,
  transit: transaction,
  distributor: orangeGroup,
  terminal: verification,
  coordinator: redGroup,
  peripheral: entity,
}
export const interfaceArtwork = { priority: risk, caution, transaction, evidence: verification }

const clusterArtwork: Record<string, string> = {
  [signalPalette.red]: redGroup,
  [signalPalette.orange]: orangeGroup,
  [signalPalette.yellow]: yellowGroup,
  [signalPalette.green]: greenGroup,
  [signalPalette.blue]: cyanGroup,
}
export const getClusterArtwork = (clusterId: number) => clusterArtwork[getClusterColor(clusterId)] ?? cyanGroup

export function getNodeArtwork(node: GraphNode, mode: NetworkColorMode) {
  if (mode === 'role') return roleArtwork[node.role]
  if (mode === 'cluster') return getClusterArtwork(node.clusterId)
  return priorityArtwork[riskIndex(node.priorityScore)]
}
