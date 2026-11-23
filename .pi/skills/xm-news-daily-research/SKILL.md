---
name: xm-news-daily-research
description: Event-first multilingual daily public-affairs research. Discover and verify major events across China, Europe/US, Singapore and Asia, publish dated hub with four pillar articles and source lineage.
---

# XM News Daily Research | Event-first v4

## Mission
Build a **daily-first, event-first** editorial publication. The reader journey is:
1. **首页 /** → chronology of report dates, exact-date/year/month filter.
2. **/issues/YYYY-MM-DD/** → one day of important events, comparing China/Western/Singapore–Asia lenses, then four modules.
3. **/issues/YYYY-MM-DD/{politics,finance,economy,livelihood}/** → standalone deep-dive.
Maintain four stable latest aliases (/politics/, /finance/, /economy/, /livelihood/) and old /posts/ as historical compatibility.

**Do not use CCTV Xinwen Lianbo (or any single publisher) as the top-level issue list.** It is a candidate source, not the agenda. News is selected by material events, cross-border consequences, novelty, evidence quality and reader relevance. A source's nationality is not a guarantee of neutrality.

## Read before action
Read AGENTS.md, README.md, docs/daily-operating-procedure.md, docs/source-directory.md, docs/source-policy.md, docs/github-pages-architecture.md, config/source-catalog.json, plus this Skill, the vendored Olah narrative/HTML/SVG references, latest main/CI/Pages, past issues, open PRs and Gmail Sent. Keep this Skill byte-identical with its .pi mirror.

## Editorial funnel — never skip
### Gate 1: Candidate discovery
Search independently, rather than from the TV broadcast table of contents:
- **China:** policy/government originals, CCTV/Xinhua/People's Daily/Qiushi as leads, national and provincial original data and disclosures; Caixin/Yicai/other professional reporting.
- **Europe and Americas:** Reuters/AP/AFP, Bloomberg, Financial Times, Economist, WSJ, BBC, major investigative outlets and official counterparty releases.
- **Singapore and Asia:** Singapore PMO/MFA/MTI originals, CNA, The Straits Times, Nikkei Asia, SCMP, ISEAS/Fulcrum, East Asia Forum and relevant local sources.
- **Transnational:** IMF/World Bank/OECD/WTO/ILO/WHO/BIS/IEA and papers where relevant.
- **X/Twitter and other social:** tips and primary statements only after account/URL/timestamp/media provenance checks; never a sole basis for a major claim.

Track distinct searches and truly relevant, verifiable hits by source region. If a region lacks relevant verified material, say so; never fill artificial source quotas.

### Gate 2: Candidate scoring and deduplication
Record each candidate event's **event_date, published_at, observed_at, source IDs, originality, affected groups/markets, consequences, confirmation, conflicting evidence**. Group syndicated/translated versions of the same Reuters/AP/Xinhua report in one independence cluster. Group several media citations of a single government notice as one primary evidence lineage.
Prioritize significance, cross-region relevance, novelty, direct evidence, audience value and uncertainty. Select a compact set of ~5–10 high-value events, with a real reason for each; daily material need not be evenly split across publishers. Do not make coverage of Xinwen Lianbo a gating condition.

### Gate 3: Evidence and comparative interpretation
For important claims record claim_id, source_id, URL, publisher, source_region, published_at, retrieved_at, locator, access_mode, original/syndication lineage, source_role, confidence, limitations, alternative explanation and counter-evidence.
For the same event distinguish:
1. shared documented facts,
2. different emphasis/framing among Chinese, Western, Singapore/Asia outlets,
3. what the independent reporting actually adds,
4. what is contested or not verified.
Paywalled articles: summarize only accessible excerpt/authorized reprint/public audio notes; never pretend to have read a complete article.
Use explicit labels 【事实】【官方表述】【媒体分析】【推断】【情景】. Headlines and causal market narratives are not proof.

### Gate 4: Four pillar assignment
Map each selected event to a **primary pillar** (politics/finance/economy/livelihood); cross-link other relevant pillars rather than copying the same event as four separate headlines. Every pillar should have a real insight and relevant independent evidence; if no major breaking news, use honestly labeled ongoing policy/structural observations. 
Finance: market session, instrument, currency, actual/estimated flow; economy: nominal/real, monthly/YTD, YoY/MoM; politics: each party's original statement; livelihood: draft/enacted/implemented and outcome/target.

## Canonical daily bundle
- data/YYYY-MM-DD.json (date, timezone, as_of, market_date, sections, source IDs and **editorial**)
- sources/YYYY-MM-DD.md (claim-source ledger and independent source lineages)
- content/YYYY-MM-DD.md (daily executive thesis) and four content/YYYY-MM-DD/{pillar}.md
- sections/YYYY-MM-DD/{pillar}/index.html (four detailed Olah-style pages)
- index.html date-first **source preview**; scripts/build_site.py generates dist/index.html dynamically from all dated JSON.
- dist/issues/YYYY-MM-DD/index.html (generated date hub, not manually maintained)
- dist/assets/site.css and filters.js (local progressive enhancement)
- dist/days.json for external consumers.
- Keep old financial posts and old dates immutable.

### editorial schema
```json
{
  "editorial": {
    "version": "daily-events-v1",
    "lead": "One day summary",
    "lenses": [
      {"label": "中国...", "outlets": "actual sources used", "summary": "what verified"},
      {"label": "欧美...", "outlets": "actual sources used", "summary": "what verified"},
      {"label": "新加坡与亚洲...", "outlets": "actual sources used", "summary": "what verified"}
    ],
    "observations": [
      {
        "id": "stable-short-id", "pillar": "politics",
        "title": "event-specific", "summary": "verified facts",
        "perspectives": "what each region/source adds",
        "source_ids": ["S01", "S02"], "status": "evidence state",
        "limitation": "important uncertainty or absent evidence"
      }
    ],
    "limitations": ["cross-edition limitations"]
  }
}
```
Lenses must represent actual reporting **with truthful scope**, not a fixed newsroom quota. An empty lens must explicitly say "暂无核实且相关的新信息". Sources referenced by observations must exist in the daily sources file and top-level source_ids.

## UX and visual requirements
- Home: issue count, latest complete issue, **date/month/year filters**, chronological cards; click date leads to date hub. All dates accessible with JS disabled.
- Date hub: date + as_of + cross-border lead, 3 regional source lenses, event cards with provenance IDs/limits, one original accessible conceptual SVG, **four clickable pillar cards**, clear back navigation.
- Pillar articles: single H1, 4+ H2, 3–4 facts/metrics, actual mechanisms, source matrix including conflicting perspectives, original accessible SVG with title/desc/figcaption, risks and concrete observations. Date hub link and date-scoped navigation. No publisher charts copied.
- Use local CSS/JS only, semantic accessible markup, keyboard focus, responsive 1440/768/390/360, reduced motion and print. Javascript is optional progressive enhancement, not required for reading or navigation.

## Quality, release and email
Run real `python scripts/validate_news.py`, `python -m pytest -q`; Olah static `validate.py` and Chromium `browser_check.py` on **all four dated HTML files**; `python scripts/build_site.py --output dist`. Verify home archive, date filter behavior, date-hub links and sources, all four detail pages, and no accidental publication of skills/keys.
Submit once per date to current repository only; respect SHA-based writes and no force pushes. Wait for validate-news and deploy-pages at the matching HEAD, inspect Pages publicly if possible. Do not equate workflow success with independent webpage verification.
Deliver Gmail only to task's configured recipient after checking Sent for duplicates; include **daily hub link and four date-scoped detail links**, main home, brief findings, limitations, commit/CI/Pages status. Failure states are explicit: NOT_RUN / PENDING / FAILED / SUCCESS. Never invent sending or website availability.
If invoked before 21:00 Asia/Shanghai, do not claim the whole day's market closes or evening news are complete. Label early run PRELIMINARY, retain/point to latest complete issue, and let the scheduled evening run produce the final dated issue.
