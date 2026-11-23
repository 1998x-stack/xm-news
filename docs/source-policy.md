# Source policy and evidence ledger

## Source tiers

| Tier | Source type | Examples | Use |
|---|---|---|---|
| P0 | Primary / official | CCTV, Xinhua, State Council, PBOC, SAFE, SSE, SZSE, BSE, HKEX, NEA, ministries | Establish official statements, rules, releases and original data |
| P1 | Major wire / editorial publisher | Bloomberg, The Economist, Reuters, AP, FT | Independent reporting, analysis, international context |
| P2 | Financial data and specialist media | China Financial Information Network, China Securities Journal, Yicai, NBD, HKEJ, Eastmoney Choice | Market close, cross-check, market color |
| P3 | Aggregators / social / newsletters | Search result mirrors, reposts, social accounts | Discovery only; never the sole basis for material facts |

## Evidence record

For every key claim, retain:

- `id`: stable identifier.
- `claim`: exact claim being supported.
- `source_url`: original or authorized publication URL.
- `publisher` and `published_at`: provenance and publication time.
- `retrieved_at`: retrieval time in Asia/Shanghai.
- `locator`: paragraph, section, table, line, or named data field.
- `status`: `verified`, `derived`, `illustrative`, or `unverified`.
- `caveat`: scope, discrepancy, paywall, estimate or other limitation.

## Cross-checking

1. Official policy text takes precedence over media paraphrase.
2. For index close, compare at least two reputable sources when possible.
3. For turnover and market breadth, preserve source-level definitions. Do not average inconsistent counts.
4. A futures price is not an underlying cash-market close.
5. If only a headline/abstract/podcast description is available, say so.
6. If a source page is inaccessible, record the search result or syndication source used and do not imply the original page was read.

## Daily report structure

1. Executive summary — no more than five central conclusions.
2. News broadcast — all headline items, grouped by theme.
3. China markets — A-share, HK, liquidity, FX and policy.
4. Global markets — US/Asia/Europe, rates, FX and commodities.
5. International publications — Economist/Bloomberg/Reuters/AP article summaries.
6. Synthesis — mechanisms, cross-market transmission and competing explanations.
7. Watchlist — observable indicators, not unsupported predictions.
8. Sources and limitations.

## Copyright

Summarize rather than reproduce. Link to the original publisher, keep direct quotations brief, and do not copy proprietary charts or photographs. A search snippet is not permission to republish an article.
