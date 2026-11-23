# Publication and email delivery｜Four pillars

## Bundle
content/YYYY-MM-DD.md; four pillar Markdown files; data/YYYY-MM-DD.json; sources/YYYY-MM-DD.md; sections/YYYY-MM-DD/{politics,finance,economy,livelihood}/index.html; index.html; source-guide/index.html; config/source-catalog.json. Keep legacy posts/YYYY-MM-DD as finance archive.

## Build
`python scripts/build_site.py --output dist`. Publish only dist/: portal, four latest pillar routes, date archive, source guide, machine-readable source catalog, archive, latest.json, sitemap, robots and 404. Never expose .agent/.pi, scripts, test caches, private addresses or credentials.

## Routes
`/`, `/politics/`, `/finance/`, `/economy/`, `/livelihood/`, `/issues/YYYY-MM-DD/{pillar}/`, `/source-guide/`, `/source-catalog.json`, `/archive/`, `/latest.json`.

## Deployment
GitHub Actions: validate bundle → pytest → Olah static validation for all four pages → Chromium QA for all four → build dist → upload artifact → deploy. Verify deploy head SHA, conclusion, environment URL and actual public pages. Validation success is not deployment success.

## Email
Subject: XM News｜YYYY-MM-DD 四大板块每日研究. Include four pillar findings, 3–5 cross-pillar conclusions, material risks/data gaps, portal + four page links, commit, CI and Pages state. Recipient stays in private automation config. If Pages pending/failed, state it and include GitHub file links. Never claim delivery without Gmail confirmation.
