# XM News: Event-first multilingual editorial method

## Editorial objective
“What did the world observe **on this date**?” is the question. Do not start from Xinwen Lianbo's broadcast rundown. Define a date window, then observe events covered by Chinese original materials, Western reporting, Singapore/Asian outlets and global datasets. Each source family contributes **its actual documented evidence**, not an artificially opposing stance.

## Candidate event schema
\`\`\`json
{
  "event_id": "D-slug",
  "event_date": "YYYY-MM-DD",
  "observed_at": "2026-11-23T21:00:00+08:00",
  "pillar": "politics | finance | economy | livelihood",
  "primary_claim": "...",
  "source_ids": ["S01","S02"],
  "independence_clusters": ["official-release-123","reuters-wire-123"],
  "new_information": "...",
  "affected_groups": ["..."],
  "source_positions": {"China":"...","West":"...","SingaporeAsia":"..."},
  "disagreements": ["..."],
  "unverified": ["..."]
}
\`\`\`

## Ranking without fake quotas
Use an editorial rubric (not a mathematical truth): materiality to public decisions, cross-border reach, novelty from yesterday, independent evidence depth, long-term significance, and disagreement requiring explanation. Don't prefer a sensational but poorly supported item over a substantiated high-impact story. Suggest 5–10 events when warranted, not a quota.

## Independent evidence
- Primary government press release + its translated page is **one official claim**.
- Reuters carried by CNA + Straits Times + portal copies is **one Reuters article lineage**.
- Bloomberg ETF market flow cited by FT or other media is **one market-data source**, though independent reporting may add interviews and context.
- Social media and viral clips must be authenticated and contextualized, not merely referenced.
- An independent journalist's own interview is a distinct contribution even if it references an existing official notice.

## Visual grammar
- Home uses **time-axis cards, date/year/month filters**; date is the primary interactive key, not pillars.
- Day hub uses 3 real-region perspective panels, 5–10 curated event cards, a conceptual 3-lane evidence diagram, then four detailed pillar entry cards.
- Individual pages contain an evidence comparison, original diagrams and accessible references. Chart metric numbers must be traceable to source data, with axes/date/units where applicable. Don't turn commentary into a visual statistic.
- All content must work without JavaScript; progressive filtering cannot be the only route to a day.

## Non-negotiable uncertainty labels
【事实】【官方表述】【媒体分析】【推断】【情景】 and explicit access restrictions, conflicts, unsourced claims and missing perspectives. If Singapore sources add no independent information on a specific story, state that; do not call them neutral arbitrators.

## Publication
Use dated canonical URLs. Preserve previously published dates even if editorial templates evolve. Keep source files and four module Markdown/HTML independent. Build dist and verify the full 3-hop navigation before reporting public delivery.
