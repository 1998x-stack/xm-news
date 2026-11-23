---
name: xm-news-daily-research
description: Produce source-grounded daily Chinese news, A-share/Hong Kong market, macro and global-media research; publish an evidence-led responsive HTML briefing to XM News GitHub Pages and email a concise verified delivery summary.
---

# XM News Daily Research

This project skill specializes the vendored `olah-style-paper-posts` visual method for daily journalism and financial-market research. It is the project-specific operating contract for `xm-news`; the upstream Olah Skill remains unchanged and is used for narrative pacing, semantic HTML, SVG craft and browser QA.

## Mission

Turn a day's information flow into a durable research record, not a headline collage. The reader should understand what happened, what is known, what may explain it, what contradicts that explanation, and what observable evidence would change the conclusion.

## When to use

Use for every daily issue and for updates to an existing daily issue. Also use for special reports about China policy, A/H-share markets, macroeconomics, global technology and international relations. Do not use this skill for personal investment recommendations or for reproducing paywalled articles.

## Mandatory output bundle

For date `YYYY-MM-DD`, create or update:

1. `content/YYYY-MM-DD.md` — full Chinese research note.
2. `data/YYYY-MM-DD.json` — structured facts, market observations, article metadata, source IDs and limitations.
3. `sources/YYYY-MM-DD.md` — evidence register with URL, publisher, publication time, retrieval time, locator, verification status and caveat.
4. `posts/YYYY-MM-DD/index.html` — standalone visual article.
5. Refresh `README.md` only when project instructions or structure change.
6. Run `python scripts/validate_news.py`, unit tests, the Olah static validator and Chromium QA.
7. Build the Pages artifact with `python scripts/build_site.py --output dist`.
8. Verify the deployment run and live URL. Then email the user a concise digest with the latest verified page URL; if deployment is not verified, clearly label it pending and include the GitHub HTML fallback.

## Ordered workflow — do not skip gates

### Gate 0 — Establish the report boundary

- Resolve report date in `Asia/Shanghai` and capture a real `as_of` timestamp.
- Separate calendar date `D` from the latest completed A-share and Hong Kong trading date `T`.
- State whether each market value is pre-market, intraday, closing, after-hours or futures.
- If the day is a market holiday, do not fabricate a same-day close; use the latest completed session and label it.
- Read the current `AGENTS.md`, `README.md`, source policy, previous report bundle, current workflow and existing open PRs before editing.
- Search for an existing report for the same date. Update it idempotently; do not create duplicate directories or repeated content.

### Gate 1 — Discover and verify sources

Follow [research-protocol.md](references/research-protocol.md). Prioritize official primary sources, then independent wire services and major publishers. Search broadly enough to cover:
- CCTV Xinwen Lianbo: official programme page, full text or item-level transcript where available; distinguish a third-party programme summary from an official transcript.
- China policy and data: State Council, ministries, PBOC, SAFE, NBS, NDRC, NEA, SSE, SZSE, BSE, HKEX and company filings.
- A-share and Hong Kong market closes: exchange/index-owner data or reputable financial data providers; cross-check key index levels and turnover.
- Global markets: US, Europe and Asia cash markets; futures only with an explicit session label; FX, rates, gold, oil and key industrial commodities when material.
- International reporting: The Economist, Bloomberg, Reuters, AP, FT and relevant specialist publications.

Do not treat search snippets as full articles. For paywalled sources, summarize only what is visible in public excerpts, official podcasts, abstracts or authorized syndication. Record access limitations.

### Gate 2 — Build the evidence ledger before conclusions

Every material factual or numerical statement must map to a source ID. Each source record must retain:
- stable ID such as `S01`;
- exact claim supported;
- original URL or authorized syndication URL;
- publisher, publication timestamp and retrieval timestamp;
- locator (section, table, paragraph, announcement clause or named data field);
- verification state: `verified`, `derived`, `illustrative` or `unverified`;
- caveat and competing source if definitions conflict.

Use at least one primary source for important policy claims where available. For material market numbers, seek an independent cross-check. If providers disagree, preserve the disagreement and explain the likely scope/refresh-time difference; never average inconsistent values.

### Gate 3 — Analyse markets without false causality

Follow [market-data-protocol.md](references/market-data-protocol.md).

For every market number, record instrument/index, close or snapshot, change, currency/unit, market date, timezone, provider and source ID. Separate A-share indices from Hong Kong indices. Distinguish cash-market closes from futures and pre-market quotes.

