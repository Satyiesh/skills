"""NSE bhavcopy -> split/bonus-adjusted per-symbol OHLCV CSVs (the format run.py reads).

  python -m swingbt.bhavcopy download --start 2016-10-01 --raw-dir data/bhav_raw
  python -m swingbt.bhavcopy build    --raw-dir data/bhav_raw --out-dir data/nse
  python run.py --market nse

Raw bhavcopy prices are NOT adjusted for corporate actions. build() reconstructs adjustments from the
exchange's own previous-close field: on an ex-date NSE publishes an adjusted PREVCLOSE, so
ratio = PREVCLOSE_t / CLOSE_{t-1} (consecutive trading days only) is the action factor. Every detected
event is written to adjustments.csv -- eyeball it before trusting results.
Known gaps: symbol renames break a history; a missed day of data around an event hides that event.

URL templates are module constants; NSE has moved these before, so edit them if a download 404s on
a day that was definitely a trading day. They could not be tested from the sandbox this was written in.
"""
import argparse
import datetime as dt
import io
import re
import time
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

UDIFF_URL = "https://nsearchives.nseindia.com/content/cm/BhavCopy_NSE_CM_0_0_0_{ymd}_F_0000.csv.zip"
LEGACY_URL = "https://nsearchives.nseindia.com/content/historical/EQUITIES/{y}/{mon}/cm{dd}{mon}{y}bhav.csv.zip"
INDEX_URL = "https://nsearchives.nseindia.com/content/indices/ind_close_all_{dmy}.csv"
UDIFF_START = dt.date(2024, 7, 8)   # NSE switched the CM bhavcopy to the UDiFF layout around here
HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124 Safari/537.36",
           "Accept": "*/*", "Referer": "https://www.nseindia.com/"}

UDIFF_COLS = {"TckrSymb": "symbol", "SctySrs": "series", "OpnPric": "open", "HghPric": "high",
              "LwPric": "low", "ClsPric": "close", "PrvsClsgPric": "prev_close", "TtlTradgVol": "volume"}
LEGACY_COLS = {"SYMBOL": "symbol", "SERIES": "series", "OPEN": "open", "HIGH": "high", "LOW": "low",
               "CLOSE": "close", "PREVCLOSE": "prev_close", "TOTTRDQTY": "volume"}
NUM = ["open", "high", "low", "close", "prev_close", "volume"]


# ----------------------------------------------------------------------------- download
def _session():
    import requests
    s = requests.Session()
    s.headers.update(HEADERS)
    try:
        s.get("https://www.nseindia.com/", timeout=15)   # cookie warm-up; archives usually don't need it
    except Exception:
        pass
    return s


def _fetch(s, url, tries=4):
    """bytes, or None for 404 (holiday / not published). Raises after repeated failures."""
    for i in range(tries):
        try:
            r = s.get(url, timeout=30)
            if r.status_code == 200 and len(r.content) > 200:
                return r.content
            if r.status_code == 404:
                return None
            err = f"HTTP {r.status_code}"
        except Exception as e:  # network hiccup
            err = repr(e)
        time.sleep(2 ** i)
    raise RuntimeError(f"giving up on {url}: {err}. If this is HTTP 403, NSE is blocking this IP/headers.")


def _cm_urls(d):
    ud = UDIFF_URL.format(ymd=d.strftime("%Y%m%d"))
    lg = LEGACY_URL.format(y=d.year, mon=d.strftime("%b").upper(), dd=d.strftime("%d"))
    return [ud, lg] if d >= UDIFF_START else [lg, ud]


def download(start, end, raw_dir, delay=0.25):
    raw = Path(raw_dir)
    (raw / "cm").mkdir(parents=True, exist_ok=True)
    (raw / "idx").mkdir(parents=True, exist_ok=True)
    s = _session()
    d, end = pd.Timestamp(start).date(), pd.Timestamp(end).date()
    got = {"cm": 0, "idx": 0}
    while d <= end:
        if d.weekday() < 5:
            ymd = d.strftime("%Y%m%d")
            jobs = {"cm": _cm_urls(d), "idx": [INDEX_URL.format(dmy=d.strftime("%d%m%Y"))]}
            for kind, urls in jobs.items():
                f, none = raw / kind / f"{ymd}.bin", raw / kind / f"{ymd}.none"
                if f.exists() or none.exists():
                    continue
                blob = next((b for b in (_fetch(s, u) for u in urls) if b is not None), None)
                if blob is None:
                    none.touch()
                else:
                    f.write_bytes(blob)
                    got[kind] += 1
                time.sleep(delay)
        d += dt.timedelta(days=1)
    print(f"downloaded {got['cm']} equity files, {got['idx']} index files into {raw}")


# ----------------------------------------------------------------------------- parsing
def _csv_bytes(blob):
    if blob[:2] == b"PK":
        z = zipfile.ZipFile(io.BytesIO(blob))
        return z.read(z.namelist()[0])
    return blob


