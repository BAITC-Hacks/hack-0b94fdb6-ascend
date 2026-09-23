# Freedom Graph — design preview

The active entry point is `src/DesignDashboard.tsx`, loaded from `src/main.tsx`.
The previous MVP components remain available in the source tree.

- Russian, Kazakh and English translations live in `src/i18n.ts`. The language choice is saved locally when browser storage is available.
- Five visual review-priority tiers: critical (coral), high (amber), medium (yellow), low (green), minimal (cyan). Thresholds are presentation-only mock conventions, not a bank-approved methodology or a probability of misconduct.
- SVG avatars and the stylized Kazakhstan silhouette are built in code. The silhouette is decorative, not a map of client locations or an authoritative boundary dataset.
- Cytoscape provides directed edges, node selection, pan, zoom and fit. Role, cluster and priority coloring are selectable. Role/cluster/priority filters apply to the visible graph and client list.
- Directed paths carry colored particles and soft arrival rings; selected-node paths receive emphasis. The flow canvas follows Cytoscape curve geometry and never intercepts pointer input. Rendering is capped at 30 fps, 80 paths and 2× pixel density.
- The Kazakhstan contour follows the supplied silhouette reference. It pans and zooms with the graph, with subtle ambient drift and a clipped light sweep. No map disclaimer is displayed in the interface at the user's request; it remains a visual backdrop, not client geolocation.
- Five shaded vector portraits and matching warning/flame/bars/shield/sparkle markers are shared across the UI. Role, metric and mode icons use the existing icon library.
- Pause and `prefers-reduced-motion` disable continuous movement. Particle rendering also stops in hidden tabs. Animation frames, listeners and resize observers are cleaned up on unmount.
- Laptop layout fits the viewport with independent sidebar scrolling. Narrow screens use a finite vertically stacked layout.
- Preview uses 10 synthetic nodes and 14 synthetic edges, marked as demo data. Counts describe the mock data actually displayed; no real analysis is claimed. API integration is outside this design change.
- No dependencies, remote fonts, raster assets or external runtime services were added.

Validation: production TypeScript/Vite build; `node --test tests/flowAnimation.test.mjs` checks movement, pause, reduced motion, hidden tabs and cleanup. Browser verification covers RU/KZ/EN, GID search, synchronized map zoom, animation pause and laptop viewport bounds.
