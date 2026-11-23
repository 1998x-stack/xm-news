# Market data and causal-analysis protocol

## 1. Required market observation

Each observation should include:
```json
{
  "instrument": "CSI 300",
  "market_date": "YYYY-MM-DD",
  "as_of": "YYYY-MM-DDTHH:MM:SS+08:00",
  "session": "close | intraday | pre_market | after_hours | futures",
  "value": 0,
  "change_pct": 0,
  "currency": "CNY",
  "unit": "index_points",
  "provider": "source publisher",
  "source_id": "S01"
}
```

The numeric zero above is a schema example only, not a missing-value convention. For unavailable observations use JSON `null`, not 0.

## 2. Market groups

- A-share: Shanghai Composite, Shenzhen Component, ChiNext, CSI 300, STAR 50 and/or BSE 50 where data is available.
- Hong Kong: Hang Seng, Hang Seng TECH, Hang Seng China Enterprises and main-board turnover.
- China liquidity: PBOC reverse repos/MLF/other disclosed operations, maturities, net injection/withdrawal, Shibor and CGB yields.
- FX: USD/CNY central parity, onshore CNY and offshore CNH if available; label each separately.
- Global: US, Europe and Asia indices; cash close vs futures; major yields, USD index, gold, crude oil and key industrial metals when material.

Do not present a futures quote as a cash close. Do not combine USD, HKD and CNY without labeling currency. Distinguish turnover from net capital inflow and financing capacity from realized financing balances.

## 3. Causal analysis chain

For every proposed explanation:
1. Observed market move.
2. Information available to investors before or during that market session.
3. Plausible mechanism (earnings, rates, currency, liquidity, policy, positioning, supply/demand).
4. Corroborating evidence (breadth, turnover, sector leadership, company exposure, filings).
5. Counter-evidence or alternative explanation.
6. What future observation would confirm or falsify the explanation.

If the policy/news appeared after the market close, it can only be a next-session catalyst. Do not use hindsight to explain the already completed session.

## 4. Risk framing

- A one-day rebound is not a trend reversal.
- A policy announcement is not the same as implementation.
- A theoretical credit/margin capacity change is not actual capital inflow.
- A price increase is not necessarily a volume increase.
- A nominal import value increase is not necessarily an increase in physical import quantity.
- A high index return does not imply all constituents or all sectors advanced.
- Analyst estimates and stress scenarios are not official forecasts.

## 5. Watchlist design

A useful watch item contains:
- the variable or event to observe;
- the expected release/observation window;
- a source or data endpoint;
- a condition supporting the thesis;
- a condition contradicting the thesis.

Avoid unsupported price targets or deterministic predictions. No personal investment advice.
