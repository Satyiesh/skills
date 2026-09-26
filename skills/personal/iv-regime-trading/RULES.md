# IV-regime rules

Capital ₹10 lakh. Regime-switching with a short-vol bias. NSE index + stock options, MCX minis.

## Regime (daily, per underlying, on ATM 30-day IV)

First match wins:

1. < 120 days of IV history → **STAND_ASIDE**.
2. Scheduled event ≤ 2 days away and near/far monthly IV ≥ 1.10 → **EVENT_CRUSH**.
3. Near-month IV > far-month IV → **STAND_ASIDE** (stress).
4. IV percentile (252d) ≥ 50 **and** IV30 − RV20 ≥ 3 vol pts (indices also: India VIX percentile ≥ 50) → **SELL**.
5. IV percentile ≤ 20 **and** IV30 ≤ RV20 **and** a catalyst 5–15 days away → **BUY**.
6. Otherwise → **STAND_ASIDE**.

## Risk budget

- Max loss per trade: index condor ₹20k · stock crush ₹15k · stock run-up ₹10k at its −40% stop (premium ≤ ₹25k) · crude ₹15k · metals ₹10k · commodity long-vol ₹10k premium.
- Total open max-loss ≤ ₹60k. Book loss on +5 vol pts ≤ ₹30k.
- One underlying/correlated group (e.g. BANKNIFTY + bank stocks) ≤ 40% of total risk. Commodities combined ≤ ₹24k.
- One event-crush trade at a time.
- Month P&L ≤ −₹80k → no new trades this month; close everything below 40% of max profit.

## Trade types

| # | Trade | Regime | Entry | Structure | Exit |
|---|---|---|---|---|---|
| 1 | NIFTY/BANKNIFTY monthly iron condor | SELL | 30–45 DTE, monthly expiry; no event ≤ 10 days | Shorts 15–20 Δ, symmetric wings, credit ≥ ⅓ width, max loss ≤ ₹20k | 50% of credit · 21 DTE · 7 days before event · loss = 2× credit · short Δ ≥ 0.30 |
| 2 | Stock pre-earnings run-up | BUY-style | 10–15 days before results, event-expiry ATM IV ≤ its median at the same distance over the last 8 cycles (min 4) | Long ATM straddle (strangle 1 step OTM if over cap), premium ≤ ₹25k, risk = −40% stop ≤ ₹10k | Close day before results; +30% / −40% |
| 3 | Stock earnings crush | EVENT_CRUSH | Close before results; event move extracted from the first two monthly expiries after results, expected abs move (s.d. × √(2/π)) > avg actual move of last 8 results | Iron fly, wings at first strikes beyond ± one event s.d., max loss ≤ ₹15k | Next morning, win or lose |
| 4 | Crude Oil mini condor | SELL | 25–35 DTE; no OPEC+ within 7 days | Shorts 10–15 Δ, wings ~5 Δ, credit ≥ 20% of wider wing, max loss ≤ ₹15k | 50% · 2× credit · short Δ ≥ 0.30 · OPEC+ within 3 days · 10 DTE |
| 5 | Crude Oil mini strangle | BUY | IVP ≤ 20, IV ≤ RV, OPEC+/geopolitical deadline 5–15 days out | Long 25 Δ call + put on the first expiry spanning the event, ≤ ₹10k | Close before the event; +30% / −40% |
| 6 | Gold mini **or** Silver mini condor | SELL | 25–35 DTE; no FOMC/US CPI within 7 days | Shorts 12–18 Δ, wings ~5 Δ, credit ≥ 20% of wider wing, max loss ≤ ₹10k | 50% · 2× credit · short Δ ≥ 0.30 · FOMC/CPI within 3 days · 10 DTE |
| 7 | Gold/Silver mini strangle | BUY | IVP ≤ 20, IV ≤ RV, FOMC/US CPI 5–15 days out | Long 25 Δ call + put, ≤ ₹10k | Close before the event; +30% / −40% |

Universe: stocks = top ~30 F&O names with ATM spread ≤ 1% of premium; MCX minis need ATM spread ≤ 2% of premium and usable OI. No weekly options. No natural gas until capital > ₹25 lakh. Gold and Silver never together — if both qualify, the larger IV − RV gap wins a sell, the lower IVP wins a buy. One MCX position per group (energy, metals); full-size crude only if the mini fails liquidity.

## Pre-trade checklist

1. Regime today matches the trade type's regime.
2. Expiry/DTE window and event-distance rules met.
3. Strikes at the specified delta; credit/width or premium rule met.
4. Max loss within the per-trade cap for this type.
5. Total open risk, vega (+5 pts), group 40% and commodity caps still hold after adding it.
6. Liquidity gate met (spread, OI); stock not in F&O ban.
7. Exit plan written down: profit target, stop, time/event exit — and for stocks, out before the last 5 trading days of the month (physical settlement).
8. Rollout stage allows real money for this trade type (else paper).

## Management — no adjustments

Exit order, first match wins: stop (loss = 2× credit, gap or intraday) → vol jump → short Δ ≥ 0.30 → profit target → event exit → time exit.

Regime flips, per asset class:
- near IV > far IV → cut short-vol lots by half (once per position);
- India VIX +25% in a day, or an underlying's IV30 +8 vol pts in a day → close all short vol;
- monthly breaker → close everything below 40% of max profit.

## Validation gates (per trade type)

Expectancy > ₹0 after all costs · profit factor ≥ 1.3 · worst month ≥ −10% · recovery ≤ 4 months. Live vs backtest: win rate within ±10 pts, average loss no worse. **A failing trade type is dropped, not tuned.**

Rollout: backtest (3–5 yrs incl. Mar-2020, Jun-2024, 2022 crude) → paper 1–2 cycles → 1 lot / ~25% risk for 2 cycles → full size.
