import io
import tempfile
import unittest
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

from swingbt import bhavcopy as bc

LEG = "SYMBOL,SERIES,OPEN,HIGH,LOW,CLOSE,LAST,PREVCLOSE,TOTTRDQTY,TOTTRDVAL,TIMESTAMP,TOTALTRADES,ISIN,\n"
UD = ("TradDt,BizDt,Sgmt,Src,FinInstrmTp,FinInstrmId,ISIN,TckrSymb,SctySrs,XpryDt,FininstrmActlXpryDt,StrkPric,"
      "OptnTp,FinInstrmNm,OpnPric,HghPric,LwPric,ClsPric,LastPric,PrvsClsgPric,UndrlygPric,SttlmPric,OpnIntrst,"
      "ChngInOpnIntrst,TtlTradgVol,TtlTrfVal,TtlNbOfTxsExctd,SsnId,NewBrdLotQty,Rmks,Rsvd1,Rsvd2,Rsvd3,Rsvd4\n")


def legacy(rows):
    s = LEG
    for sym, ser, o, h, l, c, pc, v in rows:
        s += f"{sym},{ser},{o},{h},{l},{c},{c},{pc},{v},0,01-JAN-2020,1,INE000,\n"
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        z.writestr("x.csv", s)
    return buf.getvalue()


def udiff(rows):
    s = UD
    for sym, ser, o, h, l, c, pc, v in rows:
        s += f"2025-01-01,2025-01-01,CM,NSE,STK,1,INE000,{sym},{ser},,,,,N,{o},{h},{l},{c},{c},{pc},,{c},,,{v},0,1,F1,1,,,,,\n"
    return s.encode()   # plain csv also accepted


class Bhav(unittest.TestCase):
    def test_parse_both_layouts_filters_series(self):
        rows = [("AAA", "EQ", 10, 11, 9, 10.5, 10, 100), ("BBB", "BE", 5, 5, 5, 5, 5, 1)]
        for blob in (legacy(rows), udiff(rows)):
            df = bc.parse_cm(blob, "2025-01-01")
            self.assertEqual(list(df.symbol), ["AAA"])
            self.assertEqual(df.close.iloc[0], 10.5)

    def test_split_adjustment_makes_series_continuous(self):
        with tempfile.TemporaryDirectory() as tmp:
            raw = Path(tmp) / "raw"
            (raw / "cm").mkdir(parents=True)
            days = pd.bdate_range("2023-01-02", periods=320)
            px, prev = 1000.0, None
            for i, d in enumerate(days):
                if i == 200:                       # 1:2 split on day 200: price halves, prevclose is adjusted
                    prev_adj = px / 2
                    px = px / 2
                else:
                    prev_adj = prev if prev else px
                new = px * (1.01 if i % 2 else 0.995)
                rows = [("AAA", "EQ", px, max(px, new), min(px, new), new, prev_adj, 1000),
                        ("FILL", "EQ", 50, 51, 49, 50, 50, 1000)]
                (raw / "cm" / f"{d:%Y%m%d}.bin").write_bytes(legacy(rows) if i % 2 else udiff(rows))
                prev, px = new, new
            out = Path(tmp) / "out"
            bc.build(raw, out)
            a = pd.read_csv(out / "AAA.csv", index_col="Date", parse_dates=True)
            jump = (a.Close / a.Close.shift(1) - 1).abs().max()
            self.assertLess(jump, 0.02, "split should be adjusted away")
            ev = pd.read_csv(out / "adjustments.csv")
            self.assertEqual(len(ev[ev.symbol == "AAA"]), 1)
            self.assertAlmostEqual(ev[ev.symbol == "AAA"].ratio.iloc[0], 0.5, delta=0.01)
            self.assertAlmostEqual(a.Volume.iloc[0], 1000 * 2, delta=1)   # pre-split volume doubled


if __name__ == "__main__":
    unittest.main()


class Lake(unittest.TestCase):
    def test_lake_to_adjusted_csv_and_proxy(self):
        with tempfile.TemporaryDirectory() as tmp:
            lake = Path(tmp) / "parquet"
            days = pd.bdate_range("2023-01-02", periods=330)
            px = {"AAA": 1000.0, "BBB": 50.0, "CCC": 80.0}
            prev = dict(px)
            rng = np.random.default_rng(0)
            for i, d in enumerate(days):
                rows = []
                for s in px:
                    pc = prev[s]
                    if s == "AAA" and i == 200:      # 1:2 split; NSE publishes the adjusted prev close
                        pc, px[s] = pc / 2, px[s] / 2
                    new = px[s] * (1 + rng.normal(0, 0.01))
                    rows.append(dict(date=d.date(), symbol=s, series="EQ", open=px[s], high=max(px[s], new) * 1.01,
                                     low=min(px[s], new) * 0.99, close=new, prev_close=pc, volume=1000,
                                     turnover=0.0, isin="X"))
                    prev[s], px[s] = new, new
                rows.append(dict(date=d.date(), symbol="JUNK", series="BZ", open=1.0, high=1.0, low=1.0, close=1.0,
                                 prev_close=1.0, volume=1, turnover=0.0, isin="Y"))
                out = lake / f"year={d.year}" / f"month={d.month:02d}"
                out.mkdir(parents=True, exist_ok=True)
                pd.DataFrame(rows).to_parquet(out / f"date={d.date()}.parquet")
            o = Path(tmp) / "nse"
            bc.build_from_lake(lake, o)
            self.assertFalse((o / "JUNK.csv").exists(), "BZ series must be excluded")
            a = pd.read_csv(o / "AAA.csv", index_col="Date", parse_dates=True)
            self.assertLess((a.Close / a.Close.shift(1) - 1).abs().max(), 0.06)
            ev = pd.read_csv(o / "adjustments.csv")
            self.assertEqual(list(ev.symbol), ["AAA"])
            m = pd.read_csv(o / "IDX_MKT_PROXY.csv", index_col="Date")
            self.assertEqual(len(m), 330)
            self.assertTrue((m.Close > 0).all())
