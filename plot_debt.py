"""Bonus figure, in academic journal style: debt of families with children at home,
by parental education, 1989-2025 (SCF, 2025 dollars).

Three panels: (a) share holding any debt, (b) median debt and (c) mean debt among
families holding debt, the convention of the Fed's SCF debt tables (Table 13).

Reads data/parents_by_educ.csv (run get_data.py first).
Writes figures/debt_by_educ.pdf (vector, for submission) and figures/debt_by_educ.png.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import FuncFormatter

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "parents_by_educ.csv"
OUT = ROOT / "figures" / "debt_by_educ"

# Grayscale with redundant line style and marker, so the figure survives
# black-and-white printing.
SERIES = {
    "College degree": dict(label="Bachelor's degree or more", color="black", linestyle="-",
                           marker="o", markerfacecolor="black"),
    "High school or less": dict(label="High school or less", color="0.45", linestyle="--",
                                marker="s", markerfacecolor="white"),
}
PANELS = [
    ("share_with_debt", 100, "(a) Families with any debt", "Percent"),
    ("median_debt", 1e-3, "(b) Median debt, families with debt", "Thousands of 2025 dollars"),
    ("mean_debt", 1e-3, "(c) Mean debt, families with debt", "Thousands of 2025 dollars"),
]

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "Times", "DejaVu Serif"],
    "mathtext.fontset": "stix",
    "font.size": 9,
    "axes.linewidth": 0.6,
    "xtick.direction": "in",
    "ytick.direction": "in",
    "xtick.major.width": 0.6,
    "ytick.major.width": 0.6,
    "pdf.fonttype": 42,  # embed TrueType fonts, as most journals require
})


def main():
    df = pd.read_csv(DATA)
    fig, axes = plt.subplots(1, 3, figsize=(7.0, 2.6))

    for ax, (column, scale, title, ylabel) in zip(axes, PANELS):
        wide = df.pivot(index="year", columns="group", values=column) * scale
        for group, style in SERIES.items():
            ax.plot(wide.index, wide[group], linewidth=1.0, markersize=3.5,
                    markeredgewidth=0.7, markeredgecolor=style["color"],
                    **{k: v for k, v in style.items() if k != "label"}, label=style["label"])
        ax.set_title(title, fontsize=9, loc="left")
        ax.set_ylabel(ylabel)
        ax.set_xticks([1989, 1998, 2007, 2016, 2025])
        ax.set_xlim(1987, 2027)
        ax.set_ylim(0, 100 if column == "share_with_debt" else wide.max().max() * 1.1)
        ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:,.0f}"))
        for side in ("top", "right"):
            ax.spines[side].set_visible(False)

    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=2, frameon=False,
               bbox_to_anchor=(0.5, 0.0))
    fig.tight_layout(rect=(0, 0.08, 1, 1), w_pad=1.5)

    OUT.parent.mkdir(exist_ok=True)
    for ext in ("pdf", "png"):
        fig.savefig(OUT.with_suffix(f".{ext}"), dpi=300)
        print(f"wrote {OUT.with_suffix(f'.{ext}').relative_to(ROOT)}")


if __name__ == "__main__":
    main()
