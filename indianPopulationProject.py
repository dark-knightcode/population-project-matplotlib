"""
=============================================================
  INDIA POPULATION DATA ANALYSIS — Matplotlib Project
=============================================================
  Datasets:
    - Census of India: https://censusindia.gov.in/census.website/data/population-finder
    - Kaggle (State-wise): https://www.kaggle.com/datasets/imdevskp/india-state-wise-population
    - World Bank: https://data.worldbank.org/indicator/SP.POP.TOTL?locations=IN

  Requirements:
    pip install matplotlib seaborn numpy pandas

  Run:
    python india_population_project.py
=============================================================
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns

# ── Global style ──────────────────────────────────────────
plt.rcParams.update({
    "axes.titlesize":  13,
    "axes.labelsize":  11,
    "axes.grid":       True,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
})

ACCENT = "steelblue"
GREEN  = "mediumseagreen"
CORAL  = "tomato"
PINK   = "palevioletred"
AMBER  = "goldenrod"
PURPLE = "mediumpurple"

# ── Datasets ──────────────────────────────────────────────

states = [
    "Uttar Pradesh", "Maharashtra", "Bihar", "West Bengal",
    "Madhya Pradesh", "Rajasthan", "Tamil Nadu", "Karnataka",
    "Gujarat", "Andhra Pradesh"
]
abbr = ["UP", "MH", "BR", "WB", "MP", "RJ", "TN", "KA", "GJ", "AP"]

population_m   = [199.8, 112.4, 104.1,  91.3,  72.6,  68.6,  72.1,  61.1,  60.4,  84.7]
literacy_pct   = [ 67.7,  82.9,  63.8,  77.1,  70.6,  66.1,  80.1,  75.6,  79.3,  67.4]
urban_pct      = [ 22.3,  45.2,  11.3,  31.9,  27.6,  24.9,  48.4,  38.6,  42.6,  33.5]
density        = [  828,   365,  1106,  1028,   236,   201,   555,   319,   308,   308]
growth_pct     = [ 18.7,  16.0,  25.1,  13.8,  20.3,  21.3,  15.6,  15.7,  19.2,  11.1]
sex_ratio      = [  912,   929,   918,   950,   931,   928,   996,   973,   919,   993]

df = pd.DataFrame({
    "State":       states,
    "Abbr":        abbr,
    "Population":  population_m,
    "Literacy":    literacy_pct,
    "Urban":       urban_pct,
    "Density":     density,
    "Growth":      growth_pct,
    "SexRatio":    sex_ratio,
}).set_index("State")

# Historical data (World Bank)
years      = [1951, 1961, 1971, 1981, 1991, 2001, 2011, 2024]
pop_total  = [0.36, 0.44, 0.55, 0.68, 0.84, 1.03, 1.21, 1.44]   # billions


# ═══════════════════════════════════════════════════════════
#  Figure layout: 3×2 grid
# ═══════════════════════════════════════════════════════════
fig = plt.figure(figsize=(18, 14))
fig.suptitle(
    "India Population Analysis  ·  Census 2011 & World Bank Data",
    fontsize=16, fontweight="bold", color="#e8eaf0", y=0.98
)

gs = fig.add_gridspec(3, 2, hspace=0.45, wspace=0.35)

ax_bar    = fig.add_subplot(gs[0, 0])   # Bar  – state population
ax_line   = fig.add_subplot(gs[0, 1])   # Line – historical growth
ax_heat   = fig.add_subplot(gs[1, :])   # Heatmap (full width)
ax_donut  = fig.add_subplot(gs[2, 0])   # Doughnut – urban/rural
ax_sex    = fig.add_subplot(gs[2, 1])   # Bar – sex ratio


# ── 1. Bar chart: State population ────────────────────────
sorted_df = df.sort_values("Population", ascending=True)
bars = ax_bar.barh(
    sorted_df["Abbr"], sorted_df["Population"],
    color=ACCENT, edgecolor="none", height=0.65
)
for bar, val in zip(bars, sorted_df["Population"]):
    ax_bar.text(
        bar.get_width() + 2, bar.get_y() + bar.get_height() / 2,
        f"{val:.0f}M", va="center", ha="left", fontsize=8, color="#8b8fa8"
    )
ax_bar.set_title("State population (2011 Census)", pad=10)
ax_bar.set_xlabel("Population (millions)")
ax_bar.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x)}M"))
ax_bar.spines[["top", "right"]].set_visible(False)
ax_bar.set_xlim(0, 230)


# ── 2. Line chart: Historical growth ──────────────────────
ax_line.plot(years, pop_total, color=GREEN, linewidth=2.2,
             marker="o", markersize=5, markerfacecolor=GREEN, zorder=3)
ax_line.fill_between(years, pop_total, alpha=0.15, color=GREEN)
for x, y in zip(years, pop_total):
    ax_line.annotate(
        f"{y}B", (x, y), textcoords="offset points",
        xytext=(0, 8), ha="center", fontsize=8, color="#8b8fa8"
    )
ax_line.set_title("Population growth 1951–2024", pad=10)
ax_line.set_ylabel("Population (billions)")
ax_line.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:.2f}B"))
ax_line.spines[["top", "right"]].set_visible(False)


# ── 3. Heatmap ─────────────────────────────────────────────
heat_df = df[["Population", "Literacy", "Urban", "Density", "Growth"]].copy()
heat_df.index = df["Abbr"]

# Min-max normalise each column so colours are comparable
heat_norm = (heat_df - heat_df.min()) / (heat_df.max() - heat_df.min())

col_labels = [
    "Population\n(millions)",
    "Literacy\n(%)",
    "Urban\n(%)",
    "Density\n(per km²)",
    "Decadal\nGrowth (%)",
]

sns.heatmap(
    heat_norm.T,
    ax=ax_heat,
    cmap="Blues",
    linewidths=0.5,
    linecolor="#0f1117",
    annot=heat_df.T,          # raw values as annotations
    fmt=".0f",
    annot_kws={"size": 9, "color": "#e8eaf0"},
    cbar_kws={"label": "Normalised intensity", "shrink": 0.6},
    xticklabels=heat_df.index,
    yticklabels=col_labels,
)
ax_heat.set_title("Heatmap — State-wise demographic indicators (2011)", pad=12)
ax_heat.tick_params(axis="x", labelrotation=0, labelsize=9)
ax_heat.tick_params(axis="y", labelrotation=0, labelsize=9)
cbar = ax_heat.collections[0].colorbar
cbar.ax.yaxis.label.set_color("#c9ccd8")
cbar.ax.tick_params(colors="#8b8fa8")


# ── 4. Doughnut: Urban vs Rural ───────────────────────────
urban_share = 31.2
rural_share = 68.8
wedges, _ = ax_donut.pie(
    [urban_share, rural_share],
    colors=[ACCENT, CORAL],
    startangle=90,
    wedgeprops={"width": 0.55, "edgecolor": "#0f1117", "linewidth": 1.5},
)
ax_donut.text(0, 0.08, f"{urban_share}%", ha="center", va="center",
              fontsize=18, fontweight="bold", color=ACCENT)
ax_donut.text(0, -0.22, "Urban", ha="center", va="center",
              fontsize=10, color="#8b8fa8")
ax_donut.legend(
    wedges, [f"Urban ({urban_share}%)", f"Rural ({rural_share}%)"],
    loc="lower center", bbox_to_anchor=(0.5, -0.12),
    ncol=2, fontsize=9, frameon=False
)
ax_donut.set_title("Urban vs rural population split (2011)", pad=10)


# ── 5. Sex ratio by state ──────────────────────────────────
national_avg = 943
colors_sex = [PINK if v < national_avg else GREEN for v in df["SexRatio"]]
bars2 = ax_sex.bar(
    df["Abbr"], df["SexRatio"],
    color=colors_sex, edgecolor="none", width=0.65
)
ax_sex.axhline(national_avg, color=AMBER, linewidth=1.4,
               linestyle="--", label=f"National avg ({national_avg})")
for bar, val in zip(bars2, df["SexRatio"]):
    ax_sex.text(
        bar.get_x() + bar.get_width() / 2, bar.get_height() + 3,
        str(val), ha="center", va="bottom", fontsize=8, color="#8b8fa8"
    )
ax_sex.set_title("Sex ratio (females per 1000 males, 2011)", pad=10)
ax_sex.set_ylabel("Sex ratio")
ax_sex.set_ylim(870, 1030)
ax_sex.legend(fontsize=9, frameon=True)
ax_sex.spines[["top", "right"]].set_visible(False)

# ── Footnote ──────────────────────────────────────────────
fig.text(
    0.5, 0.005,
    "Sources: Census of India 2011 · World Bank · "
    "kaggle.com/datasets/imdevskp/india-state-wise-population",
    ha="center", fontsize=8, color="#555870"
)

plt.savefig("india_population_analysis.png", dpi=150,
            bbox_inches="tight", facecolor=fig.get_facecolor())
print("Saved -> india_population_analysis.png")
plt.show()

import geopandas as gpd

# Load India map
map_df = gpd.read_file(r"D:\CLASS\JU\indian population heatmap\india_telengana.geojson")

# Fix state name mismatch (VERY IMPORTANT)
# GeoJSON uses slightly different names
state_mapping = {
    "Uttar Pradesh": "Uttar Pradesh",
    "Maharashtra": "Maharashtra",
    "Bihar": "Bihar",
    "West Bengal": "West Bengal",
    "Madhya Pradesh": "Madhya Pradesh",
    "Rajasthan": "Rajasthan",
    "Tamil Nadu": "Tamil Nadu",
    "Karnataka": "Karnataka",
    "Gujarat": "Gujarat",
    "Andhra Pradesh": "Andhra Pradesh"
}

# Convert your dataframe index into column
df_reset = df.reset_index()

# Merge map with your dataset
merged = map_df.merge(df_reset, left_on="NAME_1", right_on="State")

# Plot choropleth map
fig, ax = plt.subplots(1, 1, figsize=(10, 10))

merged.plot(
    column="Population",   # Change this to Literacy / Density / etc
    cmap="OrRd",
    linewidth=0.8,
    ax=ax,
    edgecolor="0.8",
    legend=True
)

ax.set_title("India Population Heatmap (State-wise)", fontsize=14)
ax.axis("off")

plt.show()