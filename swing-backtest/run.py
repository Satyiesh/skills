#!/usr/bin/env python3
"""Run the 10 swing strategies with in-sample / out-of-sample split and regime comparison.

  python run.py --synthetic                          # plumbing demo, meaningless numbers
  python run.py --start 2012-01-01 --split 2020-01-01 # downloads via yfinance, caches CSVs in ./data
  python run.py --market nse                          # after: python -m swingbt.bhavcopy download/build
  python run.py --universe my_tickers.txt --sectors sectors.csv --earnings eps.csv
"""
import argparse
import sys
from pathlib import Path

import pandas as pd

from swingbt.context import ContextBuilder, read_optional
from swingbt.bhavcopy import idx_key
from swingbt.data import DEFAULT_SECTORS, SECTOR_ETFS, load_prices, read_ohlcv_csv
from swingbt.engine import Cost, simulate
from swingbt.indicators import add_features
from swingbt.metrics import portfolio, trade_stats
from swingbt.strategies import STRATEGIES


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--universe", help="text file, one ticker per line (default: built-in demo list)")
    ap.add_argument("--sectors", help="csv ticker,etf  (default: built-in map for the demo list)")
    ap.add_argument("--earnings", help="csv ticker,date,surprise_pct")
    ap.add_argument("--shortint", help="csv ticker,date,si_float,dtc")
    ap.add_argument("--insiders", help="csv ticker,date  (Form 4 filing date of open-market buys)")
    ap.add_argument("--eps-min", type=float, default=5.0, help="min EPS surprise %% for S02 when --earnings given")
    ap.add_argument("--market", choices=["us", "nse"], default="us")
    ap.add_argument("--min-price", type=float, default=None, help="universe floor (us 5, nse 50)")
    ap.add_argument("--min-dvol", type=float, default=None, help="20d avg traded value floor (us 2e7 USD, nse 1e8 INR = Rs10cr)")
    ap.add_argument("--data-dir", default=None, help="default: data (us) / data/nse (nse)")
    ap.add_argument("--start", default=None, help="default: 2012-01-01 (us) / 2016-10-01 (nse)")
    ap.add_argument("--end", default=None)
    ap.add_argument("--split", default="2020-01-01", help="OOS starts here")
    ap.add_argument("--strategies", default="all", help="comma list of IDs like S01,S03 or 'all'")
    ap.add_argument("--atr-min", type=float, default=0.035)
    ap.add_argument("--slip-bps", type=float, default=10.0)
    ap.add_argument("--comm-bps", type=float, default=None, help="per side; default us 0, nse 12 (STT+brokerage+GST+stamp+exchange)")
    ap.add_argument("--risk-pct", type=float, default=0.0075)
    ap.add_argument("--max-pos", type=int, default=8)
    ap.add_argument("--no-universe-filter", action="store_true")
    ap.add_argument("--out", default="results")
    ap.add_argument("--synthetic", action="store_true")
    a = ap.parse_args(argv)

    nse = a.market == "nse"
    a.data_dir = a.data_dir or ("data/nse" if nse else "data")
    a.start = a.start or ("2016-10-01" if nse else "2012-01-01")
    a.comm_bps = a.comm_bps if a.comm_bps is not None else (12.0 if nse else 0.0)
    min_price = a.min_price if a.min_price is not None else (50.0 if nse else 5.0)
    min_dvol = a.min_dvol if a.min_dvol is not None else (1e8 if nse else 20e6)

    if a.synthetic:
        from swingbt.synth import make_panel
        prices, spy, etfs, sectors = make_panel()
        print("!! SYNTHETIC DATA: plumbing check only, numbers are meaningless !!", file=sys.stderr)
    elif nse:
        d = Path(a.data_dir)
        if not (d / "IDX_NIFTY_50.csv").exists():
            sys.exit(f"{d}/IDX_NIFTY_50.csv not found -- run: python -m swingbt.bhavcopy download && build")
        trim = lambda df: df.loc[a.start:a.end]
        prices = {p.stem: trim(read_ohlcv_csv(p)) for p in sorted(d.glob("*.csv"))
                  if not p.stem.startswith("IDX_")}
        spy = trim(read_ohlcv_csv(d / "IDX_NIFTY_50.csv"))
        # --sectors csv: symbol,index   (index like "Nifty Bank" or IDX_NIFTY_BANK); S08 is skipped without it
        sectors = {}
        if a.sectors:
            sectors = {str(k).strip(): (v if str(v).startswith("IDX_") else idx_key(v))
                       for k, v in pd.read_csv(a.sectors).values}
        etfs = {k: trim(read_ohlcv_csv(d / f"{k}.csv")) for k in set(sectors.values()) if (d / f"{k}.csv").exists()}
        print(f"NSE: {len(prices)} symbols loaded", file=sys.stderr)
    else:
        sectors = dict(DEFAULT_SECTORS)
        if a.sectors:
            sectors = dict(pd.read_csv(a.sectors).values)
        tickers = [l.strip().upper() for l in open(a.universe) if l.strip()] if a.universe else list(sectors)
        prices = load_prices(tickers, a.data_dir, a.start, a.end)
        spy = load_prices(["SPY"], a.data_dir, a.start, a.end)["SPY"]
        etfs = load_prices(SECTOR_ETFS, a.data_dir, a.start, a.end)

    ctxb = ContextBuilder(prices, spy, etfs, sectors, eps=read_optional(a.earnings),
                          shortint=read_optional(a.shortint), insiders=read_optional(a.insiders),
                          eps_min=a.eps_min)
    want = None if a.strategies == "all" else {s.strip().upper() for s in a.strategies.split(",")}
    chosen = {k: f for k, f in STRATEGIES.items() if want is None or k.split("_")[0] in want}
    cost = Cost(a.slip_bps, a.comm_bps)

    feats = {t: add_features(d, atr_min=a.atr_min, min_price=min_price, min_dollar_vol=min_dvol)
             for t, d in prices.items() if len(d) > 300}
    if not a.no_universe_filter:                  # skip names that never pass the liquidity/volatility screen
        feats = {t: f for t, f in feats.items() if f.universe.any()}
    print(f"{len(feats)} tradable symbols after universe screen", file=sys.stderr)
    all_trades, skipped = [], {}
    for name, fn in chosen.items():
        for t, d in feats.items():
            spec = fn(d, ctxb.for_ticker(t, d.index))
            if spec is None:
                skipped[name] = "missing optional input data"
                break
            if not a.no_universe_filter:
                spec.entry = spec.entry & d.universe
            all_trades += simulate(d, spec, cost, t, name)
    trades = pd.DataFrame(all_trades)
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    if trades.empty:
        print("No trades generated.")
        return
    trades["regime_up"] = ctxb.spy_up.reindex(pd.to_datetime(trades.signal_date)).fillna(False).to_numpy()
    trades.to_csv(out / "trades.csv", index=False)

    split = pd.Timestamp(a.split)
    rows = []
    for name in chosen:
        tn = trades[trades.strategy == name]
        for period, m in (("IS", tn.entry_date < split), ("OOS", tn.entry_date >= split), ("ALL", tn.entry_date.notna())):
            for regime, rm in (("any", True), ("SPY>200d", tn.regime_up)):
                sub = tn[m & rm]
                row = {"strategy": name, "period": period, "regime": regime, **trade_stats(sub)}
                if len(sub) >= 30:
                    row.update(portfolio(sub, risk_pct=a.risk_pct, max_pos=a.max_pos)[0])
                rows.append(row)
    summ = pd.DataFrame(rows)
    summ.to_csv(out / "summary.csv", index=False)
    pd.set_option("display.width", 250, "display.max_columns", 30)
    cols = ["strategy", "period", "regime", "n", "win%", "avg_ret%", "tstat", "exp_R", "PF", "hit5%", "hit10%",
            "avg_days", "CAGR%", "maxDD%"]
    show = summ[(summ.regime == "any") & summ.period.isin(["IS", "OOS"])]
    print(show[[c for c in cols if c in show]].round(2).to_string(index=False))
    for k, v in skipped.items():
        print(f"skipped {k}: {v}")
    print(f"\nwrote {out}/trades.csv and {out}/summary.csv (includes SPY>200d regime rows)")


if __name__ == "__main__":
    main()
