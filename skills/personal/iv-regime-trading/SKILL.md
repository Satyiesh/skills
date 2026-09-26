---
name: iv-regime-trading
description: Run my IV-regime options playbook for NSE index/stock and MCX commodity options — daily regime check, pre-trade checklist, and reviewing a proposed or open trade against my rules. Use when I ask what to trade today, whether a trade fits my system, how to manage an open options position, or mention IV rank/percentile, India VIX, iron condors, IV crush or earnings plays.
---

# IV-regime trading

My rules live in [RULES.md](./RULES.md). They are fixed decisions, not suggestions — apply them as written and flag any deviation instead of improvising. Every threshold there is a **starting value under validation**; the current stage of the rollout decides the size I'm allowed to trade.

The backtester and daily regime tool is the `iv-regime-backtester` repo (`ivrb` CLI): `ivrb regime` for the daily check, `ivrb backtest` for index condors, `ivrb backtest-stocks` for the results trades, `ivrb backtest-mcx` for commodities. Prefer running it over estimating numbers by hand.

## Daily regime check

1. Make sure the day's NSE bhavcopy (and MCX, India VIX) are in the data folder — `ivrb download --start <date> --end <date> --out data/nse` for NSE.
2. Run `ivrb regime --data data/nse --vix data/vix --events data/events.csv`.
3. For each underlying report the regime and the one-line reason, then list the **actions** the rules allow today: new entries (by trade type), and exits/cuts due on open positions.
4. If `data/events.csv` has nothing in the next 15 days, say so — a stale event calendar silently breaks the BUY, event-crush and event-exit rules.

## Reviewing a proposed trade

Walk the pre-trade checklist in RULES.md top to bottom and answer each line **pass / fail / unknown** with the number that decided it. Any fail → the answer is "don't take it", with the failing line. Unknowns → name the data needed. Never resize or re-strike a trade to make it pass unless the rules themselves produce that structure.

## Managing an open trade

Check the exit rules in RULES.md in their stated order (first match wins) against today's prices. State which rule fires, or that none does and what level would trigger the nearest one. **No adjustments** — the only actions are hold, cut, or close.

## Where the system stands

Rollout stage (update this line as it changes): **Stage 1 — backtesting.** Milestones 1–4 (regime engine, index iron condor, stock run-up and crush, MCX condors and strangles) built; portfolio simulation not yet. Until a trade type passes its gates, it is paper-only.