def parse_cm(blob, date):
    df = pd.read_csv(io.BytesIO(_csv_bytes(blob)), skipinitialspace=True)
    df.columns = [c.strip() for c in df.columns]
    cols = UDIFF_COLS if "TckrSymb" in df.columns else LEGACY_COLS
    df = df[list(cols)].rename(columns=cols)
    df["symbol"] = df.symbol.astype(str).str.strip()
    df = df[df.series.astype(str).str.strip() == "EQ"].drop(columns="series")
    for c in NUM:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df = df[(df.close > 0) & (df.open > 0)]
    df.insert(0, "date", pd.Timestamp(date))
    return df


def idx_key(name):
    return "IDX_" + re.sub(r"[^A-Z0-9]+", "_", str(name).upper()).strip("_")


def parse_index(blob, date):
    df = pd.read_csv(io.BytesIO(_csv_bytes(blob)), skipinitialspace=True)
    df.columns = [c.strip().lower() for c in df.columns]
    m = {"index name": "name", "open index value": "open", "high index value": "high",
         "low index value": "low", "closing index value": "close"}
    df = df.rename(columns=m)[list(m.values())]
    for c in ("open", "high", "low", "close"):
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df = df[df.close > 0]
    for c in ("open", "high", "low"):
        df[c] = df[c].fillna(df.close)
    df["key"] = df.name.map(idx_key)
    df.insert(0, "date", pd.Timestamp(date))
    return df


# ----------------------------------------------------------------------------- adjustment
def adjust_symbol(g, day_no, noise=0.001):
    """g: one symbol sorted by date with columns open..volume, prev_close. Returns (adjusted, events)."""
    close, pc = g.close.to_numpy(float), g.prev_close.to_numpy(float)
    consec = np.r_[False, np.diff(day_no[g.index.to_numpy()]) == 1] if len(g) else np.array([], bool)
    f = np.ones(len(g))
    ok = consec & (pc > 0) & np.isfinite(pc)
    ok[0:1] = False
    prev_close_obs = np.r_[np.nan, close[:-1]]
    ratio = np.where(ok, pc / prev_close_obs, 1.0)
    ev = np.abs(ratio - 1) > noise
    f[ev] = ratio[ev]
    mult = np.ones(len(g))                     # product of factors of all LATER bars
    mult[:-1] = np.cumprod(f[::-1])[::-1][1:]
    out = g.copy()
    for c in ("open", "high", "low", "close"):
        out[c] = g[c].to_numpy() * mult
    out["volume"] = g.volume.to_numpy() / mult
    events = g.loc[ev, ["date"]].assign(ratio=ratio[ev])
    return out[["date", "open", "high", "low", "close", "volume"]], events


def _write_adjusted(allp, out, min_rows):
    """allp: long frame [date,symbol,open,high,low,close,prev_close,volume] (unadjusted).
    Writes adjusted per-symbol CSVs, adjustments.csv and the IDX_MKT_PROXY benchmark."""
    out.mkdir(parents=True, exist_ok=True)
    dates = np.sort(allp.date.unique())
    allp = allp.copy()
    allp["day_no"] = np.searchsorted(dates, allp.date.to_numpy())
    allp = allp.sort_values(["symbol", "date"], kind="stable").drop_duplicates(["symbol", "date"], keep="last")
    allp = allp.reset_index(drop=True)
    day_no = allp.day_no.to_numpy()
    n_sym, events, closes, dvol = 0, [], {}, {}
    for sym, g in allp.groupby("symbol", sort=False):
        if len(g) < min_rows:
            continue
        adj, ev = adjust_symbol(g.reset_index(drop=False).set_index("index"), day_no)
        adj = adj.set_index("date")
        adj.to_csv(out / f"{sym}.csv", index_label="Date",
                   header=["Open", "High", "Low", "Close", "Volume"], float_format="%.4f")
        closes[sym], dvol[sym] = adj.close, adj.close * adj.volume
        events.append(ev.assign(symbol=sym))
        n_sym += 1
    ev = pd.concat(events) if events else pd.DataFrame(columns=["date", "ratio", "symbol"])
    ev[["symbol", "date", "ratio"]].to_csv(out / "adjustments.csv", index=False)
    if closes:
        write_market_proxy(pd.DataFrame(closes), pd.DataFrame(dvol), out)
    return n_sym, len(ev)


def write_market_proxy(closes, dvol, out, top_n=200):
    """Benchmark when no index file exists: equal-weight return of the top_n most liquid stocks, where
    liquidity is the PRIOR day's 20d average traded value (no lookahead). Daily returns clipped at +-40%
    so a bad adjustment cannot swing the series. Written as IDX_MKT_PROXY.csv (O=H=L=C)."""
    r = closes.pct_change(fill_method=None).clip(-0.4, 0.4)
    liq = dvol.rolling(20, min_periods=10).mean().shift(1)
    top = liq.rank(axis=1, ascending=False) <= top_n
    m = r.where(top).mean(axis=1).fillna(0.0)
    lvl = 1000 * (1 + m).cumprod()
    pd.DataFrame({"Open": lvl, "High": lvl, "Low": lvl, "Close": lvl, "Volume": 0.0}).to_csv(
        Path(out) / "IDX_MKT_PROXY.csv", index_label="Date")


