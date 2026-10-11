"""Price loading. Order: CSV cache in data_dir -> yfinance (if installed) -> error.

CSV schema (one file per ticker, data_dir/TICKER.csv): Date,Open,High,Low,Close,Volume
Prices should be split/dividend ADJUSTED consistently (yfinance auto_adjust=True does this).
For serious work use point-in-time data that includes delisted names (Norgate, Polygon, Sharadar).
"""
from pathlib import Path

import pandas as pd

SECTOR_ETFS = ["XLK", "XLC", "XLY", "XLF", "XLE", "XLV", "XLI", "XLB", "XLU", "XLP", "XLRE"]

# Demo universe: liquid, high-volatility names. NOTE: chosen with hindsight => survivorship bias.
DEFAULT_SECTORS = {
    "NVDA": "XLK", "AMD": "XLK", "AVGO": "XLK", "MU": "XLK", "CRM": "XLK", "PANW": "XLK", "SMCI": "XLK",
    "PLTR": "XLK", "ANET": "XLK", "ON": "XLK",
    "META": "XLC", "NFLX": "XLC", "ROKU": "XLC", "TTD": "XLC",
    "TSLA": "XLY", "AMZN": "XLY", "ABNB": "XLY", "CVNA": "XLY", "RIVN": "XLY", "LULU": "XLY",
    "COIN": "XLF", "HOOD": "XLF", "SOFI": "XLF", "GS": "XLF", "SCHW": "XLF",
    "XOM": "XLE", "OXY": "XLE", "DVN": "XLE", "FANG": "XLE", "HAL": "XLE",
    "MRNA": "XLV", "VRTX": "XLV", "REGN": "XLV", "DXCM": "XLV", "ISRG": "XLV",
    "BA": "XLI", "CAT": "XLI", "UBER": "XLI", "GE": "XLI",
    "FCX": "XLB", "ALB": "XLB", "NUE": "XLB",
    "VST": "XLU", "CEG": "XLU", "NRG": "XLU",
    "ELF": "XLP", "CELH": "XLP",
}


def _read_csv(p):
    df = pd.read_csv(p, parse_dates=["Date"], index_col="Date").sort_index()
    return df[["Open", "High", "Low", "Close", "Volume"]].dropna()


def _yf_download(tickers, start, end):
    try:
        import yfinance as yf
    except ImportError as e:  # pragma: no cover
        raise SystemExit("yfinance not installed and no CSV cache found. `pip install yfinance` "
                         "or place TICKER.csv files in --data-dir.") from e
    raw = yf.download(list(tickers), start=start, end=end, auto_adjust=True, progress=False,
                      group_by="ticker", threads=True)
    out = {}
    for t in tickers:
        try:
            df = raw[t] if len(tickers) > 1 else raw
            df = df[["Open", "High", "Low", "Close", "Volume"]].dropna()
            if len(df):
                df.index.name = "Date"
                out[t] = df
        except KeyError:
            pass
    return out


def load_prices(tickers, data_dir, start, end):
    data_dir = Path(data_dir)
    data_dir.mkdir(parents=True, exist_ok=True)
    out, missing = {}, []
    for t in tickers:
        p = data_dir / f"{t}.csv"
        if p.exists():
            out[t] = _read_csv(p)
        else:
            missing.append(t)
    if missing:
        for t, df in _yf_download(missing, start, end).items():
            df.to_csv(data_dir / f"{t}.csv")
            out[t] = df
    return {t: df.loc[start:end] for t, df in out.items()}
