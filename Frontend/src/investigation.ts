import type { GraphEdge, GraphNode } from './types/graph'

export type Trace = { nodeIds: string[]; edgeIds: string[] }
export type Evidence = { key: string; title: string; facts: string[] }
export const TRACE_LIMIT = 6

/** Shortest directed path by edge count; amounts are not distance or traced funds. */
export function findDirectedPath(nodes: GraphNode[], edges: GraphEdge[], from: string, to: string): Trace | null {
  const ids = new Set(nodes.map(n => n.id))
  if (!ids.has(from) || !ids.has(to)) throw new Error('Один из GID отсутствует в снимке.')
  if (from === to) throw new Error('Выберите два разных GID.')
  const outgoing = new Map<string, GraphEdge[]>()
  for (const edge of edges) {
    if (!ids.has(edge.source) || !ids.has(edge.target)) continue
    const group = outgoing.get(edge.source) || []
    group.push(edge); outgoing.set(edge.source, group)
  }
  for (const group of outgoing.values()) group.sort((a,b) => a.target.localeCompare(b.target) || a.id.localeCompare(b.id))
  const queue = [{ id: from, depth: 0 }]
  const previous = new Map<string, GraphEdge>()
  const seen = new Set([from])
  for (let i = 0; i < queue.length; i++) {
    const current = queue[i]
    if (current.depth === TRACE_LIMIT) continue
    for (const edge of outgoing.get(current.id) || []) {
      if (seen.has(edge.target)) continue
      seen.add(edge.target); previous.set(edge.target, edge)
      if (edge.target === to) {
        const nodeIds = [to], edgeIds: string[] = []
        let cursor = to
        while (cursor !== from) {
          const step = previous.get(cursor)!
          edgeIds.unshift(step.id); nodeIds.unshift(step.source); cursor = step.source
        }
        return { nodeIds, edgeIds }
      }
      queue.push({ id: edge.target, depth: current.depth + 1 })
    }
  }
  return null
}

export function edgeEvidence(edge: GraphEdge): Evidence {
  return { key: 'edge:' + edge.id, title: `Связь ${edge.source} → ${edge.target}`, facts: [
    `Наблюдаемая сумма: ${edge.amount}`,
    `Число переводов: ${edge.transactions ?? 'не указано'}`,
    `Первый перевод: ${edge.firstDate || 'нет данных'}; последний: ${edge.lastDate || 'нет данных'}`,
  ] }
}

/** Date ranges can disprove an ordering, but cannot prove a transaction-level flow. */
export function checkChronology(edges: GraphEdge[]) {
  if (!edges.length || edges.some(e => !e.firstDate || !e.lastDate)) return {
    status:'unknown', message:'Для проверки хронологии не хватает дат. Показана только структура связей.',
  }
  let earliest = ''
  for (let i=0; i<edges.length; i++) {
    const edge = edges[i]
    if (edge.lastDate! < earliest) return { status:'conflict',
      message:`Хронология не сходится: на шаге ${i+1} последний перевод был ${edge.lastDate}, а предыдущие шаги требуют даты не раньше ${earliest}. Эта цепочка не описывает последовательное движение средств в наблюдаемом периоде.` }
    if (edge.firstDate! > earliest) earliest = edge.firstDate!
  }
  return { status:'unconfirmed', message:'Диапазоны дат не исключают последовательность. Агрегаты не подтверждают, что по цепочке прошли одни и те же деньги; нужна проверка отдельных операций.' }
}

export function reportMarkdown(runId: string, period: string, items: Evidence[]): string {
  return [ '# Freedom Graph · Досье исследования', '', `Снимок: ${runId}`, `Период: ${period}`, '',
    'Материал для ручной проверки. Роли и приоритеты — гипотезы, а не выводы о виновности.', '',
    ...items.flatMap((item, i) => [`## ${i + 1}. ${item.title}`, '', ...item.facts.map(f => `- ${f}`), '']),
    '## Ограничения наблюдения', '',
    '- Связи — агрегированные направленные переводы в наблюдаемом срезе.',
    '- Путь показывает структурную достижимость; не доказывает движение одних и тех же денег или последовательность операций во времени.',
    '- На границе обхода исходящие связи не прослежены; отсутствие пути не доказывает отсутствие финансовой связи.',
    '- Межбанковские операции и переводы ниже порога исходного набора не представлены.',
    '- Числовые факты взяты из указанного снимка. Этот отчёт собран из выбранных аналитиком фактов, без генерации LLM.', '',
  ].join('\n')
}
