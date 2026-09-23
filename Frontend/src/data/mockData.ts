import { signalPalette } from './palette'
import type { GraphEdge, GraphNode, SignalMeta } from '../types/graph'

export const mockNodes: GraphNode[] = [
  { id: 'n192831', gid: '192831', role: 'consolidator', roleScore: .91, priorityScore: .94, clusterId: 3, incoming: 14, outgoing: 2, received: '₸8.3M', sent: '₸7.9M', evidence: 'Получает средства от 14 уникальных клиентов и направляет основной объём только двум получателям.', x: 50, y: 49 },
  { id: 'n203472', gid: '203472', role: 'transit', roleScore: .87, priorityScore: .91, clusterId: 3, incoming: 8, outgoing: 8, received: '₸5.1M', sent: '₸5.0M', evidence: 'Наблюдается сквозной поток: объём входящих и исходящих операций сопоставим.', x: 63, y: 33 },
  { id: 'n104882', gid: '104882', role: 'distributor', roleScore: .83, priorityScore: .86, clusterId: 3, incoming: 3, outgoing: 11, received: '₸4.7M', sent: '₸4.6M', evidence: 'Распределяет входящий поток между 11 получателями по устойчивому веерному паттерну.', x: 75, y: 58 },
  { id: 'n882104', gid: '882104', role: 'coordinator', roleScore: .78, priorityScore: .79, clusterId: 2, incoming: 9, outgoing: 7, received: '₸3.2M', sent: '₸3.1M', evidence: 'Связывает два плотных кластера и повторно соединяет одни и те же пути переводов.', x: 32, y: 28 },
  { id: 'n441095', gid: '441095', role: 'terminal', roleScore: .74, priorityScore: .71, clusterId: 3, incoming: 5, outgoing: 0, received: '₸2.6M', sent: '₸0', evidence: 'В наблюдаемом фрагменте есть входящие потоки без исходящих; вывод ограничен границей выборки.', x: 88, y: 35 },
  { id: 'n703118', gid: '703118', role: 'peripheral', roleScore: .61, priorityScore: .54, clusterId: 1, incoming: 1, outgoing: 2, received: '₸740K', sent: '₸612K', evidence: 'Узел на периферии кластера: недостаточно связей для специализированной роли.', x: 17, y: 68 },
  { id: 'n319420', gid: '319420', role: 'transit', roleScore: .69, priorityScore: .63, clusterId: 3, incoming: 4, outgoing: 5, received: '₸1.9M', sent: '₸1.8M', evidence: 'Передаёт наблюдаемый объём дальше по повторяющемуся пути внутри кластера.', x: 42, y: 70 },
  { id: 'n551920', gid: '551920', role: 'peripheral', roleScore: .56, priorityScore: .49, clusterId: 1, incoming: 2, outgoing: 1, received: '₸510K', sent: '₸405K', evidence: 'Небольшой объём и малое число связей; необходима дополнительная проверка контекста.', x: 25, y: 50 },
  { id: 'n902441', gid: '902441', role: 'distributor', roleScore: .72, priorityScore: .68, clusterId: 3, incoming: 2, outgoing: 7, received: '₸2.1M', sent: '₸2.0M', evidence: 'Направляет средства нескольким конечным узлам в повторяемом распределительном паттерне.', x: 65, y: 73 },
  { id: 'n120934', gid: '120934', role: 'terminal', roleScore: .66, priorityScore: .59, clusterId: 2, incoming: 3, outgoing: 0, received: '₸1.2M', sent: '₸0', evidence: 'Видимый входящий поток не имеет исходящих операций в наблюдаемом фрагменте сети.', x: 78, y: 19 },
]

export const mockEdges: GraphEdge[] = [
  { id: 'e1', source: 'n551920', target: 'n192831', amount: '₸510K' }, { id: 'e2', source: 'n703118', target: 'n192831', amount: '₸740K' }, { id: 'e3', source: 'n882104', target: 'n192831', amount: '₸1.8M' }, { id: 'e4', source: 'n192831', target: 'n203472', amount: '₸3.2M' }, { id: 'e5', source: 'n192831', target: 'n104882', amount: '₸4.7M' }, { id: 'e6', source: 'n203472', target: 'n441095', amount: '₸1.5M' }, { id: 'e7', source: 'n203472', target: 'n104882', amount: '₸1.8M' }, { id: 'e8', source: 'n319420', target: 'n192831', amount: '₸1.9M' }, { id: 'e9', source: 'n104882', target: 'n441095', amount: '₸900K' }, { id: 'e10', source: 'n104882', target: 'n902441', amount: '₸1.1M' }, { id: 'e11', source: 'n902441', target: 'n120934', amount: '₸620K' }, { id: 'e12', source: 'n902441', target: 'n441095', amount: '₸810K' }, { id: 'e13', source: 'n882104', target: 'n319420', amount: '₸640K' }, { id: 'e14', source: 'n319420', target: 'n902441', amount: '₸450K' },
]

export const roleMeta = {
  consolidator: { label: 'Консолидатор', color: signalPalette.yellow }, transit: { label: 'Транзит', color: signalPalette.blue }, distributor: { label: 'Распределитель', color: signalPalette.orange }, terminal: { label: 'Конечный получатель', color: signalPalette.green }, coordinator: { label: 'Координатор', color: signalPalette.red }, peripheral: { label: 'Периферийный', color: signalPalette.green },
} as const

export const clusterMeta: Record<number, { color: string; nNodes: number; nSeed: number; internalTurnover: string; keyGids: string[]; hypothesis: string }> = {
  1: { color: signalPalette.green, nNodes: 624, nSeed: 22, internalTurnover: '₸98.2M', keyGids: ['703118', '551920'], hypothesis: 'Периферийный фрагмент с ограниченным числом наблюдаемых связей.' },
  2: { color: signalPalette.yellow, nNodes: 713, nSeed: 28, internalTurnover: '₸121.4M', keyGids: ['882104', '120934'], hypothesis: 'Фрагмент со связующими узлами между несколькими путями переводов.' },
  3: { color: signalPalette.blue, nNodes: 911, nSeed: 31, internalTurnover: '₸146.3M', keyGids: ['192831', '203472', '104882'], hypothesis: 'Плотный фрагмент с признаками консолидации и распределения наблюдаемого потока.' },
}

export function getClusterColor(clusterId: number) {
  return clusterMeta[clusterId]?.color ?? signalPalette.blue
}

export function getSignalMeta(priorityScore: number): SignalMeta {
  if (priorityScore >= .85) return { level: 'high', label: 'Высокий сигнал', shortLabel: 'Высокий', color: '#ef7a68', softColor: 'rgba(239, 122, 104, .16)' }
  if (priorityScore >= .70) return { level: 'elevated', label: 'Повышенный сигнал', shortLabel: 'Повышен', color: '#e9b35f', softColor: 'rgba(233, 179, 95, .15)' }
  if (priorityScore >= .55) return { level: 'review', label: 'Сигнал для проверки', shortLabel: 'Проверка', color: '#59beb5', softColor: 'rgba(89, 190, 181, .14)' }
  return { level: 'background', label: 'Фоновый сигнал', shortLabel: 'Фоновый', color: '#778394', softColor: 'rgba(119, 131, 148, .13)' }
}

export function formatScore(score: number) { return `${Math.round(score * 100)}%` }
