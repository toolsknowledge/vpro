"""Dashboard of 7 core matplotlib charts, built with subplots on sample data.

Run:  python vibe_graphs.py   -> saves vibe_graphs.png (and opens a window if possible)
"""
import os

import matplotlib

if os.environ.get("MPLBACKEND") is None and not os.environ.get("DISPLAY") and os.uname().sysname != "Darwin":
    matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np

# ---------- sample data (seeded so output is reproducible) ----------
rng = np.random.default_rng(42)

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
sales = np.array([120, 135, 150, 145, 170, 190, 210, 205, 185, 175, 220, 260])
costs = np.array([100, 108, 115, 118, 125, 135, 150, 148, 140, 138, 160, 175])

depts = ["Eng", "Sales", "HR", "Ops", "Design"]
headcount = [42, 30, 8, 18, 12]

exam_scores = rng.normal(loc=68, scale=12, size=300).clip(0, 100)

market_share = {"Web": 45, "Mobile": 30, "Desktop": 15, "Other": 10}

hours = rng.uniform(1, 10, 60)
marks = 45 + 5 * hours + rng.normal(0, 6, 60)

features = ["Age", "Hours", "Marks", "Sleep", "Stress"]
data = np.column_stack([
    rng.normal(25, 4, 100),
])
hours_s = rng.uniform(1, 10, 100)
marks_s = 45 + 5 * hours_s + rng.normal(0, 6, 100)
sleep = 9 - 0.4 * hours_s + rng.normal(0, 0.8, 100)
stress = 2 + 0.5 * hours_s - 0.3 * sleep + rng.normal(0, 0.7, 100)
corr = np.corrcoef(np.vstack([data[:, 0], hours_s, marks_s, sleep, stress]))

groups = {
    "Team A": rng.normal(70, 8, 80),
    "Team B": rng.normal(78, 14, 80),
    "Team C": np.append(rng.normal(65, 6, 78), [105, 20]),  # two outliers
}

# ---------- palette (fixed order, one colour per entity) ----------
C = ["#2a6fdb", "#e0782b", "#2a9d8f", "#8e5bd6", "#c9a227"]
INK, MUTED, GRID = "#1f2937", "#6b7280", "#e5e7eb"

plt.rcParams.update({
    "axes.edgecolor": GRID, "axes.labelcolor": MUTED, "axes.titlecolor": INK,
    "xtick.color": MUTED, "ytick.color": MUTED, "axes.spines.top": False,
    "axes.spines.right": False, "axes.titleweight": "bold", "axes.titlesize": 12,
    "axes.titlelocation": "left", "font.size": 10,
})


def style(ax, ylabel=None, xlabel=None):
    ax.grid(axis="y", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    if ylabel:
        ax.set_ylabel(ylabel)
    if xlabel:
        ax.set_xlabel(xlabel)


fig, axes = plt.subplots(2, 4, figsize=(20, 9.5))
fig.suptitle("Matplotlib Dashboard - 7 Essential Charts", fontsize=18, fontweight="bold",
             color=INK, x=0.01, ha="left")
ax_line, ax_bar, ax_hist, ax_pie, ax_sc, ax_heat, ax_box, ax_note = axes.flat

# 1) LINE - trend over time
ax_line.plot(months, sales, color=C[0], lw=2, marker="o", ms=5, label="Sales")
ax_line.plot(months, costs, color=C[1], lw=2, marker="s", ms=5, label="Costs")
ax_line.fill_between(months, costs, sales, color=C[0], alpha=0.08)
ax_line.set_title("1. Line - trend over time")
style(ax_line, "Amount ($k)")
ax_line.tick_params(axis="x", labelrotation=45)
ax_line.legend(frameon=False)

# 2) BAR - compare categories
bars = ax_bar.bar(depts, headcount, color=C[0], width=0.6)
ax_bar.bar_label(bars, color=INK, padding=2)
ax_bar.set_title("2. Bar - compare categories")
style(ax_bar, "Employees")

# 3) HISTOGRAM - distribution of one variable
ax_hist.hist(exam_scores, bins=15, color=C[2], edgecolor="white")
ax_hist.axvline(exam_scores.mean(), color=INK, ls="--", lw=1.5,
                label=f"mean = {exam_scores.mean():.1f}")
ax_hist.set_title("3. Histogram - distribution")
style(ax_hist, "Students", "Score")
ax_hist.legend(frameon=False)

# 4) PIE - parts of a whole
ax_pie.pie(market_share.values(), labels=market_share.keys(), colors=C[:4],
           autopct="%1.0f%%", startangle=90, counterclock=False,
           wedgeprops={"width": 0.45, "edgecolor": "white", "linewidth": 2},
           textprops={"color": INK})
ax_pie.set_title("4. Pie (donut) - share of whole")

# 5) SCATTER - relationship between 2 variables
ax_sc.scatter(hours, marks, color=C[3], alpha=0.8, edgecolor="white", s=50)
slope, intercept = np.polyfit(hours, marks, 1)
xs = np.linspace(hours.min(), hours.max(), 50)
ax_sc.plot(xs, slope * xs + intercept, color=INK, lw=1.5, label=f"trend (slope {slope:.1f})")
ax_sc.set_title("5. Scatter - relationship")
style(ax_sc, "Marks", "Study hours")
ax_sc.legend(frameon=False)

# 6) HEATMAP - matrix of values (correlation)
im = ax_heat.imshow(corr, cmap="RdBu_r", vmin=-1, vmax=1)
ax_heat.set_xticks(range(len(features)), features, rotation=45, ha="right")
ax_heat.set_yticks(range(len(features)), features)
for i in range(len(features)):
    for j in range(len(features)):
        ax_heat.text(j, i, f"{corr[i, j]:.2f}", ha="center", va="center", fontsize=8,
                     color="white" if abs(corr[i, j]) > 0.6 else INK)
ax_heat.set_title("6. Heatmap - correlation")
ax_heat.spines[:].set_visible(False)
fig.colorbar(im, ax=ax_heat, fraction=0.046, pad=0.04)

# 7) BOX PLOT - spread, median, outliers
bp = ax_box.boxplot(list(groups.values()), tick_labels=list(groups.keys()), patch_artist=True,
                    medianprops={"color": INK, "linewidth": 2},
                    flierprops={"marker": "o", "markerfacecolor": C[1], "markeredgecolor": "white"})
for patch, color in zip(bp["boxes"], C):
    patch.set(facecolor=color, alpha=0.7, edgecolor=color)
ax_box.set_title("7. Box plot - spread & outliers")
style(ax_box, "Performance score")

# Cheat sheet panel
ax_note.axis("off")
ax_note.text(0, 1, "When to use what\n", fontsize=13, fontweight="bold", color=INK, va="top")
ax_note.text(0, 0.9, (
    "Line      trend over time\n\n"
    "Bar       compare categories\n\n"
    "Histogram shape of one variable\n\n"
    "Pie       parts of a whole (few slices)\n\n"
    "Scatter   relationship of two variables\n\n"
    "Heatmap   many-by-many matrix of values\n\n"
    "Box plot  median, quartiles, outliers"
), fontsize=10.5, color=INK, va="top", family="monospace")

fig.tight_layout(rect=(0, 0, 1, 0.96))

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "vibe_graphs.png")
    fig.savefig(out, dpi=110)
    print(f"saved {out}")
    plt.show()
