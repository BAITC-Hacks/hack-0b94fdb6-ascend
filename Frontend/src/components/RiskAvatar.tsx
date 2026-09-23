import type { CSSProperties } from 'react'
import { UserRound } from 'lucide-react'
import { riskColors, riskIndex } from '../i18n'
import { priorityArtwork } from '../data/visualAssets'

/** A compact priority mark; the adjacent text carries its meaning. */
export function RiskAvatar({ score, large = false }: { score: number; large?: boolean }) {
  return <span className={`risk-avatar risk-avatar--minimal ${large ? 'risk-avatar--large' : ''}`} style={{ '--risk': riskColors[riskIndex(score)] } as CSSProperties} aria-hidden="true">
    {large && <UserRound size={22} strokeWidth={1.4}/>}
  </span>
}

const glyphs = [
  '<path d="M12 3 22 21H2Z"/><path d="M12 9v5m0 3v1"/>',
  '<path d="M13 2c2 7-6 7-4 12 1-2 3-3 4-4 7 5 5 12-1 12C2 22 2 12 7 8c0 4 2 4 2 4-1-5 4-6 4-10Z"/>',
  '<path d="M5 20v-6m7 6V9m7 11V3" stroke-width="4"/>',
  '<path d="M12 2 21 6v6c0 5-9 10-9 10S3 17 3 12V6Z"/><path d="m8 12 3 3 5-6"/>',
  '<path d="M12 2c1 7 3 9 10 10-7 1-9 3-10 10-1-7-3-9-10-10 7-1 9-3 10-10Z"/>',
]

export function riskNodeImage(score: number, color: string, useArtwork = false) {
  if (useArtwork) return priorityArtwork[riskIndex(score)]
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 64 64"><defs><radialGradient id="b" cx=".3" cy=".2"><stop stop-color="${color}" stop-opacity=".3"/><stop offset="1" stop-color="#0b1711"/></radialGradient></defs><circle cx="32" cy="32" r="30" fill="url(#b)" stroke="${color}" stroke-width="2"/><circle cx="32" cy="32" r="25" fill="none" stroke="${color}" stroke-opacity=".25"/><g transform="translate(20 19)" fill="none" stroke="${color}" stroke-width="1.8" stroke-linejoin="round" stroke-linecap="round">${glyphs[riskIndex(score)]}</g></svg>`
  return `data:image/svg+xml;charset=utf-8,${encodeURIComponent(svg)}`
}
