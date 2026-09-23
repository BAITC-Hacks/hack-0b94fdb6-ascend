import { getSignalMeta } from '../data/mockData'

interface EntitySignalIconProps {
  priorityScore: number
  size?: number
  animate?: boolean
  label?: string
}

/**
 * A code-native SVG marker used for analytical signal levels.
 * It deliberately communicates a review priority, not a verdict about a person.
 */
export function EntitySignalIcon({ priorityScore, size = 42, animate = false, label }: EntitySignalIconProps) {
  const signal = getSignalMeta(priorityScore)
  const title = label ?? `${signal.label}, оценка ${Math.round(priorityScore * 100)}%`

  return <svg className={`entity-signal entity-signal--${signal.level} ${animate ? 'entity-signal--animated' : ''}`} width={size} height={size} viewBox="0 0 48 48" role="img" aria-label={title}>
    <title>{title}</title>
    <circle className="entity-signal__halo" cx="24" cy="24" r="20" fill="none" stroke={signal.color} />
    <circle className="entity-signal__ring" cx="24" cy="24" r="15.5" fill={signal.softColor} stroke={signal.color} />
    <path className="entity-signal__person" d="M24 12.5a5.25 5.25 0 1 0 0 10.5 5.25 5.25 0 0 0 0-10.5Zm-9.1 21.85c.93-5.2 4.1-8.05 9.1-8.05s8.17 2.85 9.1 8.05c.13.7-.45 1.35-1.17 1.35H16.07c-.72 0-1.3-.65-1.17-1.35Z" fill={signal.color} />
    <path className="entity-signal__mark" d="M34.7 12.4 37 14.7l-5.1 5.1-2.3-2.3 5.1-5.1Z" fill={signal.color} />
  </svg>
}

export function SignalBadge({ priorityScore }: { priorityScore: number }) {
  const signal = getSignalMeta(priorityScore)
  return <span className={`signal-badge signal-badge--${signal.level}`}><i style={{ backgroundColor: signal.color }} />{signal.shortLabel}</span>
}
