# Frontend progress log

## Checkpoint 1 — MVP shell

- Created a Vite + React + TypeScript frontend in `Frontend/` only.
- Added the MoneyGraph dark enterprise fintech layout for a 1440×900 laptop viewport.
- Added mock priority nodes, role and cluster filters, Cytoscape directed graph, GID search, node selection, zoom/pan/fit/reset controls and explainability details.
- Added `npm run build` verification; production build passes.
- Backend, AI-agent and other team folders were not modified.

## Checkpoint 2 — multilingual visual design

- Added RU/KZ/EN design preview with persistent language selection.
- Added five colored priority avatars, decorative Kazakhstan backdrop, selected-edge motion and pause/reduced-motion support.
- Fixed the viewport layout; panels scroll independently without expanding the graph canvas or document.
- Added role/cluster/priority coloring and graph filtering; verified GID search and language switching in the browser.
- Production build passes. No software installed; backend and graph packages were read only.
- Design scope and limitations are described in `docs/DESIGN.md`.

## Checkpoint 3 — map motion and visual icon system

- Inspected the user's video and Kazakhstan outline reference.
- Replaced the approximate backdrop with a recognizable traced contour, synchronized graph pan/zoom, subtle map drift and a light sweep.
- Added colored particles traveling along directed links, restrained arrival pulses, pause, reduced-motion and hidden-tab handling.
- Added shaded client portraits, all five priority symbols, and role/metric/toolbar icons without new dependencies.
- Removed the decorative-map caption in all languages as requested.
- Scope remains exclusively `Frontend/`; backend and AI implementation is unchanged.

## Next checkpoint

- Align frontend data adapters and copy only the final backend response contract after `Project.md` and team API decisions are available.
