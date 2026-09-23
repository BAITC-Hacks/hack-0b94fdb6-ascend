import { useId, type CSSProperties } from 'react'
import { TriangleAlert, Flame, ChartNoAxesColumnIncreasing, ShieldCheck, Sparkle } from 'lucide-react'
import { riskColors, riskIndex } from '../i18n'

export const tierIcons = [TriangleAlert, Flame, ChartNoAxesColumnIncreasing, ShieldCheck, Sparkle]

/** One vector vocabulary for client portraits, priority cards and graph markers. */
export function RiskAvatar({ score, large = false }: { score: number; large?: boolean }) {
  const id = useId().replace(/:/g, '')
  const tier = riskIndex(score)
  const Badge = tierIcons[tier]
  return <span className={`risk-avatar ${large ? 'risk-avatar--large' : ''}`} style={{ '--risk': riskColors[tier] } as CSSProperties} aria-hidden="true">
    <svg viewBox="0 0 80 80" className="avatar-portrait">
      <defs>
        <radialGradient id={`${id}-halo`} cx="35%" cy="22%" r="85%"><stop stopColor="currentColor" stopOpacity=".23"/><stop offset="1" stopColor="#07100e"/></radialGradient>
        <radialGradient id={`${id}-metal`} cx="24%" cy="12%" r="85%"><stop stopColor="#d7e7e1"/><stop offset=".2" stopColor="#66827a"/><stop offset=".47" stopColor="#243c35"/><stop offset=".8" stopColor="#0d1715"/><stop offset="1" stopColor="#030a08"/></radialGradient>
        <linearGradient id={`${id}-rim`} x2="1" y2="1"><stop stopColor="#edfff7" stopOpacity=".9"/><stop offset=".38" stopColor="currentColor" stopOpacity=".55"/><stop offset="1" stopColor="currentColor" stopOpacity=".06"/></linearGradient>
      </defs>
      <circle cx="40" cy="40" r="38" fill={`url(#${id}-halo)`} stroke="currentColor" strokeOpacity=".22"/>
      <circle cx="40" cy="40" r="33.5" fill="none" stroke="currentColor" strokeOpacity=".15" strokeWidth="4"/>
      <circle cx="40" cy="40" r="34" className="avatar-arc"/>
      <circle cx="40" cy="40" r="29.5" fill="none" stroke="currentColor" strokeOpacity=".3" strokeWidth=".5" strokeDasharray="1 3"/>
      <path d="M17 62C18 51 25 48 31 46H49C55 48 62 51 63 62Q40 76 17 62Z" fill={`url(#${id}-metal)`} stroke={`url(#${id}-rim)`} strokeWidth=".8"/>
      <ellipse cx="40" cy="32" rx="12.5" ry="16" fill={`url(#${id}-metal)`} stroke={`url(#${id}-rim)`} strokeWidth=".9"/>
    </svg>
    <span className="avatar-badge"><Badge size={large ? 17 : 10} strokeWidth={2}/></span>
  </span>
}

const glyphs = [
  '<path d="M12 3 22 21H2Z"/><path d="M12 9v5m0 3v1"/>',
  '<path d="M13 2c2 7-6 7-4 12 1-2 3-3 4-4 7 5 5 12-1 12C2 22 2 12 7 8c0 4 2 4 2 4-1-5 4-6 4-10Z"/>',
  '<path d="M5 20v-6m7 6V9m7 11V3" stroke-width="4"/>',
  '<path d="M12 2 21 6v6c0 5-9 10-9 10S3 17 3 12V6Z"/><path d="m8 12 3 3 5-6"/>',
  '<path d="M12 2c1 7 3 9 10 10-7 1-9 3-10 10-1-7-3-9-10-10 7-1 9-3 10-10Z"/>',
]

export function riskNodeImage(score: number, color: string) {
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 64 64"><defs><radialGradient id="b" cx=".3" cy=".2"><stop stop-color="${color}" stop-opacity=".3"/><stop offset="1" stop-color="#0b1711"/></radialGradient></defs><circle cx="32" cy="32" r="30" fill="url(#b)" stroke="${color}" stroke-width="2"/><circle cx="32" cy="32" r="25" fill="none" stroke="${color}" stroke-opacity=".25"/><g transform="translate(20 19)" fill="none" stroke="${color}" stroke-width="1.8" stroke-linejoin="round" stroke-linecap="round">${glyphs[riskIndex(score)]}</g></svg>`
  return `data:image/svg+xml;charset=utf-8,${encodeURIComponent(svg)}`
}
