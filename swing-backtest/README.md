# swing-backtest

Backtest harness for 10 swing-trade strategies targeting +5–20% moves in 5–10 trading days.

```bash
pip install -r requirements.txt
python -m unittest discover -s tests          # engine rules + no-lookahead checks
python run.py --synthetic                     # plumbing demo (meaningless numbers)
python run.py --start 2012-01-01 --split 2020-01-01   # yfinance download, CSVs cached in ./data
```

Outputs `results/trades.csv` (every trade) and `results/summary.csv` (strategy × IS/OOS/ALL × regime).

## Strategies and data needs
| ID | Strategy | Extra data |
|---|---|---|
| S01 | VCP / NR breakout | none |
| S02 | PEAD (gap + volume + close strength) | optional `--earnings` (ticker,date,surprise_pct) adds the EPS filter |
| S03 | RSI(2) pullback in uptrend | none |
| S04 | 52-week-high momentum | none (RS rank computed across your universe) |
| S05 | Gap-and-go pullback | none |
| S06 | Capitulation reversal | none (cannot screen out fraud / going-concern — review by hand) |
| S07 | Short squeeze | **required** `--shortint` (ticker,date,si_float,dtc); skipped otherwise |
| S08 | Sector rotation catch-up | sector ETF prices + ticker→ETF map (`--sectors`) |
| S09 | Insider cluster + breakout | **required** `--insiders` (ticker,date = Form 4 *filing* date); skipped otherwise |
| S10 | Bollinger-in-Keltner squeeze release | none |

## Execution assumptions (see `swingbt/engine.py`)
Signal at close of day t → fill at open of t+1 plus slippage (default 10 bps/side; ×1.5 for S06/S07).
Stop wins if stop and target hit in the same bar; gapped-through stops fill at the open.
Close-based exits fill at the next open. One position per ticker. Universe filter on every signal:
price > $5, 20d dollar volume > $20M, ATR(14)/close ≥ 3.5% (`--atr-min`, `--no-universe-filter`).

## Reading the output
* `hit5%/hit10%/hit20%` = share of trades whose intraday high touched +5/10/20% before exit. This is
  *reachability*, not realised P&L — compare with `avg_ret%` and `exp_R`.
* Portfolio columns (CAGR, maxDD) use realised P&L at exits, risk 0.75%/trade, ≤8 positions, no leverage;
  drawdown is understated vs daily mark-to-market. Only shown for ≥30 trades.
* `regime` rows split trades by SPY > 200-day MA at signal time.

## Known limitations
* The built-in universe is hand-picked with hindsight → survivorship bias. Supply a point-in-time universe
  including delisted names for anything you intend to trade.
* yfinance data is adjusted and unaudited; the yfinance download path is untested in this repo's CI (no network).
* Parameters are the first-pass values from the strategy list; no optimisation has been done. Treat IS/OOS gaps,
  trade counts (aim ≥200) and the t-stat before believing any row. Tests only cover price-only strategies for
  lookahead; check S02 (EPS), S07 and S09 inputs are keyed by the date the information was *public*.
