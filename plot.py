"""First figure: the wealth gap between college-educated families and families
with a high school education or less, among families with children at home,
1989-2025 (SCF, 2025 dollars), drawn once with means and once with medians.

Reads data/networth_by_educ.csv (run get_data.py first).
Writes figures/networth_gap.png (mean) and figures/networth_gap_median.png.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import FuncFormatter, MultipleLocator

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "networth_by_educ.csv"
# statistic -> (CSV column, output file, footnote on how it is computed)
STATS = {
    "mean": ("mean_networth", ROOT / "figures" / "networth_gap.png",
             "Means use all five implicates."),
    "median": ("median_networth", ROOT / "figures" / "networth_gap_median.png",
               "Medians pool all five implicates, as in the Fed's tables."),
}

SURFACE = "#fcfcfb"
INK = "#0b0b0b"
INK_2 = "#52514e"
GRID = "#e4e3df"
COLORS = {"College degree": "#2a78d6", "High school or less": "#eb6834"}


def style(ax):
    ax.set_facecolor(SURFACE)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color(INK_2)
    ax.grid(axis="y", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    ax.tick_params(colors=INK_2, length=0, labelsize=9)


def draw(df, stat):
    column, out, method = STATS[stat]
    wide = df.pivot(index="year", columns="group", values=column) / 1e3
    ratio = wide["College degree"] / wide["High school or less"]
    years = wide.index

    fig, (top, bottom) = plt.subplots(
        2, 1, figsize=(8, 7), sharex=True, height_ratios=[3, 2], facecolor=SURFACE
    )

    # Panel 1: net worth by group, direct-labeled at the right end
    for group, color in COLORS.items():
        top.plot(years, wide[group], color=color, linewidth=2, marker="o", markersize=5,
                 markeredgecolor=SURFACE, markeredgewidth=1.5, label=group)
        top.annotate(f"{group}\n${wide[group].iloc[-1]:,.0f}k", (years[-1], wide[group].iloc[-1]),
                     xytext=(8, 0), textcoords="offset points", va="center", fontsize=9, color=INK)
    style(top)
    top.set_ylim(0, None)
    top.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"${v:,.0f}k"))
    top.set_title(f"{stat.capitalize()} family net worth, by parental education (2025 dollars)",
                  loc="left", fontsize=10, color=INK_2)
    top.legend(loc="upper left", frameon=False, fontsize=9, labelcolor=INK)

    # Panel 2: the gap as a ratio (separate chart, not a second y-axis)
    bottom.plot(years, ratio, color=INK, linewidth=2, marker="o", markersize=5,
                markeredgecolor=SURFACE, markeredgewidth=1.5)
    for y in (years[0], years[-1]):
        bottom.annotate(f"{ratio[y]:.1f}×", (y, ratio[y]), xytext=(0, 9),
                        textcoords="offset points", ha="center", fontsize=9, color=INK)
    style(bottom)
    bottom.set_ylim(0, ratio.max() * 1.2)
    bottom.yaxis.set_major_locator(MultipleLocator(2))
    bottom.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:.0f}×"))
    bottom.set_title(f"Ratio: college-degree {stat} ÷ high-school-or-less {stat}",
                     loc="left", fontsize=10, color=INK_2)
    bottom.set_xticks(years)
    bottom.set_xlim(years[0] - 1, years[-1] + 5)  # room for end labels

    fig.suptitle("The college wealth gap, 1989–2025", x=0.06, ha="left",
                 fontsize=14, fontweight="bold", color=INK)
    fig.text(0.06, 0.01,
             "Source: Federal Reserve Survey of Consumer Finances, summary extract public data. "
             f"{method}\n"
             "\"High school or less\" = no diploma or HS diploma/GED; \"College degree\" = bachelor's or more.\n"
             "Families where the reference person has a child living at home; education is the reference person's.",
             fontsize=7.5, color=INK_2, va="bottom")
    fig.tight_layout(rect=(0.03, 0.07, 1, 0.97))

    out.parent.mkdir(exist_ok=True)
    fig.savefig(out, dpi=200, facecolor=SURFACE)
    plt.close(fig)
    print(f"wrote {out.relative_to(ROOT)}")


def main():
    df = pd.read_csv(DATA)
    for stat in STATS:
        draw(df, stat)


if __name__ == "__main__":
    main()
