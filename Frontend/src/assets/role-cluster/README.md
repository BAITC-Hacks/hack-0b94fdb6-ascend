# Role and cluster PNG artwork

Eleven icons extracted from the user-supplied sheet dated 23 September 2026, 15:25:13.
Each icon is a 256×256 RGBA PNG. Original glyphs and colors are preserved, text is excluded,
and the area outside the circular frame/glow is transparent. The dark interior is intentional.
The source crops were approximately 158×158 (roles) and 220×220 (clusters); 256px exports
standardize their size and do not add source detail.

- `roles/risk.png`: red flame
- `roles/sanction.png`: yellow warning triangle
- `roles/company.png`: green four-point symbol
- `roles/transaction.png`: cyan bars
- `roles/verification.png`: green checked shield
- `clusters/red.png`, `orange.png`, `yellow.png`, `green.png`, `cyan.png`, `neutral.png`: network groups
- `preview.png`: contact sheet for review, not an application icon

The artwork is connected through `src/data/networkArtwork.ts`. The sheet's role names are not
replacements for the application's analytical roles. Cluster colors do not assert a risk
classification. The neutral gray icon is included in the archive but is not added to the
dashboard's five-color palette.

Current role mapping: consolidator → yellow group; transit → cyan bars; distributor → orange
group; terminal → green shield; coordinator → red group; peripheral → green star. The red
flame marks the priority list; the yellow triangle accompanies the analytical-hypothesis notice.
Cluster IDs 1 / 2 / 3 use green / yellow / cyan groups respectively. PNG icons appear in the
graph, mode-aware client list, details and localized legends. Scores and role assignments are unchanged.

Reproduce with `scripts/extract-role-cluster-icons.mjs`, passing the source sheet, output directory,
and the path to an already available Sharp module. No project dependency was added.
