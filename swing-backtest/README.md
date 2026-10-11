# swing-backtest

Backtest harness for 10 swing-trade strategies targeting +5–20% moves in 5–10 trading days.

```bash
pip install -r requirements.txt
python -m unittest discover -s tests          # engine rules + no-lookahead checks
python run.py --synthetic                     # plumbing demo (meaningless numbers)
python run.py --start 2012-01-01 --split 2020-01-01   # yfinance download, CSVs cached in ./data
```

Outputs `results/trades.csv` (every trade) and `results/summary.csv` (strategy × IS/OOS/ALL × regime).

## Indian market (NSE bhavcopy, ~10 years)
```bash
python -m swingbt.bhavcopy download --start 2016-10-01     # ~2,500 daily files, resumable, ~0.25s polite delay
python -m swingbt.bhavcopy build                           # -> data/nse/*.csv (adjusted) + adjustments.csv
python run.py --market nse --split 2022-01-01 [--sectors sectors.csv]
```
* Raw bhavcopy is **unadjusted**. `build` derives split/bonus factors from NSE's own PREVCLOSE and writes every
  detected event to `data/nse/adjustments.csv`; spot-check a few known splits before trusting results.
* Universe floors default to price > Rs50 and 20d traded value > Rs10 crore; costs default to 12 bps/side
  (STT, brokerage, GST, stamp, exchange fees) plus 10 bps slippage. Override with `--min-price/--min-dvol/--comm-bps`.
* Benchmark/regime = Nifty 50 (index bhavcopy). S08 needs `--sectors` (`symbol,index`, e.g. `INFY,Nifty IT`).
  S07 (no short-interest series in India) and S09 are skipped; S02 runs in price-only mode.
* Long-only. NSE circuit limits can make stops un-fillable on gap-downs; the engine fills gapped stops at the open,
  which understates that risk for circuit-locked names.
* The download URLs were written from memory of NSE's archive layout and could not be tested from the sandbox
  (NSE is blocked there). If a day fails, adjust the URL constants at the top of `swingbt/bhavcopy.py`.

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
