import type { Core } from 'cytoscape'

type Point = { x: number; y: number }
type Route = { start: Point; end: Point; control: Point; color: string; focused: boolean }
const pointAt = (route: Route, t: number): Point => ({
  x: (1 - t) ** 2 * route.start.x + 2 * (1 - t) * t * route.control.x + t ** 2 * route.end.x,
  y: (1 - t) ** 2 * route.start.y + 2 * (1 - t) * t * route.control.y + t ** 2 * route.end.y,
})

/** Decorative replay of existing directed edges, not a live transaction stream. */
export function attachFlowAnimation(cy: Core, canvas: HTMLCanvasElement, container: HTMLElement, enabled: boolean) {
  const ctx = canvas.getContext('2d')
  if (!ctx) return () => {}
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)')
  let frame = 0, previous = 0, time = 0, width = 0, height = 0
  let dirty = true
  let routes: Route[] = []
  const refresh = () => { dirty = true }
  const resize = () => {
    width = container.clientWidth; height = container.clientHeight
    const ratio = Math.min(window.devicePixelRatio || 1, 2)
    canvas.width = Math.round(width * ratio); canvas.height = Math.round(height * ratio)
    ctx.setTransform(ratio, 0, 0, ratio, 0, 0)
    dirty = true
  }
  const updateRoutes = () => {
    routes = []
    // Bounded visual workload even if a larger snapshot is supplied later.
    cy.edges().slice(0, 80).forEach(edge => {
      const start = edge.renderedSourceEndpoint(), end = edge.renderedTargetEndpoint()
      const control = edge.renderedControlPoints()?.[0]
      if (start && end && control && [start.x, start.y, end.x, end.y, control.x, control.y].every(Number.isFinite)) {
        routes.push({ start, end, control, color: edge.data('color'), focused: edge.hasClass('focused') })
      }
    })
    dirty = false
  }
  const draw = (now: number) => {
    frame = requestAnimationFrame(draw)
    if (now - previous < 1000 / 30) return
    time += previous ? Math.min(now - previous, 80) : 0
    previous = now
    ctx.clearRect(0, 0, width, height)
    if (dirty) updateRoutes()
    routes.forEach((route, index) => {
      const phase = (time / (4200 + (index % 4) * 600) + index * .193) % 1
      const position = pointAt(route, phase)
      ctx.strokeStyle = route.color; ctx.fillStyle = route.color
      ctx.lineCap = 'round'
      for (let tail = 7; tail >= 0; tail--) {
        const t = phase - tail * .012
        if (t <= 0) continue
        const a = pointAt(route, Math.max(0, t - .012)), b = pointAt(route, t)
        ctx.globalAlpha = (1 - tail / 8) * (route.focused ? .7 : .3)
        ctx.lineWidth = route.focused ? 2.6 : 1.6
        ctx.beginPath(); ctx.moveTo(a.x, a.y); ctx.lineTo(b.x, b.y); ctx.stroke()
      }
      ctx.globalAlpha = route.focused ? .95 : .55
      ctx.beginPath(); ctx.arc(position.x, position.y, route.focused ? 2.6 : 1.8, 0, Math.PI * 2); ctx.fill()
      if (phase > .8) {
        const arrival = (phase - .8) * 5
        ctx.globalAlpha = (1 - arrival) * .45
        ctx.lineWidth = 1
        ctx.beginPath(); ctx.arc(route.end.x, route.end.y, 3 + arrival * 16, 0, Math.PI * 2); ctx.stroke()
      }
    })
    ctx.globalAlpha = 1
  }
  const updatePlayback = () => {
    cancelAnimationFrame(frame); previous = 0
    ctx.clearRect(0, 0, width, height)
    if (enabled && !reduced.matches && !document.hidden) frame = requestAnimationFrame(draw)
  }
  const observer = new ResizeObserver(resize)
  observer.observe(container); resize()
  cy.on('render pan zoom position add remove select unselect style', refresh)
  reduced.addEventListener('change', updatePlayback)
  document.addEventListener('visibilitychange', updatePlayback)
  updatePlayback()
  return () => {
    cancelAnimationFrame(frame); observer.disconnect()
    cy.off('render pan zoom position add remove select unselect style', refresh)
    reduced.removeEventListener('change', updatePlayback)
    document.removeEventListener('visibilitychange', updatePlayback)
    ctx.clearRect(0, 0, width, height)
  }
}
