import { test } from 'node:test'
import assert from 'node:assert/strict'
import { selectGraphView } from '../src/graphView.ts'

const nodes = Array.from({ length: 2248 }, (_, i) => ({ id: String(10000 + i), priorityScore: 1 - i / 2248 }))
const selected = nodes.at(-1).id
const edges = nodes.slice(0, 200).map(n => ({ source: selected, target: n.id }))

test('bounded view retains a searched low-priority node and never creates dangling edges', () => {
  const result = selectGraphView(nodes, edges, selected, 'top')
  assert.equal(result.nodes.length, 100)
  assert.equal(result.nodes[0].id, selected)
  assert.deepEqual(result.nodes.slice(1), nodes.slice(0, 99))
  const ids = new Set(result.nodes.map(n => n.id))
  assert.ok(result.edges.every(e => ids.has(e.source) && ids.has(e.target)))
  assert.equal(result.edges.length, 99)
  assert.equal(nodes.length, 2248)
})

test('high-degree neighborhoods are bounded; isolated and filtered-out selections are valid', () => {
  assert.equal(selectGraphView(nodes, edges, selected, 'neighbors').nodes.length, 100)
  assert.deepEqual(selectGraphView(nodes, [], selected, 'neighbors'), { nodes: [nodes.at(-1)], edges: [] })
  assert.deepEqual(selectGraphView(nodes.slice(0, 3), [], selected, 'neighbors'), { nodes: [], edges: [] })
})

test('explicit full view includes all original nodes and edges', () => {
  const result = selectGraphView(nodes, edges, selected, 'all')
  assert.equal(result.nodes.length, 2248)
  assert.equal(result.edges.length, 200)
})
