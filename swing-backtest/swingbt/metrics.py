import numpy as np
import pandas as pd


def trade_stats(t):
    if len(t) == 0:
        return {"n": 0}
    w, l = t.ret[t.ret > 0], t.ret[t.ret <= 0]
    n = len(t)
    se = t.ret.std(ddof=1) / np.sqrt(n) if n > 1 else np.nan
    return {
        "n": n,
        "win%": 100 * (t.ret > 0).mean(),
        "avg_ret%": 100 * t.ret.mean(),
        "med_ret%": 100 * t.ret.median(),
        "tstat": t.ret.mean() / se if se and se > 0 else np.nan,
        "exp_R": t.R.mean(),
        "PF": w.sum() / -l.sum() if l.sum() < 0 else np.inf,
        "avg_win%": 100 * w.mean() if len(w) else 0.0,
        "avg_loss%": 100 * l.mean() if len(l) else 0.0,
        "hit5%": 100 * t.hit5.mean(),
        "hit10%": 100 * t.hit10.mean(),
        "hit20%": 100 * t.hit20.mean(),
        "avg_days": t.days.mean(),
        "stop%": 100 * (t.reason == "stop").mean(),
    }


def portfolio(trades, equity0=100_000.0, risk_pct=0.0075, max_pos=8, max_pos_pct=0.20, seed=7):
    """Realised-P&L portfolio: risk_pct of equity per trade, no leverage, max concurrent positions.
    Equity is marked only at exits, so drawdown is understated vs. a daily mark-to-market."""
    if len(trades) == 0:
        return {}, pd.Series(dtype=float)
    t = trades.sample(frac=1, random_state=seed).sort_values("entry_date", kind="stable")
    equity, open_pos, curve, taken = equity0, [], {}, 0

    def realise(upto):
        nonlocal equity
        for p in sorted([p for p in open_pos if p[0] <= upto], key=lambda p: p[0]):
            equity += p[2]
            curve[p[0]] = equity
            open_pos.remove(p)

    for r in t.itertuples():
        realise(r.entry_date)
        if len(open_pos) >= max_pos:
            continue
        exposure = sum(p[1] for p in open_pos)
        size = min(equity * risk_pct / r.risk, equity * max_pos_pct, equity - exposure)
        if size <= 0:
            continue
        open_pos.append((r.exit_date, size, size * r.ret))
        taken += 1
    realise(pd.Timestamp.max)
    eq = pd.Series(curve).sort_index()
    eq = eq[~eq.index.duplicated(keep="last")]
    if len(eq) < 2:
        return {"trades_taken": taken}, eq
    daily = eq.resample("D").last().ffill()
    yrs = (daily.index[-1] - daily.index[0]).days / 365.25
    rets = daily.pct_change().dropna()
    dd = (daily / daily.cummax() - 1).min()
    cagr = (daily.iloc[-1] / equity0) ** (1 / yrs) - 1 if yrs > 0 else np.nan
    return {
        "trades_taken": taken,
        "CAGR%": 100 * cagr,
        "maxDD%": 100 * dd,
        "calmar": cagr / -dd if dd < 0 else np.nan,
        "sharpe": rets.mean() / rets.std() * np.sqrt(365) if rets.std() > 0 else np.nan,
    }, eq
