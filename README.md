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
  skipping any already there, and writes `data/parents_by_educ.csv`: one row
  per year and education group, with median and mean net worth, the group's share
  of parent families, and the debt measures described below.
- `plot.py` reads that CSV and writes both net worth figures to `figures/`.

## Bonus: debt

**Figure:** `figures/debt_by_educ.pdf` (vector, fonts embedded, for
submission) and `figures/debt_by_educ.png`, in grayscale journal style. Three
panels compare parents with a bachelor's degree or more to parents with a high
school education or less, 1989–2025: (a) the share of families with any debt,
(b) median debt and (c) mean debt among families with debt, in 2025 dollars.

In 2025, 91% of college-educated parent families and 80% of
high-school-or-less parent families had debt. Among those with debt, median
debt was $270K vs. $34K and mean debt was $350K vs. $108K.

**Data:** the same SCF summary extracts and parent families as above. Debt is
total family debt (`DEBT`): mortgages and home equity lines, other real estate
loans, other lines of credit, credit card balances, installment loans
(student, vehicle and other) and other debt. Following the Fed's debt tables
(Table 13), medians and means are for families holding any debt (`DEBT > 0`). This reproduces the Fed's
published share, median and mean by education and by family structure in
every survey year, 1989–2025.

**Reading the median:** for high-school-or-less parents, the median falls
right at the line between families with mortgages and families without. It
halves from $67K (2022) to $34K (2025) because the share of debtors with
home-secured debt slipped from 51% to 45%. The mean is steadier.

**Rerunning:** after setting up the environment as above,

```bash
.venv/bin/python get_data.py
.venv/bin/python plot_debt.py
```

`get_data.py` adds the columns `share_with_debt`, `median_debt` and
`mean_debt` to `data/parents_by_educ.csv`; `plot_debt.py` reads them and
writes both debt figure files.
