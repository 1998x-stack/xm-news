# XM News editorial visual system

## 1. Editorial principle

The article is a research feature, not a trading terminal or marketing dashboard. Use the Olah-style narrative sequence: tension → baseline facts → mechanism → evidence → counter-evidence → synthesis. A chart should reduce cognitive load, not decorate the page.

## 2. Design tokens

| Token | Value | Use |
|---|---|---|
| Paper | `#fffdf9` | Main reading surface |
| Ink | `#203035` | Primary text |
| Muted | `#53676d` | Captions and secondary labels |
| Teal | `#147f80` | Positive/structural path; not a universal bullish signal |
| Coral | `#b85b47` | Negative/risk path |
| Amber | `#916c22` | Caveats and uncertainty |
| Border | `#dce8e4` | Separators and cards |
| Wash | `#f3f9f6` | Quiet callouts |

## 3. Information hierarchy

1. Brand/date/as-of time.
2. One headline with a real tension, not a prediction.
3. One-sentence dek explaining the key contradiction.
4. 3–5 metric cards, each with unit and data time.
5. Executive takeaways with confidence/caveat.
6. Thematic sections with one argument per section.
7. Original diagrams and market tables.
8. Inline source links and a complete source register.
9. Limitations and investment disclaimer.

## 4. Charts and diagrams

- Label axes, units, dates and source IDs.
- Show zero baselines for bar charts unless a clearly stated reason requires another scale.
- Do not use dual axes to imply correlation.
- Use direct labels; avoid legends that force readers to decode colors.
- Every figure has `title`, `desc`, `role="img"`, `aria-labelledby` and a nonempty `figcaption`.
- Distinguish factual charts from conceptual mechanism diagrams. Label conceptual diagrams "机制示意图，不代表定量因果关系".
- Use source-backed values only. No decorative data or fake precision.
- Use original SVG; do not reuse Bloomberg/Economist chart artwork or logos without permission.

## 5. HTML and accessibility

- Exactly one H1; H2 for main sections; H3 for subsections.
- Use semantic `main`, `article`, `nav`, `section`, `figure`, `figcaption`, `table`, `caption`, `th scope`.
- Add a skip link, visible focus, useful link text and keyboard-operable buttons.
- Keep core content visible when JavaScript is disabled.
- Include responsive design for 1440, 768, 390 and 360 px, print mode and reduced motion.
- Avoid external fonts, analytics, JS bundles and chart services. Inline critical CSS/JS and SVG.
- Long source URLs must wrap and never widen the viewport.

## 6. Homepage and archive

- Homepage: latest issue, three key takeaways, selected market snapshot, links to archive and methodology.
- Archive: reverse chronological list with date, title, short summary and topic tags.
- Article: standalone, source-linked, navigable, responsive and printable.
- Keep article content in `posts/YYYY-MM-DD/index.html`; site build copies only approved public pages into the Pages artifact.
