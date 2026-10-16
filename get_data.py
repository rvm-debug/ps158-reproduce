"""Download the Fed's Survey of Consumer Finances summary extracts (1989-2025)
and build a small table of family net worth by parental education: families where
the reference person has a child living at home (KIDS > 0), grouped by the
reference person's education.

Source: https://www.federalreserve.gov/econres/scfindex.htm
The summary extract files ("scfpYYYYexcel.zip") are re-released with each new
survey, so every year is already in 2025 dollars.

Output: data/networth_by_educ.csv (one row per survey year x education group)
"""

import io
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd
import requests

YEARS = list(range(1989, 2026, 3))  # triennial: 1989, 1992, ..., 2025
URL = "https://www.federalreserve.gov/econres/files/scfp{year}excel.zip"

ROOT = Path(__file__).resolve().parent
RAW = ROOT / "data" / "raw"
OUT = ROOT / "data" / "networth_by_educ.csv"

# EDCL: education of the reference person (the SCF has no parents'-education item)
#   1 = no high school diploma, 2 = high school diploma/GED,
#   3 = some college or associate degree, 4 = bachelor's degree or more
GROUPS = {
    "High school or less": [1, 2],
    "Some college": [3],
    "College degree": [4],
}


def download(year):
    """Fetch one year's summary extract CSV into data/raw, skipping if present."""
    path = RAW / f"SCFP{year}.csv"
    if not path.exists():
        print(f"downloading {year} ...")
        resp = requests.get(URL.format(year=year), timeout=120)
        resp.raise_for_status()
        with zipfile.ZipFile(io.BytesIO(resp.content)) as zf:
            (name,) = [n for n in zf.namelist() if n.lower().endswith(".csv")]
            path.write_bytes(zf.read(name))
    return path


def load(year):
    df = pd.read_csv(download(year))
    # Case id is YY1/Y1 in recent files and XX1/X1 in older ones.
    # Each family appears five times (one per imputation); implicate = Y1 - 10*YY1.
    case, row = ("YY1", "Y1") if "YY1" in df else ("XX1", "X1")
    return pd.DataFrame({
        "implicate": df[row] - 10 * df[case],
        "wgt": df["WGT"],
        "edcl": df["EDCL"],
        "networth": df["NETWORTH"],
        "kids": df["KIDS"],
    })


def weighted_median(x, w):
    order = np.argsort(x)
    x, cw = x[order], np.cumsum(w[order])
    return x[np.searchsorted(cw, cw[-1] / 2)]


def summarize(df):
    """Median and mean net worth per group. Medians are computed within each
    implicate and averaged; means use all implicates with the full weights.
    Only families with a child of the reference person at home are kept."""
    df = df[df.kids > 0]
    rows = []
    for group, codes in GROUPS.items():
        g = df[df.edcl.isin(codes)]
        medians = [
            weighted_median(gi.networth.to_numpy(), gi.wgt.to_numpy())
            for _, gi in g.groupby("implicate")
        ]
        rows.append({
            "group": group,
            "median_networth": np.mean(medians),
            "mean_networth": np.average(g.networth, weights=g.wgt),
            "share_of_families": g.wgt.sum() / df.wgt.sum(),
        })
    return rows


def main():
    RAW.mkdir(parents=True, exist_ok=True)
    rows = []
    for year in YEARS:
        for r in summarize(load(year)):
            rows.append({"year": year, **r})
    out = pd.DataFrame(rows)
    out.to_csv(OUT, index=False, float_format="%.4f")
    print(f"wrote {OUT.relative_to(ROOT)} ({len(out)} rows)")


if __name__ == "__main__":
    main()
