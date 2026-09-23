# Freedom Graph — design preview

The active entry point is `src/DesignDashboard.tsx`, loaded from `src/main.tsx`.
The previous MVP components remain available in the source tree.

- Russian, Kazakh and English translations live in `src/i18n.ts`. The language choice is saved locally when browser storage is available.
- Five visual review-priority tiers: critical (coral), high (amber), medium (yellow), low (green), minimal (cyan). Thresholds are presentation-only mock conventions, not a bank-approved methodology or a probability of misconduct.
- SVG avatars and the stylized Kazakhstan silhouette are built in code. The silhouette is decorative, not a map of client locations or an authoritative boundary dataset.
- Cytoscape provides directed edges, node selection, pan, zoom and fit. Role, cluster and priority coloring are selectable. Role/cluster/priority filters apply to the visible graph and client list.
- Selected-node edges have a subtle moving dash. Pause and `prefers-reduced-motion` disable continuous movement. Timers and resize observers are cleaned up when the component unmounts.
- Laptop layout fits the viewport with independent sidebar scrolling. Narrow screens use a finite vertically stacked layout.
- Preview uses 10 synthetic nodes and 14 synthetic edges, marked as demo data. Counts describe the mock data actually displayed; no real analysis is claimed. API integration is outside this design change.
- No dependencies, remote fonts, raster assets or external runtime services were added.

Validation: production TypeScript/Vite build; browser rendering, RU/KZ/EN switching, GID search, and viewport overflow check at 1280×720. The browser console had no captured warnings or errors during those checks.
