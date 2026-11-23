# Research and source protocol

## 1. Source hierarchy

| Tier | Source | Examples | What it can establish |
|---|---|---|---|
| P0 | Original primary source | CCTV programme page, government, ministry, PBOC, SAFE, NBS, NEA, SSE, SZSE, HKEX, listed-company filing | Official statements, rules, raw releases, issuer facts |
| P1 | Independent major publisher / wire | Bloomberg, The Economist, Reuters, AP, FT | Reported events, independent context, editorial analysis |
| P2 | Financial data provider / specialist publication | Exchange data distributors, China Securities Journal, Yicai, NBD, financial data terminals | Market close, cross-checks, specialist context |
| P3 | Aggregator, social media, newsletter | Search mirrors, reposts, public social posts | Discovery leads only; never sole support for a material claim |

A high-authority source is not automatically the right source for every claim. A government release establishes what the agency announced; it does not prove that a policy has already changed private-sector behavior. An opinion column establishes the author's view, not an objective consensus.

## 2. Search plan

Search at least the following buckets and keep the query date explicit:
1. Official Xinwen Lianbo daily page and item transcript.
2. Major policy announcements and official data releases of the day.
3. A-share and Hong Kong market close, breadth, turnover and sector performance.
4. PBOC liquidity, Shibor, USD/CNY, CGB yields and relevant commodities.
5. Global cash-market closes and futures, clearly separated by session.
6. The Economist, Bloomberg, Reuters, AP and FT articles published in the last 24–72 hours.
7. Relevant industry/issuer filings where an article makes a company-specific claim.

Do not infer publication date from a URL slug alone. Verify the page's date, update time and timezone. When the article date differs from the event date, record both.

## 3. Evidence ledger fields

For each source:
- `id`: stable within the report, e.g. `S01`;
- `claim`: one concise factual proposition supported;
- `url`: canonical source URL or clearly labeled authorized syndication;
- `publisher`: publisher or issuing body;
- `published_at`: timestamp/timezone if available;
- `retrieved_at`: actual retrieval timestamp/timezone;
- `locator`: section, paragraph, table, chart or announcement clause;
- `status`: `verified`, `derived`, `illustrative`, `unverified`;
- `access_note`: full text, abstract, snippet, podcast notes, syndication or paywall;
- `limitations`: scope and conflicts.

## 4. Cross-check policy

- Official regulation text beats media paraphrase.
- For an important market close, prefer exchange/index-owner data plus one independent provider.
- If two providers disagree, preserve both values and describe their sample, timestamp or definition if known.
- If the reason for a market move is only attributed by market participants, say "媒体/交易员将其归因于" rather than stating direct causation.
- If a source is unavailable, do not pretend to have read it. Use an alternative and mark the original as inaccessible.
- Search snippets may discover a source but should not be treated as full-text evidence.

## 5. News selection

Prioritize:
- official policy with an identifiable instrument, responsible agency, effective date or budget;
- new macroeconomic data that changes the base case;
- market events with broad cross-asset or cross-sector transmission;
- technology/industry developments with named issuers and verifiable exposure;
- international events with direct implications for China, trade, energy, capital flows or security.

Avoid filling the page with low-impact routine headlines. Keep the full programme headline list separate from the editor's top stories.

## 6. Contradictions and missing information

Record contradictory statements in a "source conflicts" subsection:
- source A and source B;
- what each actually measures;
- likely difference in scope/time/definition;
- which value is used in the main text and why.

Use null/unknown for missing numbers. Never convert missing to zero. Never fabricate article titles, quotes, source locators, URLs, data points or publication times.