def build(raw_dir, out_dir, min_rows=300):
    raw, out = Path(raw_dir), Path(out_dir)
    frames = [parse_cm(f.read_bytes(), pd.Timestamp(f.stem)) for f in sorted((raw / "cm").glob("*.bin"))]
    if not frames:
        raise SystemExit(f"no equity files in {raw / 'cm'} -- run `download` first")
    n_sym, n_ev = _write_adjusted(pd.concat(frames, ignore_index=True), out, min_rows)

    ifr = [parse_index(f.read_bytes(), pd.Timestamp(f.stem)) for f in sorted((raw / "idx").glob("*.bin"))]
    n_idx = 0
    if ifr:
        ia = pd.concat(ifr, ignore_index=True)
        for key, g in ia.groupby("key"):
            g = g.drop_duplicates("date").set_index("date").sort_index()
            g.assign(Volume=0.0)[["open", "high", "low", "close", "Volume"]].to_csv(
                out / f"{key}.csv", index_label="Date", header=["Open", "High", "Low", "Close", "Volume"])
            n_idx += 1
    print(f"wrote {n_sym} symbols, {n_idx} indices, {n_ev} corporate-action events -> {out}")


LAKE_COLS = ["date", "symbol", "series", "open", "high", "low", "close", "prev_close", "volume"]


def read_lake(lake_dir, series=("EQ", "BE")):
    """Read NseSwingQuant's parquet lake: <lake>/year=YYYY/month=MM/date=YYYY-MM-DD.parquet with columns
    date,symbol,series,open,high,low,close,prev_close,volume,turnover,isin (unadjusted).
    BZ (trade-to-trade, surveillance) is excluded. If a symbol shows under two series on one day, EQ wins."""
    files = sorted(Path(lake_dir).glob("year=*/month=*/date=*.parquet"))
    if not files:
        raise SystemExit(f"no parquet files under {lake_dir}/year=*/month=*/ -- is this the lake's data/parquet dir?")
    df = pd.concat([pd.read_parquet(f, columns=LAKE_COLS) for f in files], ignore_index=True)
    df["date"] = pd.to_datetime(df["date"])
    df = df[df.series.isin(series)]
    df = df.assign(_eq=(df.series != "EQ")).sort_values(["symbol", "date", "_eq"])
    df = df.drop_duplicates(["symbol", "date"], keep="first").drop(columns=["_eq", "series"])
    for c in ("open", "high", "low", "close", "prev_close", "volume"):
        df[c] = pd.to_numeric(df[c], errors="coerce")
    return df[(df.close > 0) & (df.open > 0)].reset_index(drop=True)


def build_from_lake(lake_dir, out_dir, min_rows=300):
    df = read_lake(lake_dir)
    n_days = df.date.nunique()
    print(f"lake: {n_days} trading days ({df.date.min():%Y-%m-%d} to {df.date.max():%Y-%m-%d}), "
          f"{len(df):,} rows, {df.symbol.nunique()} symbols")
    n_sym, n_ev = _write_adjusted(df, Path(out_dir), min_rows)
    if n_sym == 0:
        raise SystemExit(f"0 symbols have >= {min_rows} trading days of history (the lake has only {n_days} days). "
                         "Rebuild the lake in full (`python -m src.cli build`, not --limit) or lower --min-rows.")
    print(f"wrote {n_sym} symbols, {n_ev} corporate-action events and IDX_MKT_PROXY -> {out_dir}")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    d = sub.add_parser("download")
    d.add_argument("--start", default="2016-10-01")
    d.add_argument("--end", default=dt.date.today().isoformat())
    d.add_argument("--raw-dir", default="data/bhav_raw")
    d.add_argument("--delay", type=float, default=0.25)
    b = sub.add_parser("build")
    b.add_argument("--raw-dir", default="data/bhav_raw")
    b.add_argument("--out-dir", default="data/nse")
    b.add_argument("--min-rows", type=int, default=300)
    L = sub.add_parser("build-lake", help="build from NseSwingQuant's parquet lake instead of raw downloads")
    L.add_argument("--lake", required=True, help="path to NseSwingQuant data/parquet")
    L.add_argument("--out-dir", default="data/nse")
    L.add_argument("--min-rows", type=int, default=300)
    a = ap.parse_args(argv)
    if a.cmd == "build-lake":
        build_from_lake(a.lake, a.out_dir, a.min_rows)
    elif a.cmd == "download":
        download(a.start, a.end, a.raw_dir, a.delay)
    else:
        build(a.raw_dir, a.out_dir, a.min_rows)


if __name__ == "__main__":
    main()
