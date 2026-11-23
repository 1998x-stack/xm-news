# XM News Date-First Pages Architecture

## Reader route
\`\`\`text
/                                 home: all daily issues, filter by exact date/year/month
└── /issues/YYYY-MM-DD/            day hub: core events + China/West/Singapore/Asia lenses
    ├── politics/                 political governance/diplomacy
    ├── finance/                  financial markets/monetary policy
    ├── economy/                  macroeconomics/industry/trade
    └── livelihood/               public services/living conditions
\`\`\`
All nested URLs are immutable by date. /politics/, /finance/, /economy/, /livelihood/ are latest aliases for compatibility. /posts/YYYY-MM-DD/ retains legacy finance pages. /archive/ mirrors the complete date chronology.

## Build inputs vs generated outputs
\`\`\`text
data/YYYY-MM-DD.json + editorial.lenses + editorial.observations
sources/YYYY-MM-DD.md       content/YYYY-MM-DD.md
sections/YYYY-MM-DD/{pillar}/index.html
               │
               ▼
         build_site.py + site_views.py
           ├─ all dates from data/
           ├─ static date cards and time filters
           ├─ date hub and regional source lenses
           ├─ four pillar links scoped to the same date
           └─ dist/ only
               │
               ▼
GitHub Pages: home / issues / aliases / archive / days.json / source-guide
\`\`\`

## Detailed outputs
- dist/index.html: latest complete day feature, number of archived dates, cards ordered newest→oldest; local assets/filters.js enhances exact day/year/month inputs without hiding baseline HTML when JS is disabled.
- dist/days.json: array of {date, four_pillars, url}, same ordering as cards.
- dist/issues/D/index.html: day lead, material as-of, three grounded region views, curated event cards mapped to evidence IDs, accessible conceptual SVG, four module cards, caveats and archive navigation.
- dist/issues/D/{pillar}/index.html: dated article; navigation stays within D.
- dist/assets/site.css and filters.js: local, project-specific, no CDN, no sensitive settings.
- dist/latest.json: current complete report and latest stable routes.
- dist/archive/index.html: complete history with date filters.
- dist/source-guide/ and source-catalog.json: methodology and structured registry.

## Security and validity
Only dist/ is uploaded. Do not expose .agent/.pi, email recipients, keys, test caches or GitHub action credentials. Data inserted in HTML must be escaped; URLs are obtained from trusted repository structure rather than unverified user-supplied paths. For new reports, schema gate requires 3 real-source lenses, a meaningful set of verified observations, four sections and complete sources.

## CI
Run validate-news, pytest, Olah static validation and Chromium QA for four section HTMLs, build dist, then assert date hub/home page and links. Pages workflow head SHA and deployment result must match the commit. A successful deployment action still requires checking public URLs if a browser is accessible.
