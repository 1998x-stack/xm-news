# Market and domain data protocol

## Finance
Retain instrument, market_date, as_of, session (cash close/intraday/after-hours/futures), value, change_pct, currency, unit, provider and source_id. Unknown values are JSON null, never zero. Cover A-share/HK indices, turnover, breadth, PBOC operations, maturities, Shibor, bond yields, CNY/CNH and global cash markets/futures separately. Theoretical credit capacity is not realized inflow.

## Economy
Record period, publication date, unit, geography, YoY/MoM, seasonal adjustment, nominal/real, original source and revision. Never mix single month with year-to-date cumulative figures. Retail/investment/trade often use nominal amounts; industrial output may be a real growth rate.

## Politics
Record issuing institution, document type, issue/publication/effective date and consultation period. Distinguish draft, law, regulation, policy plan, briefing, local pilot and joint statement. For diplomacy, collect relevant parties' own statements. Absence from a press release does not prove a topic was not discussed.

## Livelihood
Separate policy targets from outcomes, draft rules from effective rules, local pilots from national coverage, case studies from representative samples, aggregate employment from youth/platform/regional employment, and price indices from household out-of-pocket burden.

## Causal analysis
Observation → information available at the time → plausible mechanism → supporting evidence → counter-evidence/alternative explanation → future falsifiable observation. Do not infer causality from same-day co-movement.
