import type { Language } from "../i18n"
import { translate } from "../interfaceCopy"
import { useEffect, useRef, useState } from 'react'
import { api } from '../api'

type Message = { role: 'user' | 'assistant'; content: string }
type Reply = { answer: string; gids: string[]; tool_calls: { name: string; args: unknown }[]; run_id: string; answer_source?: string; mode?: string; warnings?: string[] }
export function AssistantChat({ language, runId, selectedGid, onSelect, suggestedPrompt }: { language: Language; suggestedPrompt?: {text:string}|null; runId: string; selectedGid: string; onSelect: (gid: string) => void }) {
  const tr = (text: string, values: Record<string,string|number> = {}) => translate(language,text,values)
  const [open, setOpen] = useState(false)
  const [question, setQuestion] = useState('')
  const [history, setHistory] = useState<Message[]>([])
  const [reply, setReply] = useState<Reply | null>(null)
  const [error, setError] = useState('')
  const [busy, setBusy] = useState(false)
  const [status, setStatus] = useState('')
  const active = useRef<AbortController | null>(null)
  useEffect(()=>{if(suggestedPrompt){setQuestion(suggestedPrompt.text);setOpen(true)}},[suggestedPrompt])
  useEffect(() => { active.current?.abort(); active.current=null; setHistory([]); setReply(null); setError(''); setBusy(false); return () => { active.current?.abort(); active.current=null } }, [runId])
  useEffect(() => { if (open) api<{ assistant_message: string }>('/health').then(h => setStatus(h.assistant_message)).catch(() => setStatus("API недоступен")) }, [open])
  async function send() {
    const text = question.trim()
    if (!text || busy) return
    const controller = new AbortController(); active.current = controller
    setBusy(true); setError(''); setReply(null)
    const timer = setTimeout(() => controller.abort(), 70000)
    try {
      const result = await api<Reply>('/assistant', { method: 'POST', headers: { 'Content-Type': 'application/json' }, signal: controller.signal,
        body: JSON.stringify({ question: text, history: history.slice(-6) }) })
      if (active.current !== controller) return
      if (result.run_id !== runId) throw new Error(tr("Результат анализа сменился. Обновите данные сайта и повторите вопрос."))
      setReply(result)
      setHistory([...history, { role: 'user', content: text }, { role: 'assistant', content: result.answer.slice(0, 4000) }].slice(-6) as Message[])
    } catch (e) { if (active.current === controller) setError(controller.signal.aborted ? tr("Время ожидания истекло.") : e instanceof Error ? e.message : tr("Сервис недоступен")) }
    finally { clearTimeout(timer); if (active.current === controller) { setBusy(false); active.current = null } }
  }
  return <div className="assistant-dock">
    <button className="assistant-toggle" onClick={() => setOpen(!open)} aria-expanded={open}>{open ? tr("Закрыть AI") : tr("Спросить AI")}</button>
    {open && <section className="assistant-panel" aria-label={tr("AI-ассистент")}>
      <h2>{tr("AI-ассистент аналитика")}</h2><p>{tr(status)}</p>
      <p className="assistant-disclosure">{tr("Вопрос и выбранные агентом факты передаются в OpenAI. Ответы — гипотезы для проверки.")}</p>
      <div className="assistant-actions"><button disabled={busy} onClick={() => setQuestion(tr("Выбери 10 приоритетных узлов"))}>{tr("Топ-10")}</button><button disabled={busy || !selectedGid} onClick={() => setQuestion(tr("Объясни роль узла #{gid}",{gid:selectedGid}))}>{tr("Объяснить узел")}</button><button disabled={busy} onClick={() => { setHistory([]); setReply(null); setError('') }}>{tr("Новый разговор")}</button></div>
      <form onSubmit={e => { e.preventDefault(); void send() }}><textarea aria-label={tr("Вопрос агенту")} required maxLength={4000} value={question} onChange={e => setQuestion(e.target.value)} placeholder={tr("Какие узлы проверить первыми?")}/><button disabled={busy || !question.trim()}>{busy ? tr("Агент изучает данные…") : tr("Отправить вопрос")}</button></form>
      {error && <p className="integration-error" role="alert">{tr(error)}</p>}
      {reply && <><p className="assistant-disclosure">{reply.mode==='fallback'?tr("Локальный анализ · без LLM"):reply.mode==='ai'?tr("AI · факты из инструментов"):tr("Ответ по снимку графа")}</p><p className="assistant-answer">{reply.answer}</p>{reply.warnings?.map((warning,i)=><p className="assistant-disclosure" key={i}>{warning}</p>)}<div className="assistant-actions">{reply.gids.map(gid => <button key={gid} onClick={() => onSelect(gid)}>#{gid}</button>)}</div><details><summary>{tr("Инструменты агента")}</summary><pre>{JSON.stringify(reply.tool_calls, null, 2)}</pre></details></>}
    </section>}
  </div>
}
