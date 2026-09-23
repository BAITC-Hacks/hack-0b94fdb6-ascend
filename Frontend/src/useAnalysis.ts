import { useCallback, useEffect, useState } from 'react'
import { adaptNode, api, money, type Cluster, type GraphResponse, type NodeCard, type Overview } from './api'
import type { GraphNode, GraphEdge } from './types/graph'

export function useAnalysis() {
  const [nodes, setNodes] = useState<GraphNode[]>([])
  const [edges, setEdges] = useState<GraphEdge[]>([])
  const [overview, setOverview] = useState<Overview | null>(null)
  const [clusters, setClusters] = useState<Cluster[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [generation, setGeneration] = useState(0)
  const retry = useCallback(() => setGeneration(n => n + 1), [])
  useEffect(() => {
    const controller = new AbortController()
    const load = async () => {
      setLoading(true); setError('')
      try {
        const init = { signal: controller.signal }
        const info = await api<Overview>('/overview', init)
        if (!info.run_id) throw new Error('Нет результата анализа. Запустите pipeline и перечитайте снимок.')
        const graph = await api<GraphResponse>('/graph', init)
        const allClusters: Cluster[] = []
        let total = 1
        while (allClusters.length < total) {
          const page = await api<{ items: Cluster[]; total: number }>(`/clusters?limit=200&offset=${allClusters.length}`, init)
          total = page.total
          if (!page.items.length) break
          allClusters.push(...page.items)
        }
        const after = await api<Overview>('/overview', init)
        if (info.run_id !== graph.run_id || after.run_id !== graph.run_id) throw new Error('Результат изменился во время загрузки. Обновите данные.')
        if (controller.signal.aborted) return
        setNodes(graph.nodes.sort((a, b) => a.priority_rank - b.priority_rank).map(n => adaptNode(n)))
        setEdges(graph.edges.map(e => ({ id: `${e.src}:${e.dst}`, source: e.src, target: e.dst, amount: money(e.sum_kzt), sumKzt: e.sum_kzt, transactions: e.n_tx, firstDate: e.first_date, lastDate: e.last_date })))
        setOverview(after); setClusters(allClusters)
      } catch (e) { if (!controller.signal.aborted) setError(e instanceof Error ? e.message : 'API недоступен') }
      finally { if (!controller.signal.aborted) setLoading(false) }
    }
    void load()
    return () => controller.abort()
  }, [generation])
  return { nodes, edges, overview, clusters, loading, error, retry }
}

export function useNode(gid: string, runId: string | null | undefined) {
  const [state, setState] = useState<{ gid: string; runId: string | null | undefined; card: NodeCard | null; error: string }>({ gid: '', runId: null, card: null, error: '' })
  useEffect(() => {
    if (!gid || !runId) return
    const controller = new AbortController()
    setState({ gid, runId, card: null, error: '' })
    api<NodeCard>('/nodes/' + encodeURIComponent(gid), { signal: controller.signal })
      .then(async card => {
        const current = await api<Overview>('/overview', { signal: controller.signal })
        if (current.run_id !== runId) throw new Error('Снимок сменился. Обновите данные сайта.')
        if (!controller.signal.aborted) setState({ gid, runId, card, error: '' })
      })
      .catch(e => { if (!controller.signal.aborted) setState({ gid, runId, card: null, error: e.message }) })
    return () => controller.abort()
  }, [gid, runId])
  return state.gid === gid && state.runId === runId ? state : { gid, card: null, error: '' }
}
