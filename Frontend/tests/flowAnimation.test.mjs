import { test } from 'node:test'
import assert from 'node:assert/strict'
import { attachFlowAnimation } from '../src/components/flowAnimation.ts'

function setup({ reduced = false, hidden = false } = {}) {
  let sequence = 0, cleaned = false, observed = false
  const frames = new Map(), mediaEvents = new Map(), documentEvents = new Map()
  const media = { matches: reduced, addEventListener: (type, fn) => mediaEvents.set(type, fn), removeEventListener: type => mediaEvents.delete(type) }
  globalThis.window = { devicePixelRatio: 3, matchMedia: () => media }
  globalThis.document = { hidden, addEventListener: (type, fn) => documentEvents.set(type, fn), removeEventListener: type => documentEvents.delete(type) }
  globalThis.requestAnimationFrame = callback => { frames.set(++sequence, callback); return sequence }
  globalThis.cancelAnimationFrame = id => frames.delete(id)
  globalThis.ResizeObserver = class { observe() { observed = true } disconnect() { observed = false } }
  const arcs = []
  const ctx = { setTransform() {}, clearRect() { arcs.length = 0 }, beginPath() {}, moveTo() {}, lineTo() {}, stroke() {}, fill() {}, arc(...args) { arcs.push(args) } }
  const canvas = { getContext: () => ctx }
  const edge = { renderedSourceEndpoint: () => ({ x: 10, y: 10 }), renderedTargetEndpoint: () => ({ x: 90, y: 10 }), renderedControlPoints: () => [{ x: 50, y: 80 }], data: () => '#ff6b74', hasClass: () => true }
  const cy = { edges: () => [edge], on() {}, off() { cleaned = true } }
  const tick = now => { const [id, callback] = [...frames][0]; frames.delete(id); callback(now) }
  return { cy, canvas, frames, media, arcs, mediaEvents, documentEvents, tick, state: () => ({ cleaned, observed }) }
}

test('motion follows directed curves, caps pixel density and releases every listener', () => {
  const env = setup()
  const cleanup = attachFlowAnimation(env.cy, env.canvas, { clientWidth: 200, clientHeight: 100 }, true)
  assert.equal(env.canvas.width, 400)
  assert.equal(env.frames.size, 1)
  env.tick(100)
  const firstX = env.arcs[0][0]
  env.tick(180)
  assert.ok(env.arcs[0][0] > firstX, 'particle moves from source toward receiver')
  cleanup()
  assert.equal(env.frames.size, 0)
  assert.equal(env.mediaEvents.size, 0)
  assert.equal(env.documentEvents.size, 0)
  assert.deepEqual(env.state(), { cleaned: true, observed: false })
})

test('pause, reduced motion and hidden tabs do not schedule animation', () => {
  for (const options of [{ enabled: false }, { enabled: true, reduced: true }, { enabled: true, hidden: true }]) {
    const env = setup(options)
    const cleanup = attachFlowAnimation(env.cy, env.canvas, { clientWidth: 200, clientHeight: 100 }, options.enabled)
    assert.equal(env.frames.size, 0)
    cleanup()
  }
})

test('changing accessibility preference and tab visibility stops and resumes safely', () => {
  const env = setup()
  const cleanup = attachFlowAnimation(env.cy, env.canvas, { clientWidth: 200, clientHeight: 100 }, true)
  env.media.matches = true
  env.mediaEvents.get('change')()
  assert.equal(env.frames.size, 0)
  env.media.matches = false
  env.mediaEvents.get('change')()
  assert.equal(env.frames.size, 1)
  document.hidden = true
  env.documentEvents.get('visibilitychange')()
  assert.equal(env.frames.size, 0)
  document.hidden = false
  env.documentEvents.get('visibilitychange')()
  assert.equal(env.frames.size, 1)
  cleanup()
})
