# MASTER PROMPT — NSE Swing Trading Strategy Research & Backtest

## Role
Act as an expert quant trader and Python engineer. Be skeptical: separate what is verified from what is assumed, never present synthetic or unverified results as real, and never overstate a backtest.

## Goal
Find swing-trade strategies on Indian equities (NSE) that catch +5% to +20% moves within 5–10 trading days, then backtest them honestly on 10 years of NSE bhavcopy data (in-sample / out-of-sample, with realistic costs).

## Repos (all under GitHub user Satyiesh)
| Repo | Role |
|---|---|
| `skills`, branch **`swing-backtest-harness`**, folder `swing-backtest/` | The backtest harness (pandas/numpy). **Primary code to continue.** |
| `NSESwingQuant` | Parquet lake of NSE **cash-market** bhavcopy (unadjusted). Local: `/Users/satyieshmacminipro/projects/NseSwingQuant`. `data/parquet/year=YYYY/month=MM/date=YYYY-MM-DD.parquet`, columns: date, symbol, series, open, high, low, close, prev_close, volume, turnover, isin. Built via `python -m src.cli build` from `nse-quant/data/raw/audit/nse_bhavcopy/*.zip` (~2,100 zips). Parquet is gitignored, so the data lives only on my Mac. |
| `Nse-Historical-Data` | F&O bhavcopy + Dhan/Upstox data store (`nhd`, data root `~/MarketData`, `Store.underlying_daily()` for ~273 F&O stocks). Optional alternative source. Its CLAUDE.md requires updating `docs/HANDOFF.md` at the end of a session. |
| `nse-quant`, `nse-fno-quant` | Other NSE projects; not yet inspected. |

## The 10 strategies (IDs in `swingbt/strategies.py`)
S01 VCP/volatility-contraction breakout · S02 Post-earnings drift (gap + volume + close strength; optional EPS-surprise file) · S03 RSI(2) pullback in uptrend · S04 52-week-high momentum (cross-sectional RS rank ≥ 90th pct) · S05 Gap-and-go pullback to 8-EMA · S06 Capitulation reversal · S07 Short squeeze (needs short-interest data — not available for India, skipped) · S08 Sector-rotation catch-up (needs symbol→sector-index map via `--sectors`) · S09 Insider-cluster + breakout (needs Form-4-style data, skipped) · S10 Bollinger-inside-Keltner squeeze release.

## Harness design (`swing-backtest/`)
- `swingbt/indicators.py` features + liquidity/volatility universe screen. `strategies.py` entry/stop/target/exit specs. `engine.py` trade simulator. `metrics.py` trade stats + realised-P&L portfolio. `context.py` cross-sectional context (RS rank, SPY regime, sector rank, optional EPS/short-interest/insider data). `bhavcopy.py` NSE downloader + corporate-action adjuster + `build-lake`. `run.py` CLI. `tests/` (12 unittest tests).
- **Execution rules (no lookahead):** signal at close of day t → fill at open of t+1 plus slippage; stop wins over target in the same bar; gapped-through stops fill at the open; close-based exits fill next open; one position per ticker; time stop 5–10 days.
- **Universe filter (NSE defaults):** price > ₹50, 20-day avg traded value > ₹10 crore, ATR(14)/close ≥ 3.5%. **Costs:** 12 bps/side fees+taxes + 10 bps slippage.
- **Reporting:** per strategy × IS/OOS/ALL × regime (benchmark above its 200-day MA). Metrics: n, win%, avg return, t-stat, expectancy in R, profit factor, hit5/hit10/hit20 (reachability, **not** P&L), CAGR/maxDD (marks equity only at exits, so understates drawdown).
- **Benchmark:** `IDX_NIFTY_50.csv` if present in `data/nse/`, otherwise `IDX_MKT_PROXY` (equal-weight return of the 200 most liquid stocks, liquidity lagged 1 day).

## How to run (Mac, zsh — use `python3`, then venv)
```bash
cd ~/projects/skills-swing/swing-backtest      # clone of skills @ swing-backtest-harness
source .venv/bin/activate && pip install pandas numpy pyarrow
python -m unittest discover -s tests
python -m swingbt.bhavcopy build-lake --lake /Users/satyieshmacminipro/projects/NseSwingQuant/data/parquet --out-dir data/nse
python run.py --market nse --split 2022-01-01   # results/summary.csv, results/trades.csv
```

## Current state / known facts
- Harness and tests pass (12/12). All numbers seen so far came from **synthetic** data and mean nothing. **No real-data backtest has run yet.**
- Last run on my Mac: `build-lake` printed `wrote 0 symbols` — no stock had ≥300 trading days. Probable cause: the lake holds only a few days (built with `--limit`). Latest commit prints lake diagnostics (days, date range, rows, symbols). **First step: check `find …/data/parquet -name '*.parquet' | wc -l` (want ≥ ~2,000) and rebuild the full lake with `python -m src.cli build` if needed.**
- Bhavcopy is unadjusted. Adjustment factors are inferred from `prev_close_t / close_{t-1}` on consecutive trading days, written to `data/nse/adjustments.csv`. **Not yet verified** against known actions (e.g. RELIANCE bonus 2024). Symbol renames break a history.
- NSE download URLs in `bhavcopy.py` were written from memory and are untested (sandbox could not reach NSE).

## Next steps (in order)
1. Get the full lake built; run `build-lake`; confirm it reports sensible days/symbols.
2. Validate `adjustments.csv` on 5–10 known splits/bonuses/dividends; fix the adjuster if wrong (esp. legacy-format prev_close semantics, pre-2024).
3. Supply a real Nifty 50 / sector-index series (or a symbol→sector map) so the regime filter and S08 use real indices.
4. Run S01–S06, S10; review IS vs OOS, trade counts (want ≥200), t-stats, cost sensitivity (slippage ×2), regime splits. Prefer strategies whose edge survives OOS and 2× costs.
5. Fix survivorship bias: the lake only contains symbols alive in each file, which is mostly point-in-time, but confirm delisted names are present.
6. Add: daily mark-to-market drawdown, walk-forward parameter stability, F&O-universe variant (more liquid, shortable), optional delivery-% feature.
7. Short list 2–3 survivors → paper-trade rules (entry, stop, size, max positions) in a short spec.

## Rules for you (the agent)
- Don't claim performance without real-data output. Quote actual numbers from `results/summary.csv`.
- No lookahead; keep the `NoLookahead` test passing when changing strategies.
- Don't tune parameters on OOS data; if you change parameters, re-split.
- Never commit data files, `.env`, tokens, or secrets. Keep changes small; run `python -m unittest discover -s tests` before every commit.
- If you work in `Nse-Historical-Data`, end the session by updating its `docs/HANDOFF.md`.
