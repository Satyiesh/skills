import unittest

import numpy as np
import pandas as pd

from swingbt.context import ContextBuilder
from swingbt.engine import Cost, Spec, simulate
from swingbt.indicators import add_features
from swingbt.strategies import STRATEGIES
from swingbt.synth import make_panel

ZERO = Cost(0, 0)


def bars(rows):
    idx = pd.bdate_range("2024-01-02", periods=len(rows))
    d = pd.DataFrame(rows, columns=["Open", "High", "Low", "Close"], index=idx)
    d["Volume"] = 1e6
    d["atr"] = 1.0
    return d


def spec(d, stop=95, **kw):
    e = pd.Series(False, index=d.index)
    e.iloc[0] = True
    return Spec(e, pd.Series(stop, index=d.index), **kw)


class EngineRules(unittest.TestCase):
    def test_enters_next_open_and_time_stops(self):
        d = bars([(100, 101, 99, 100)] + [(100, 102, 99, 101)] * 4)
        (t,) = simulate(d, spec(d, max_hold=3), ZERO)
        self.assertEqual(t["entry_date"], d.index[1])
        self.assertEqual((t["reason"], t["days"], t["exit"]), ("time", 3, 101))

    def test_stop_fills_at_stop_intrabar(self):
        d = bars([(100, 101, 99, 100), (100, 101, 99, 100), (99, 100, 94, 96)])
        (t,) = simulate(d, spec(d), ZERO)
        self.assertEqual((t["reason"], t["exit"]), ("stop", 95))

    def test_stop_gapped_through_fills_at_open(self):
        d = bars([(100, 101, 99, 100), (100, 101, 99, 100), (90, 92, 88, 91)])
        (t,) = simulate(d, spec(d), ZERO)
        self.assertEqual(t["exit"], 90)

    def test_target_and_stop_same_bar_is_stop(self):
        d = bars([(100, 101, 99, 100), (100, 101, 99, 100), (100, 120, 90, 100)])
        (t,) = simulate(d, spec(d, target=pd.Series(110.0, index=d.index)), ZERO)
        self.assertEqual(t["reason"], "stop")

    def test_target_gap_up_fills_at_open(self):
        d = bars([(100, 101, 99, 100), (100, 101, 99, 100), (115, 118, 114, 116)])
        (t,) = simulate(d, spec(d, target=pd.Series(110.0, index=d.index)), ZERO)
        self.assertEqual((t["reason"], t["exit"]), ("target", 115))

    def test_close_based_exit_fills_next_open(self):
        d = bars([(100, 101, 99, 100), (100, 101, 99, 100), (100, 101, 99, 100), (103, 104, 102, 103)])
        xm = pd.Series([False, False, True, False], index=d.index)
        (t,) = simulate(d, spec(d, exit_mask=xm), ZERO)
        self.assertEqual((t["reason"], t["exit"]), ("signal", 103))

    def test_costs_reduce_return(self):
        d = bars([(100, 101, 99, 100)] + [(100, 101, 99, 100)] * 3)
        (a,) = simulate(d, spec(d, max_hold=2), ZERO)
        (b,) = simulate(d, spec(d, max_hold=2), Cost(10, 5))
        self.assertLess(b["ret"], a["ret"])

    def test_no_overlapping_trades(self):
        d = bars([(100, 101, 99, 100)] * 10)
        e = pd.Series(True, index=d.index)
        ts = simulate(d, Spec(e, pd.Series(95.0, index=d.index), max_hold=3), ZERO)
        for a, b in zip(ts, ts[1:]):
            self.assertGreater(b["entry_date"], a["exit_date"])


class NoLookahead(unittest.TestCase):
    """Entry flags on a truncated history must equal the flags on full history for the same dates."""

    def test_strategies(self):
        prices, spy, etfs, sectors = make_panel(n_tickers=12, seed=3, n=900)
        cut = 700
        for t in list(prices)[:6]:
            pf, pt = prices[t], prices[t].iloc[: cut + 1]
            cbf = ContextBuilder(prices, spy, etfs, sectors)
            cbt = ContextBuilder({k: v.iloc[: cut + 1] for k, v in prices.items()}, spy.iloc[: cut + 1],
                                 {e: v.iloc[: cut + 1] for e, v in etfs.items()}, sectors)
            ff, ft = add_features(pf, atr_min=0.0), add_features(pt, atr_min=0.0)
            for name, fn in STRATEGIES.items():
                sf, st = fn(ff, cbf.for_ticker(t, ff.index)), fn(ft, cbt.for_ticker(t, ft.index))
                if sf is None:
                    continue
                a = sf.entry.loc[ft.index[-250:]].astype(bool)
                b = st.entry.loc[ft.index[-250:]].astype(bool)
                pd.testing.assert_series_equal(a, b, check_names=False, obj=f"{t} {name}")
                sa, sb = sf.stop.loc[ft.index[-250:]], st.stop.loc[ft.index[-250:]]
                m = a.values
                np.testing.assert_allclose(sa.values[m], sb.values[m], err_msg=f"{t} {name} stop")


if __name__ == "__main__":
    unittest.main()
