import { mkdir } from 'node:fs/promises'
import { resolve, join } from 'node:path'
import { createRequire } from 'node:module'

// Deterministic slicing of the user-supplied sheet; no image generation or recoloring.
// Usage: node scripts/extract-role-cluster-icons.mjs INPUT OUTPUT [SHARP_MODULE_PATH]
const [input, output, sharpModule = 'sharp'] = process.argv.slice(2)
if (!input || !output) throw new Error('Provide the source sheet and output directory.')
const sharp = createRequire(import.meta.url)(sharpModule)
const root = resolve(output)
const icons = [
  { group: 'roles', name: 'risk', label: 'Risk', x: 201, y: 186, radius: 79 },
  { group: 'roles', name: 'sanction', label: 'Sanction', x: 201, y: 342, radius: 79 },
  { group: 'roles', name: 'company', label: 'Company', x: 201, y: 496, radius: 79 },
  { group: 'roles', name: 'transaction', label: 'Transaction', x: 201, y: 647, radius: 79 },
  { group: 'roles', name: 'verification', label: 'Verification', x: 201, y: 796, radius: 79 },
  { group: 'clusters', name: 'red', label: 'Red cluster', x: 927, y: 232, radius: 110 },
  { group: 'clusters', name: 'orange', label: 'Orange cluster', x: 1238, y: 232, radius: 110 },
  { group: 'clusters', name: 'yellow', label: 'Yellow cluster', x: 1551, y: 232, radius: 110 },
  { group: 'clusters', name: 'green', label: 'Green cluster', x: 927, y: 535, radius: 110 },
  { group: 'clusters', name: 'cyan', label: 'Cyan cluster', x: 1238, y: 535, radius: 110 },
  { group: 'clusters', name: 'neutral', label: 'Neutral cluster', x: 1551, y: 535, radius: 110 },
]
const meta = await sharp(input).metadata()
if (meta.width !== 1774 || meta.height !== 887) throw new Error('Expected the original 1774 × 887 sheet.')
await mkdir(join(root, 'roles'), { recursive: true })
await mkdir(join(root, 'clusters'), { recursive: true })
const tiles = []
for (const [index, icon] of icons.entries()) {
  const diameter = icon.radius * 2
  const mask = Buffer.from(`<svg width="${diameter}" height="${diameter}" xmlns="http://www.w3.org/2000/svg"><circle cx="${icon.radius}" cy="${icon.radius}" r="${icon.radius - 1}" fill="white"/></svg>`)
  const crop = await sharp(input)
    .extract({ left: icon.x - icon.radius, top: icon.y - icon.radius, width: diameter, height: diameter })
    .ensureAlpha().composite([{ input: mask, blend: 'dest-in' }]).png().toBuffer()
  const file = join(root, icon.group, `${icon.name}.png`)
  await sharp(crop).resize(256, 256).png().toFile(file)
  const { data, info } = await sharp(file).raw().toBuffer({ resolveWithObject: true })
  if (info.channels !== 4 || data[3] !== 0) throw new Error(`Transparent PNG validation failed: ${file}`)
  const column = index < 5 ? index : index - 5
  const row = index < 5 ? 0 : 1
  tiles.push({ input: await sharp(file).resize(132, 132).toBuffer(), left: 32 + column * 174, top: 64 + row * 220 })
  const label = Buffer.from(`<svg width="160" height="30" xmlns="http://www.w3.org/2000/svg"><text x="80" y="20" fill="#b7c7bb" font-family="Arial,sans-serif" font-size="13" text-anchor="middle">${icon.label}</text></svg>`)
  tiles.push({ input: label, left: 18 + column * 174, top: 200 + row * 220 })
  console.log(`${icon.group}/${icon.name}.png · 256×256 RGBA`)
}
const headings = Buffer.from('<svg width="1080" height="480" xmlns="http://www.w3.org/2000/svg"><g fill="#e3eee5" font-family="Arial,sans-serif" font-size="16" letter-spacing="3"><text x="32" y="36">ROLE ICONS</text><text x="32" y="256">CLUSTER ICONS</text></g></svg>')
await sharp({ create: { width: 1080, height: 480, channels: 4, background: '#0c1612' } })
  .composite([{ input: headings }, ...tiles]).png().toFile(join(root, 'preview.png'))
