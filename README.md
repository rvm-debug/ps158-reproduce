# The college wealth gap, 1989–2025

Net worth of U.S. families with children at home, comparing parents with a
bachelor's degree or more to parents with a high school education or less.
Data come from the Federal Reserve's Survey of Consumer Finances (SCF), every
survey from 1989 through 2025.

## Figures

| File | What it shows |
|---|---|
| `figures/networth_gap.png` | **Mean** net worth by parental education (top) and the college ÷ high-school-or-less ratio (bottom) |
| `figures/networth_gap_median.png` | The same figure using **median** net worth |

In 2025 the mean college-educated parent family had $2,291K and the mean
high-school-or-less parent family had $269K (8.5×). The medians were $626K and
$72K (8.7×). In 1989 the ratios were 4.7× (means) and 5.9× (medians).

## Data

- **Source:** SCF summary extract public data, one file per survey
  (`scfpYYYYexcel.zip`), from the
  [Federal Reserve](https://www.federalreserve.gov/econres/scfindex.htm).
  The Fed re-releases every year's file in the latest survey's dollars, so all
  values are in **2025 dollars**.
- **Families:** only families where the reference person has a child living at
  home (`KIDS > 0`, the same as the Fed's "with child(ren)" groups).
- **Parental education:** the reference person's education (`EDCL`).
  "High school or less" = no diploma or a diploma/GED (`EDCL` 1–2).
  "College degree" = a bachelor's degree or more (`EDCL` 4).
- **Method:** the SCF stores each family five times (multiple imputation).
  Means and medians are weighted (`WGT`) and pool all five copies, which is the
  Fed's own convention. This reproduces the published means and medians by
  education in the Fed's 2025 historical tables (Table 4) exactly.

## Rerunning

Requires Python 3. From this folder:

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python get_data.py
.venv/bin/python plot.py
```

- `get_data.py` downloads the 13 survey files (about 340 MB) into `data/raw/`,
  skipping any already there, and writes `data/networth_by_educ.csv`: one row
  per year and education group, with the median, the mean and the group's share
  of parent families.
- `plot.py` reads that CSV and writes both figures to `figures/`.
