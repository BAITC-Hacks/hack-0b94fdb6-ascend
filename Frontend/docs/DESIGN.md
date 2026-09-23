# Freedom Graph — design preview

The active entry point is `src/DesignDashboard.tsx`, loaded from `src/main.tsx`.
The previous MVP components remain available in the source tree.

- Russian, Kazakh and English translations live in `src/i18n.ts`. The language choice is saved locally when browser storage is available.
- Five visual review-priority tiers: critical (coral), high (amber), medium (yellow), low (green), minimal (cyan). Thresholds are presentation-only mock conventions, not a bank-approved methodology or a probability of misconduct.
- The stylized Kazakhstan silhouette is built in code. It is not a map of client locations or an authoritative boundary dataset.
- Cytoscape provides directed edges, node selection, pan, zoom and fit. Role, cluster and priority coloring are selectable. Role/cluster/priority filters apply to the visible graph and client list.
- Directed paths carry colored particles and soft arrival rings; selected-node paths receive emphasis. The flow canvas follows Cytoscape curve geometry and never intercepts pointer input. Rendering is capped at 30 fps, 80 paths and 2× pixel density.
- The Kazakhstan contour follows the supplied silhouette reference. It pans and zooms with the graph, with subtle ambient drift and a clipped light sweep. No map disclaimer is displayed in the interface at the user's request; it remains a visual backdrop, not client geolocation.
- The user's supplied logo and five priority portraits are stored unchanged under `src/assets/`. The portraits appear in the client list, details, priority scale and priority-colored graph. In role/cluster color modes, compact vector markers preserve the selected color encoding. Role, metric and mode icons use the existing icon library.
- Pause and `prefers-reduced-motion` disable continuous movement. Particle rendering also stops in hidden tabs. Animation frames, listeners and resize observers are cleaned up on unmount.
- Laptop layout fits the viewport with independent sidebar scrolling. Narrow screens use a finite vertically stacked layout.
- Preview uses 10 synthetic nodes and 14 synthetic edges, marked as demo data. Counts describe the mock data actually displayed; no real analysis is claimed. API integration is outside this design change.
- No dependencies, remote fonts or external runtime services were added. Images are bundled with Vite using local asset imports, never `file://` URLs. Artwork remains accompanied by localized priority text; the images do not add duplicate screen-reader labels.

Validation: production TypeScript/Vite build; `node --test tests/flowAnimation.test.mjs` checks movement, pause, reduced motion, hidden tabs and cleanup. Browser verification covers RU/KZ/EN, GID search, synchronized map zoom, animation pause and laptop viewport bounds.
