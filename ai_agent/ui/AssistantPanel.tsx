/** Copy into Frontend/src/components, or import from the package in your build. */
import { useEffect, useRef } from 'react'

type AssistantElement = HTMLElement & { setQuestion?: (question: string) => void }
type Props = { selectedGid?: string; onSelectGid?: (gid: string) => void; apiBase?: string }

export function AssistantPanel({ selectedGid, onSelectGid, apiBase = '/api/v1' }: Props) {
  const host = useRef<HTMLDivElement>(null)
  const element = useRef<AssistantElement | null>(null)
  const onSelect = useRef(onSelectGid)
  onSelect.current = onSelectGid
  useEffect(() => {
    const tag = document.createElement('moneygraph-assistant') as AssistantElement
    tag.setAttribute('api-base', apiBase)
    const handler = (event: Event) => {
      const e = event as CustomEvent<{ gid: string }>
      if (onSelect.current) { e.preventDefault(); onSelect.current(e.detail.gid) }
    }
    tag.addEventListener('graph-node-select', handler)
    element.current = tag
    host.current?.append(tag)
    // The backend serves this script. Configure the Vite proxy in development.
    if (!document.querySelector('script[data-moneygraph-agent]')) {
      const script = document.createElement('script')
      script.src = '/ai-agent/assistant.js'
      script.dataset.moneygraphAgent = 'true'
      script.onerror = () => { tag.textContent = 'Не удалось загрузить ассистента. Проверьте маршрут /ai-agent/assistant.js.' }
      document.head.append(script)
    }
    return () => { tag.removeEventListener('graph-node-select', handler); tag.remove(); element.current = null }
  }, [apiBase])
  useEffect(() => {
    let cancelled = false
    if (selectedGid) customElements.whenDefined('moneygraph-assistant').then(() => {
      if (!cancelled) element.current?.setQuestion?.(`Объясни роль и ограничения данных для #${selectedGid}`)
    })
    return () => { cancelled = true }
  }, [selectedGid, apiBase])
  return <div ref={host} />
}
