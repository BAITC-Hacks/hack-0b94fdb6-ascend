import { test } from 'node:test'
import assert from 'node:assert/strict'
import { checkChronology, findDirectedPath, edgeEvidence, reportMarkdown } from '../src/investigation.ts'

const nodes = Array.from({length:10},(_,i)=>({id:'10000000000000010'+i}))
const edge = (a,b) => ({id:`${a}:${b}`,source:nodes[a].id,target:nodes[b].id,amount:'12 345,67 ₸',sumKzt:12345.67,transactions:3,firstDate:'2026-07-01',lastDate:'2026-07-03'})

test('date check rejects impossible ordering but never claims proof from aggregate intervals',()=>{
  const first={...edge(0,1),firstDate:'2026-07-20',lastDate:'2026-07-28'}
  assert.equal(checkChronology([first,edge(1,2)]).status,'conflict')
  assert.equal(checkChronology([edge(1,2),first]).status,'unconfirmed')
  assert.equal(checkChronology([{...first,firstDate:null}]).status,'unknown')
  assert.equal(checkChronology([first,{...edge(1,2),firstDate:'2026-07-01',lastDate:'2026-07-30'},{...edge(2,3),lastDate:'2026-07-19'}]).status,'conflict')
})

test('shortest directed path preserves exact GIDs, handles cycles and deterministic ties',()=>{
  const edges=[edge(0,2),edge(2,3),edge(3,0),edge(0,1),edge(1,3)]
  const path=findDirectedPath(nodes,edges,nodes[0].id,nodes[3].id)
  assert.deepEqual(path,{nodeIds:[nodes[0].id,nodes[1].id,nodes[3].id],edgeIds:['0:1','1:3']})
  assert.equal(findDirectedPath(nodes,edges,nodes[9].id,nodes[0].id),null)
  assert.equal(findDirectedPath(nodes,[edge(0,1)],nodes[1].id,nodes[0].id),null)
})

test('search explicitly stops at six hops and validates both endpoints',()=>{
  const chain=nodes.slice(1).map((_,i)=>edge(i,i+1))
  assert.equal(findDirectedPath(nodes,chain,nodes[0].id,nodes[6].id).edgeIds.length,6)
  assert.equal(findDirectedPath(nodes,chain,nodes[0].id,nodes[7].id),null)
  assert.throws(()=>findDirectedPath(nodes,chain,'3',nodes[1].id),/отсутствует/)
  assert.throws(()=>findDirectedPath(nodes,chain,nodes[0].id,nodes[0].id),/разных/)
})

test('case report retains directed amounts, dates, provenance and limitations without inventing flow totals',()=>{
  const item=edgeEvidence(edge(0,1))
  const report=reportMarkdown('run-42','2026-07-01 — 2026-07-31',[item])
  assert.ok(report.includes(nodes[0].id+' → '+nodes[1].id))
  assert.ok(report.includes('12 345,67 ₸'))
  assert.ok(report.includes('Число переводов: 3'))
  assert.ok(report.includes('последний: 2026-07-03'))
  assert.ok(report.includes('Снимок: run-42'))
  assert.ok(report.includes('не доказывает движение одних и тех же денег'))
})
