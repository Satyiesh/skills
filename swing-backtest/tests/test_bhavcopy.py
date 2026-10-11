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
