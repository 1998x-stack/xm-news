---
name: xm-news-daily-research
description: Daily source-grounded research across politics, finance, economy and livelihood, using Chinese, Western, Asian regional, multilateral and social sources; publishes a four-pillar portal and four standalone HTML pages.
---

# XM News Daily Research

XM News is a four-pillar public-affairs research platform, not a financial-only digest. Every issue covers politics, finance, economy and livelihood independently, with evidence-backed cross-pillar connections.

Use `olah-style-paper-posts` for narrative design, semantic HTML, SVG, CSS and browser QA. Keep upstream Olah unchanged; this Skill defines XM News research and editorial rules.

## Daily outputs
For YYYY-MM-DD:
- content/YYYY-MM-DD.md cross-pillar summary.
- content/YYYY-MM-DD/{politics,finance,economy,livelihood}.md.
- data/YYYY-MM-DD.json with four section records, metrics, source IDs, caveats and routes.
- sources/YYYY-MM-DD.md with claim-source ledger, independence, verification and access notes.
- sections/YYYY-MM-DD/{politics,finance,economy,livelihood}/index.html.
- index.html main four-card portal.
- Keep legacy posts/YYYY-MM-DD/index.html as financial archive.
- Validate, test, build dist/, deploy Pages, verify public URLs, then email.

## Pillars
- Politics: domestic governance, major meetings, diplomacy, international relations, security, law, regulation and public administration.
- Finance: A/H shares, bonds, rates, FX, central banks, banks, insurance, funds, regulation, capital flows and global markets.
- Economy: production, consumption, investment, trade, property, fiscal policy, industry, energy, technology, enterprises and productivity.
- Livelihood: employment, wages, housing, education, healthcare, pensions, social insurance, elderly care, childcare, safety, community services and consumer rights.

A quiet news day is not a reason to insert unrelated headlines. Use structural indicators or ongoing issues and state the information gap.

## Source roles, not country ranking
Use docs/source-directory.md and config/source-catalog.json.
- P0: original documents, official statements, raw statistics, regulations, judgments and filings.
- P1: major wire services and independent news reporting.
- P2: specialist, financial, regional, academic and think-tank sources.
- P3: social media and personal accounts for leads/viewpoints only.

P0 is direct evidence of what an institution published, not an independent verdict on every disputed claim. P1/P2 are not automatically neutral. Record institutional role, editorial form, access and caveats. Do not count Reuters republished by CNA and The Straits Times as three sources; same-wire copies, translations and multiple sites quoting one notice are one evidence lineage.

## X / Twitter
Authenticate official accounts via the institution's own website. Capture original URL, handle, timestamp, edit state and retrieval time. Verify photos/video with reverse search, geolocation, time/weather/context and original uploader. A checkmark, follower count, repost volume or screenshot is not proof. Never rely on an unverified social post alone for material political, financial, safety or casualty claims.

## Workflow
1. Resolve report date D in Asia/Shanghai. Separate event, publication, retrieval, market and effective dates.
2. Read main, README, AGENTS, Skill, source policy, latest issue, open PRs, Actions and Pages. De-duplicate date D before writing.
3. Search domestic official/professional sources, Western wires/specialists, Asian regional sources, international organizations and social leads.
4. Build evidence ledger before prose: claim_id, source_id, URL, publisher, published_at, retrieved_at, locator, source_role, institutional_position, independence_cluster, verification, confidence, access_note, caveat, counter_evidence.
5. Classify material statements as 【事实】【官方表述】【媒体观点】【分析推断】【情景】. Keep disagreements visible; never average incompatible numbers.
6. Search snippets are discovery aids, not proof of full-text access. Paywalled content uses public excerpts, podcasts, abstracts or authorized syndication only.
7. Each pillar needs thesis, 3–4 facts, timeline/baseline, source comparison, mechanism, counter-evidence, uncertainty, next observations and sources.
8. Each HTML has one H1, semantic H2/H3, 3–4 fact cards, accessible original SVG, source cross-check, source links, confidence and caveats. Support mobile, keyboard focus, reduced motion and print. No remote fonts, external JS, analytics or third-party charts.
9. Portal is a four-card overview, not a fifth mixed article.
10. Validate data/source IDs and all four pages; run pytest, Olah static validation and Chromium QA for all four.
11. Build only dist/ for Pages. Check CI head SHA, deploy result, environment URL and actual public URLs.
12. Email private automation recipient with four findings, risks, portal plus four section links, commit, CI and deployment state.

## Domain discipline
Finance: label instrument, market date, session, provider, unit and currency; futures are not cash closes; theoretical financing capacity is not realized inflow.
Economy: separate nominal/real, single-month/cumulative, YoY/MoM; sector/company case is not national aggregate.
Politics: distinguish statement, joint statement, draft, law, regulation, briefing and local pilot.
Livelihood: policy target is not achieved outcome; local case is not national coverage; aggregate employment is not proof all groups are secure.
Do not infer causality from same-day co-movement.

## QA
```bash
python scripts/validate_news.py
python -m pytest -q
LATEST=$(python scripts/validate_news.py --print-latest-date)
for section in politics finance economy livelihood; do
  python .agent/skills/olah-style-paper-posts/scripts/validate.py "sections/$LATEST/$section/index.html"
  python .agent/skills/olah-style-paper-posts/scripts/browser_check.py "sections/$LATEST/$section/index.html" --output "/tmp/xm-news-qa/$section"
done
python scripts/build_site.py --output dist
```

Never report a check that did not run. If Pages or email fails, report PENDING/FAILED and provide GitHub source links.
