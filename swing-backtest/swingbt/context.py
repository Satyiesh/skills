"""Cross-sectional / external context handed to strategies. Everything is as-of the row's date."""
import pandas as pd

from .indicators import sma


def read_optional(path, **kw):
    return pd.read_csv(path, **kw) if path else None


class ContextBuilder:
    """
    prices   : {ticker: raw OHLCV}        (traded universe)
    spy      : OHLCV of SPY
    etfs     : {etf: OHLCV} of sector ETFs
    sectors  : {ticker: etf}
    eps      : DataFrame[ticker, date, surprise_pct]       (optional)  -> S02 filter
    shortint : DataFrame[ticker, date, si_float, dtc]      (optional)  -> S07  (date = publication date!)
    insiders : DataFrame[ticker, date]                     (optional)  -> S09  (date = Form 4 FILING date,
               one row per open-market purchase)
    """

    def __init__(self, prices, spy, etfs, sectors, eps=None, shortint=None, insiders=None, eps_min=5.0):
        self.spy = spy
        self.sectors = sectors
        closes = pd.DataFrame({t: d.Close for t, d in prices.items()})
        self.rs_rank = closes.pct_change(126).rank(axis=1, pct=True)
        self.spy_up = spy.Close > sma(spy.Close, 200)
        if etfs:
            ec = pd.DataFrame({e: d.Close for e, d in etfs.items()})
            self.sret20 = ec.pct_change(20)
            self.stop2 = self.sret20.rank(axis=1, ascending=False) <= 2
        else:
            self.sret20 = self.stop2 = None
        self.eps = self._group(eps, "ticker", lambda g: g[g.surprise_pct >= eps_min])
        self.si = self._group(shortint, "ticker", lambda g: g.set_index("date")[["si_float", "dtc"]])
        self.ins = self._group(insiders, "ticker", lambda g: g.date)

    @staticmethod
    def _group(df, key, fn):
        if df is None:
            return {}
        df = df.copy()
        df["date"] = pd.to_datetime(df["date"])
        return {k: fn(g.sort_values("date")) for k, g in df.groupby(key)}

    def for_ticker(self, t, idx):
        c = {"rs_rank": self.rs_rank[t].reindex(idx) if t in self.rs_rank else pd.Series(float("nan"), idx)}
        etf = self.sectors.get(t)
        if self.sret20 is not None and etf in self.sret20:
            c["sector_top"] = self.stop2[etf].reindex(idx).fillna(False).astype(bool)
            c["sector_ret20"] = self.sret20[etf].reindex(idx)
        if t in self.eps:
            c["eps_event"] = pd.Series(idx.isin(self.eps[t].date), index=idx)
        elif self.eps:
            c["eps_event"] = pd.Series(False, index=idx)
        if t in self.si:
            c["shortint"] = self.si[t].reindex(idx.union(self.si[t].index)).ffill().reindex(idx)
        if t in self.ins:
            c["insider_counts"] = self.ins[t].value_counts().reindex(idx, fill_value=0).astype(float)
        return c
