import numpy as np
import pandas as pd


def sma(s, n):
    return s.rolling(n).mean()


def ema(s, n):
    return s.ewm(span=n, adjust=False).mean()


def true_range(d):
    pc = d.Close.shift(1)
    return pd.concat([d.High - d.Low, (d.High - pc).abs(), (d.Low - pc).abs()], axis=1).max(axis=1)


def atr(d, n=14):
    return true_range(d).ewm(alpha=1 / n, adjust=False, min_periods=n).mean()


def rsi(s, n=2):
    delta = s.diff()
    up = delta.clip(lower=0).ewm(alpha=1 / n, adjust=False, min_periods=n).mean()
    dn = (-delta.clip(upper=0)).ewm(alpha=1 / n, adjust=False, min_periods=n).mean()
    rs = up / dn.replace(0, np.nan)
    out = 100 - 100 / (1 + rs)
    return out.where(dn != 0, 100.0).where(up.notna())


def sh(b, k=1):
    """Shift a boolean series, treating the unknown as False."""
    return b.shift(k).fillna(False).astype(bool)


def add_features(df, atr_min=0.035, min_price=5.0, min_dollar_vol=20e6):
    """Columns shared by every strategy. All of them use data up to and including the row's close."""
    d = df.copy()
    d["atr"] = atr(d, 14)
    d["atr_pct"] = d.atr / d.Close
    for n in (20, 50, 200):
        d[f"sma{n}"] = sma(d.Close, n)
    d["ema8"] = ema(d.Close, 8)
    d["ema10"] = ema(d.Close, 10)
    d["vavg50"] = d.Volume.rolling(50).mean().shift(1)  # prior 50 days, excludes today
    d["rvol"] = d.Volume / d.vavg50
    d["dvol20"] = (d.Close * d.Volume).rolling(20).mean()
    d["gap"] = d.Open / d.Close.shift(1) - 1
    rng = (d.High - d.Low).replace(0, np.nan)
    d["range_pos"] = (d.Close - d.Low) / rng
    d["universe"] = (d.Close > min_price) & (d.dvol20 > min_dollar_vol) & (d.atr_pct >= atr_min)
    return d
