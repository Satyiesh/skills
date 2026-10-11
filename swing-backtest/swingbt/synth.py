"""Synthetic OHLCV for plumbing tests ONLY. No edge is injected: results on this data mean nothing."""
import numpy as np
import pandas as pd


def make_ohlcv(seed, n=2600, start="2014-01-02", vol=0.022, price0=50.0):
    rng = np.random.default_rng(seed)
    idx = pd.bdate_range(start, periods=n)
    h = np.empty(n)
    h[0] = vol
    for i in range(1, n):                       # persistent volatility regimes
        h[i] = 0.97 * h[i - 1] + 0.03 * vol + 0.0003 * abs(rng.standard_normal())
    r = rng.standard_normal(n) * h + 0.0003
    gap = np.zeros(n)
    ev = np.arange(40, n, 63) + rng.integers(0, 5, len(range(40, n, 63)))
    gap[ev] = rng.standard_normal(len(ev)) * 0.06  # earnings-like gaps
    close = price0 * np.exp(np.cumsum(r + gap))
    prev = np.r_[price0, close[:-1]]
    open_ = prev * np.exp(gap + rng.standard_normal(n) * h * 0.3)
    hi = np.maximum(open_, close) * (1 + np.abs(rng.standard_normal(n)) * h * 0.5)
    lo = np.minimum(open_, close) * (1 - np.abs(rng.standard_normal(n)) * h * 0.5)
    volu = 4e6 * np.exp(rng.standard_normal(n) * 0.35) * (1 + 6 * np.abs(gap) / 0.06 * 0.3 + 40 * np.abs(r))
    return pd.DataFrame({"Open": open_, "High": hi, "Low": lo, "Close": close, "Volume": volu}, index=idx)


def make_panel(n_tickers=30, seed=0, n=2600):
    from .data import DEFAULT_SECTORS, SECTOR_ETFS
    tick = list(DEFAULT_SECTORS)[:n_tickers]
    prices = {t: make_ohlcv(seed * 1000 + i, n=n, vol=0.018 + 0.012 * (i % 4) / 3) for i, t in enumerate(tick)}
    spy = make_ohlcv(seed * 1000 + 999, n=n, vol=0.008, price0=200)
    etfs = {e: make_ohlcv(seed * 1000 + 500 + i, n=n, vol=0.009, price0=80) for i, e in enumerate(SECTOR_ETFS)}
    return prices, spy, etfs, {t: DEFAULT_SECTORS[t] for t in tick}
