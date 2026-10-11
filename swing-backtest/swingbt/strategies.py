"""The 10 strategies. Each takes (d, ctx) -> Spec | None.

d   : per-ticker DataFrame from indicators.add_features()
ctx : per-ticker context dict (see context.py). Strategies needing data the user has not
      supplied (short interest, insider filings, sector map) return None and are skipped.
Everything here uses only data available at the signal bar's close.
"""
import numpy as np
import pandas as pd

from .engine import Spec
from .indicators import atr, rsi, sh, true_range


def s01_vcp(d, ctx):
    tr = true_range(d)
    comp = tr.rolling(5).mean() / tr.rolling(30).mean()
    breakout = d.Close > d.High.rolling(30).max().shift(1)
    entry = (comp.shift(1) < 0.6) & breakout & (d.rvol >= 1.5) & (d.Close > d.sma50)
    return Spec(entry, d.Close - 2.5 * d.atr, max_hold=10,
                exit_mask=d.Close < d.Low.rolling(5).min().shift(1))


def s02_pead(d, ctx):
    entry = (d.gap >= 0.05) & (d.rvol >= 2) & (d.range_pos >= 0.75)
    ev = ctx.get("eps_event")             # bool Series: earnings reaction window with a strong surprise
    if ev is not None:
        entry &= ev | sh(ev)
    return Spec(entry, d.Low, max_hold=10, target=d.Close * 1.15)


def s03_rsi2(d, ctx):
    r = rsi(d.Close, 2)
    down3 = (d.Close < d.Close.shift(1)).astype(float).rolling(3).sum() == 3
    entry = (d.Close > d.sma200) & (r < 10) & down3
    return Spec(entry, d.Close - 3 * d.atr, max_hold=7, exit_mask=(r > 65) | (d.Close > d.High.shift(1)))


def s04_52wk_high(d, ctx):
    rank = ctx["rs_rank"]
    entry = (d.Close >= d.Close.rolling(252).max()) & (d.rvol >= 1.5) & (rank >= 0.9)
    return Spec(entry, d.Close - 3 * d.atr, max_hold=10, trail_atr=3.0, exit_mask=d.Close < d.ema10)


def s05_gap_pullback(d, ctx):
    ge = (d.gap >= 0.04) & (d.rvol >= 2)
    have = pd.Series(False, index=d.index)
    glow = pd.Series(np.nan, index=d.index)
    gvwap, gvol = glow.copy(), glow.copy()
    for k in range(1, 6):                 # most recent gap day within the last 5 bars (not today)
        m = sh(ge, k)
        new = m & ~have
        glow = glow.where(~new, d.Low.shift(k))
        gvwap = gvwap.where(~new, ((d.High + d.Low + d.Close) / 3).shift(k))
        gvol = gvol.where(~new, d.Volume.shift(k))
        have |= m
    entry = (have & (d.Close > gvwap) & (d.Low > glow) & (d.Low <= d.ema8 * 1.01)
             & (d.Close >= d.ema8) & (d.Volume < gvol) & ((d.Close - glow) / d.Close <= 0.12))
    return Spec(entry, glow, max_hold=10, target=d.Close + 2.5 * (d.Close - glow))


def s06_capitulation(d, ctx):
    ret4 = d.Close / d.Close.shift(4) - 1
    entry = (ret4 <= -0.15) & (d.rvol >= 3) & (d.range_pos >= 0.5)
    return Spec(entry, d.Low * 0.99, max_hold=10, target=d.Close + 0.5 * (d.Close.shift(4) - d.Close),
                slip_mult=1.5)


def s07_short_squeeze(d, ctx):
    si = ctx.get("shortint")              # DataFrame: si_float (%), dtc, forward-filled to d.index
    if si is None:
        return None
    crowded = (si["si_float"] >= 20) & (si["dtc"] >= 4)
    entry = crowded & (d.Close > d.High.rolling(20).max().shift(1)) & (d.rvol >= 2)
    return Spec(entry, d.Close - 2.5 * d.atr, max_hold=10, target=d.Close * 1.20, trail_atr=3.0,
                slip_mult=1.5)


def s08_sector_catchup(d, ctx):
    top, sret = ctx.get("sector_top"), ctx.get("sector_ret20")
    if top is None:
        return None
    ret20 = d.Close / d.Close.shift(20) - 1
    entry = (top & (d.Close > d.sma50) & (ret20 < sret) & (d.Close >= d.sma20 * 0.98)
             & (d.Close <= d.sma20 * 1.02) & (d.Close > d.Close.shift(1)))
    return Spec(entry, d.Close - 2.5 * d.atr, max_hold=10, target=d.Close * 1.12)


def s09_insider_cluster(d, ctx):
    cnt = ctx.get("insider_counts")       # Series: open-market purchases per day, aligned to d.index
    if cnt is None:
        return None
    cluster = cnt.rolling(10).sum() >= 2
    active = cluster.astype(float).rolling(15).max() > 0
    stop = d.Low.rolling(20).min()
    entry = active & (d.Close > d.High.rolling(10).max().shift(1)) & ((d.Close - stop) / d.Close <= 0.15)
    return Spec(entry, stop, max_hold=10, target=d.Close * 1.15)


def s10_ttm_squeeze(d, ctx):
    mid = d.sma20
    sd = d.Close.rolling(20).std()
    bb_up, bb_lo = mid + 2 * sd, mid - 2 * sd
    tr_ma = true_range(d).rolling(20).mean()
    sq = (bb_up < mid + 1.5 * tr_ma) & (bb_lo > mid - 1.5 * tr_ma)
    run6 = sq.astype(float).rolling(6).sum() == 6
    released = sh(run6, 1) | sh(run6, 2) | sh(run6, 3)        # squeezed 6+ bars, ended in the last 3 bars
    mom = d.Close - ((d.High.rolling(20).max() + d.Low.rolling(20).min()) / 2 + mid) / 2
    entry = released & ~sq & (d.Close > bb_up) & (d.Close > d.sma50) & (mom > 0) & (mom > mom.shift(1))
    return Spec(entry, d.Close - 2 * d.atr, max_hold=10, trail_atr=2.0, exit_mask=d.Close < mid)


STRATEGIES = {
    "S01_vcp_breakout": s01_vcp,
    "S02_pead": s02_pead,
    "S03_rsi2_pullback": s03_rsi2,
    "S04_52wk_high": s04_52wk_high,
    "S05_gap_pullback": s05_gap_pullback,
    "S06_capitulation": s06_capitulation,
    "S07_short_squeeze": s07_short_squeeze,
    "S08_sector_catchup": s08_sector_catchup,
    "S09_insider_cluster": s09_insider_cluster,
    "S10_ttm_squeeze": s10_ttm_squeeze,
}
