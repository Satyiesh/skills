"""Trade simulator. One position per ticker at a time.

Timing rules (no lookahead):
  * signal is evaluated at the close of day t, entry fills at the OPEN of day t+1 (+ slippage)
  * stop / target are checked intrabar from the entry bar on; stop wins if both hit in one bar
  * a stop that is gapped through fills at the open (worse price), not at the stop
  * close-based exits (exit_mask, trailing) are decided at the close and fill at the NEXT open
  * time stop exits at the close of the last allowed bar
"""
from dataclasses import dataclass

import numpy as np
import pandas as pd

HIT_LEVELS = (0.05, 0.10, 0.20)


@dataclass
class Spec:
    entry: pd.Series                      # bool, evaluated at close of signal day
    stop: pd.Series                       # initial stop price known at the signal close
    max_hold: int = 10                    # trading days including the entry bar
    target: pd.Series | None = None       # target price known at the signal close
    exit_mask: pd.Series | None = None    # bool at close -> exit next open
    trail_atr: float | None = None        # chandelier: highest close since entry - k * ATR(signal)
    slip_mult: float = 1.0                # >1 for gap / panic entries


@dataclass
class Cost:
    slip_bps: float = 10.0                # per side
    comm_bps: float = 0.0                 # per side


def _arr(s, d, dtype=float):
    return s.reindex(d.index).to_numpy(dtype=dtype)


def simulate(d, spec, cost, ticker="", strategy=""):
    O, H, L, C = (d[c].to_numpy(float) for c in ("Open", "High", "Low", "Close"))
    atr = d["atr"].to_numpy(float)
    n = len(d)
    ent = spec.entry.reindex(d.index).fillna(False).to_numpy(bool)
    stop_s = _arr(spec.stop, d)
    tgt_s = _arr(spec.target, d) if spec.target is not None else None
    xm = spec.exit_mask.reindex(d.index).fillna(False).to_numpy(bool) if spec.exit_mask is not None else None
    slip = cost.slip_bps * 1e-4 * spec.slip_mult
    comm = cost.comm_bps * 1e-4
    dates = d.index
    trades, next_free = [], 0

    for t in np.flatnonzero(ent):
        e = t + 1
        if e >= n or e < next_free:
            continue
        s0 = stop_s[t]
        px = O[e]
        if not (np.isfinite(s0) and np.isfinite(px)) or px <= s0 or px > C[t] * 1.15:
            continue                      # gapped through the stop, or an absurd gap: no trade
        fill = px * (1 + slip)
        tg = tgt_s[t] if tgt_s is not None else np.nan
        if np.isfinite(tg) and tg <= fill:
            continue
        trail = spec.trail_atr * atr[t] if spec.trail_atr else None
        if trail is not None and not np.isfinite(trail):
            continue

        stop, hc, mfe_hi, mae_lo = s0, fill, fill, fill
        last = min(n - 1, e + spec.max_hold - 1)
        pending, exit_px, reason, j = False, None, "", e
        for j in range(e, last + 1):
            if pending:
                exit_px, reason = O[j], "signal"
                break
            mae_lo = min(mae_lo, L[j])
            if L[j] <= stop:
                exit_px, reason = min(O[j], stop), "stop"
                break
            mfe_hi = max(mfe_hi, H[j])
            if np.isfinite(tg) and H[j] >= tg:
                exit_px, reason = max(O[j], tg), "target"
                break
            hc = max(hc, C[j])
            if trail is not None:
                stop = max(stop, hc - trail)
            if j == last:
                exit_px, reason = C[j], ("time" if j == e + spec.max_hold - 1 else "eod")
                break
            if xm is not None and xm[j]:
                pending = True

        entry_net = fill * (1 + comm)
        exit_net = exit_px * (1 - slip) * (1 - comm)
        ret = exit_net / entry_net - 1
        risk = (fill - s0) / fill
        mfe = mfe_hi / fill - 1
        row = dict(strategy=strategy, ticker=ticker, signal_date=dates[t], entry_date=dates[e],
                   exit_date=dates[j], entry=fill, exit=exit_px, ret=ret, risk=risk,
                   R=ret / risk if risk > 0 else np.nan, days=j - e + 1, reason=reason,
                   mfe=mfe, mae=mae_lo / fill - 1)
        for lv in HIT_LEVELS:
            row[f"hit{int(lv * 100)}"] = mfe >= lv
        trades.append(row)
        next_free = j + 1
    return trades