Explain price moves using an evidence chain:
`observed move → information available before the move → plausible transmission mechanism → confirming evidence → counter-evidence`.

Do not attribute a move to a policy announced after the market close. Do not turn theoretical financing capacity into realized capital inflow. Label analyst estimates and stress scenarios as estimates/scenarios, not official data. Include a downside case and state what evidence would falsify the main interpretation.

### Gate 4 — Write for a reader who missed the day

Use this article architecture unless the day's facts require a better one:
1. Five-line executive summary.
2. News broadcast: item list grouped by public service, policy, technology/industry and international affairs.
3. China A-share close and market breadth.
4. Hong Kong close.
5. Macro, liquidity, FX and policy changes.
6. Global markets and cross-asset signals.
7. The Economist / Bloomberg / Reuters / FT selected article briefs.
8. Cross-market synthesis: 2–4 defensible conclusions and counter-evidence.
9. Next-session watchlist: observable variables, thresholds or release events.
10. Sources, limitations and investment disclaimer.

For each selected international article, include publisher, exact title, publication date, original link, a short original-language summary, relevance and access note. Avoid copying article text.

### Gate 5 — Design the visual article

Use `.agent/skills/olah-style-paper-posts/SKILL.md` and its design/QA references. Follow [editorial-visual-system.md](references/editorial-visual-system.md).

- Use one editorial thesis in the headline, not a sensational prediction.
- Start with the market/policy contradiction that makes the day worth reading.
- Put 3–5 key metrics above the fold, with units and time context.
- Use original SVG to explain relationships and market structure; do not decorate with charts that add no information.
- Every chart needs a meaningful title, accessible description, caption, source IDs and honest axes.
- Use progressive disclosure, responsive tables, visible source links, one H1, semantic sections, keyboard-visible focus, reduced-motion and print styles.
- Keep the page readable with JavaScript disabled. Interactions are enhancements, not content gates.
- No external fonts, scripts, analytics or chart APIs. Keep the article self-contained.
- Never place internal process notes, prompt text, model names or production claims in the reader-facing article.

### Gate 6 — Validate the complete daily bundle

Run:
```bash
python scripts/validate_news.py
python -m pytest -q
python .agent/skills/olah-style-paper-posts/scripts/validate.py posts/YYYY-MM-DD/index.html
python .agent/skills/olah-style-paper-posts/scripts/browser_check.py posts/YYYY-MM-DD/index.html --output /tmp/xm-news-qa
python scripts/build_site.py --output dist
```

Validate JSON syntax and date; required data fields; source IDs and URLs; market units; article structure; SVG accessibility; local anchors; mobile overflow at 360/390px; tablet at 768px; desktop at 1440px; browser console and failed requests; print mode; and navigation to the archive. Do not report a test as passed unless it actually ran.

### Gate 7 — Publish and deliver

- Commit the complete date bundle to the repository default branch using the approved GitHub workflow. Preserve prior reports.
- The Pages workflow must build a curated static artifact from `data/` and `posts/`, not publish the repository's hidden skill directories or development scripts.
- Verify the latest GitHub Actions deployment run corresponds to the commit just published and has a successful conclusion.
- Verify `https://1998x-stack.github.io/xm-news/` and the day's article URL are reachable before calling them live.
- Send an email to `the recipient configured privately in the automation` with the date, 3–5 core conclusions, market table, material risks, latest verified GitHub Pages URL, and repository/HTML fallback.
- If Pages or CI is unavailable, still send a concise status email, explicitly mark publication as pending/failed, include the GitHub article source URL, and state the exact blocker. Never invent a live URL or claim a successful deployment without evidence.

## Quality bar

A report is ready only when:
- all material claims are source-backed;
- fact, media interpretation, inference and scenario are visibly separated;
- time, trading session and units are unambiguous;
- at least one counterargument or uncertainty accompanies each major conclusion;
- the HTML explains rather than merely repeats the Markdown;
- CI/browser checks and Pages state are honestly reported;
- email delivery is attempted only after the report and page link have been checked.

## Companion references

- [Research and source protocol](references/research-protocol.md)
- [Market-data and causal-analysis protocol](references/market-data-protocol.md)
- [Editorial visual system](references/editorial-visual-system.md)
- [Publication and email delivery](references/publication-and-delivery.md)
