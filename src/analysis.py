"""
Netflix Dataset — Core Analysis Module
======================================
Loads, cleans, and analyses netflix_titles.csv.
Run directly or import functions into a notebook.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import warnings
import os

warnings.filterwarnings("ignore")

# ── Paths ────────────────────────────────────────────────────────────────────
ROOT     = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT, "data")
OUT_DIR  = os.path.join(ROOT, "outputs")
os.makedirs(OUT_DIR, exist_ok=True)

DATA_PATH = os.path.join(DATA_DIR, "netflix_titles.csv")

# ── Style ────────────────────────────────────────────────────────────────────
NETFLIX_RED  = "#E50914"
NETFLIX_DARK = "#141414"
PALETTE      = ["#E50914", "#B20710", "#564d4d", "#8a8a8a", "#c5c5c5",
                "#f5f5f1", "#db0000", "#831010", "#3d3d3d", "#6e6e6e"]

plt.rcParams.update({
    "figure.facecolor":  NETFLIX_DARK,
    "axes.facecolor":    "#1f1f1f",
    "axes.edgecolor":    "#3a3a3a",
    "axes.labelcolor":   "#f5f5f1",
    "xtick.color":       "#8a8a8a",
    "ytick.color":       "#8a8a8a",
    "text.color":        "#f5f5f1",
    "grid.color":        "#2e2e2e",
    "grid.linestyle":    "--",
    "font.family":       "DejaVu Sans",
    "axes.titlesize":    13,
    "axes.labelsize":    11,
})


# ── Data loading & cleaning ───────────────────────────────────────────────────
def load_data(path: str = DATA_PATH) -> pd.DataFrame:
    """Load and clean the Netflix titles CSV."""
    df = pd.read_csv(path)

    # Parse dates
    df["date_added"]   = pd.to_datetime(df["date_added"].str.strip(), errors="coerce")
    df["year_added"]   = df["date_added"].dt.year
    df["month_added"]  = df["date_added"].dt.month

    # Duration
    movies = df["type"] == "Movie"
    df.loc[movies,  "duration_int"] = (
        df.loc[movies,  "duration"].str.replace(" min", "", regex=False).astype(float)
    )
    df.loc[~movies, "duration_int"] = (
        df.loc[~movies, "duration"].str.replace(r" Season.*", "", regex=True).astype(float)
    )

    # Exploded genres (stored separately to avoid row explosion on main df)
    df["genres"] = df["listed_in"].str.split(", ")

    return df


def missing_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Return a tidy missing-value summary."""
    miss  = df.isnull().sum()
    pct   = (miss / len(df) * 100).round(2)
    return pd.DataFrame({"missing": miss, "pct": pct}).query("missing > 0").sort_values("missing", ascending=False)


# ── Individual plot functions ─────────────────────────────────────────────────
def plot_content_split(df: pd.DataFrame, save: bool = True):
    counts = df["type"].value_counts()
    fig, ax = plt.subplots(figsize=(5, 5))
    fig.patch.set_facecolor(NETFLIX_DARK)
    wedges, texts, autotexts = ax.pie(
        counts,
        labels=counts.index,
        autopct="%1.1f%%",
        colors=[NETFLIX_RED, "#564d4d"],
        startangle=90,
        wedgeprops={"edgecolor": NETFLIX_DARK, "linewidth": 2},
        textprops={"color": "#f5f5f1", "fontsize": 12},
    )
    for at in autotexts:
        at.set_fontsize(11)
    ax.set_title("Movies vs TV Shows", fontsize=14, color="#f5f5f1", pad=15)
    plt.tight_layout()
    _save(fig, "01_content_split.png", save)


def plot_titles_added_yearly(df: pd.DataFrame, save: bool = True):
    yearly = df.groupby("year_added").size().loc[2015:2021]
    fig, ax = plt.subplots(figsize=(9, 4))
    bars = ax.bar(yearly.index.astype(int), yearly.values, color=NETFLIX_RED, width=0.6, zorder=3)
    ax.bar_label(bars, fmt="%d", color="#f5f5f1", fontsize=10, padding=4)
    ax.set_title("Titles added to Netflix per year", fontsize=14)
    ax.set_xlabel("Year")
    ax.set_ylabel("Number of titles")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
    ax.grid(axis="y", zorder=0)
    ax.set_axisbelow(True)
    plt.tight_layout()
    _save(fig, "02_titles_added_yearly.png", save)


def plot_top_countries(df: pd.DataFrame, n: int = 10, save: bool = True):
    top = df["country"].value_counts().head(n)
    fig, ax = plt.subplots(figsize=(9, 4))
    bars = ax.barh(top.index[::-1], top.values[::-1], color=PALETTE[:n][::-1], zorder=3)
    ax.bar_label(bars, fmt="%d", color="#f5f5f1", fontsize=9, padding=4)
    ax.set_title(f"Top {n} content-producing countries", fontsize=14)
    ax.set_xlabel("Number of titles")
    ax.grid(axis="x", zorder=0)
    ax.set_axisbelow(True)
    plt.tight_layout()
    _save(fig, "03_top_countries.png", save)


def plot_ratings(df: pd.DataFrame, save: bool = True):
    valid_ratings = ["TV-MA", "TV-14", "TV-PG", "R", "PG-13", "TV-Y7", "TV-Y", "PG", "TV-G", "NR", "G"]
    counts = df[df["rating"].isin(valid_ratings)]["rating"].value_counts()
    fig, ax = plt.subplots(figsize=(9, 4))
    bars = ax.bar(counts.index, counts.values, color=NETFLIX_RED, zorder=3)
    ax.bar_label(bars, fmt="%d", color="#f5f5f1", fontsize=9, padding=4)
    ax.set_title("Content rating distribution", fontsize=14)
    ax.set_ylabel("Number of titles")
    ax.grid(axis="y", zorder=0)
    ax.set_axisbelow(True)
    plt.tight_layout()
    _save(fig, "04_ratings.png", save)


def plot_genres(df: pd.DataFrame, n: int = 12, save: bool = True):
    genres = df["genres"].explode().value_counts().head(n)
    fig, ax = plt.subplots(figsize=(9, 5))
    bars = ax.barh(genres.index[::-1], genres.values[::-1], color=NETFLIX_RED, zorder=3)
    ax.bar_label(bars, fmt="%d", color="#f5f5f1", fontsize=9, padding=4)
    ax.set_title(f"Top {n} genres on Netflix", fontsize=14)
    ax.set_xlabel("Number of titles")
    ax.grid(axis="x", zorder=0)
    ax.set_axisbelow(True)
    plt.tight_layout()
    _save(fig, "05_top_genres.png", save)


def plot_release_year_trend(df: pd.DataFrame, save: bool = True):
    trend = df.groupby("release_year").size().loc[2000:2021]
    fig, ax = plt.subplots(figsize=(11, 4))
    ax.fill_between(trend.index, trend.values, alpha=0.25, color=NETFLIX_RED)
    ax.plot(trend.index, trend.values, color=NETFLIX_RED, linewidth=2.5, marker="o", markersize=4)
    ax.set_title("Netflix titles by release year (2000–2021)", fontsize=14)
    ax.set_xlabel("Release year")
    ax.set_ylabel("Number of titles")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
    ax.grid(axis="y", zorder=0)
    plt.tight_layout()
    _save(fig, "06_release_year_trend.png", save)


def plot_movie_duration(df: pd.DataFrame, save: bool = True):
    movies = df[df["type"] == "Movie"]["duration_int"].dropna()
    fig, ax = plt.subplots(figsize=(9, 4))
    ax.hist(movies, bins=40, color=NETFLIX_RED, edgecolor=NETFLIX_DARK, linewidth=0.4, zorder=3)
    ax.axvline(movies.mean(),  color="#f5f5f1", linestyle="--", linewidth=1.5, label=f"Mean: {movies.mean():.0f} min")
    ax.axvline(movies.median(), color="#8a8a8a", linestyle=":",  linewidth=1.5, label=f"Median: {movies.median():.0f} min")
    ax.set_title("Movie duration distribution", fontsize=14)
    ax.set_xlabel("Duration (minutes)")
    ax.set_ylabel("Count")
    ax.legend(fontsize=10)
    ax.grid(axis="y", zorder=0)
    plt.tight_layout()
    _save(fig, "07_movie_duration.png", save)


def plot_tv_seasons(df: pd.DataFrame, save: bool = True):
    tv = df[df["type"] == "TV Show"]["duration_int"].dropna()
    counts = tv.value_counts().sort_index().head(10)
    fig, ax = plt.subplots(figsize=(8, 4))
    bars = ax.bar(counts.index.astype(int), counts.values, color=NETFLIX_RED, zorder=3)
    ax.bar_label(bars, fmt="%d", color="#f5f5f1", fontsize=9, padding=4)
    ax.set_title("TV show season count distribution", fontsize=14)
    ax.set_xlabel("Number of seasons")
    ax.set_ylabel("Number of shows")
    ax.set_xticks(counts.index.astype(int))
    ax.grid(axis="y", zorder=0)
    plt.tight_layout()
    _save(fig, "08_tv_seasons.png", save)


def plot_monthly_additions(df: pd.DataFrame, save: bool = True):
    month_map = {1:"Jan",2:"Feb",3:"Mar",4:"Apr",5:"May",6:"Jun",
                 7:"Jul",8:"Aug",9:"Sep",10:"Oct",11:"Nov",12:"Dec"}
    monthly = df["month_added"].value_counts().sort_index()
    monthly.index = [month_map[m] for m in monthly.index]
    fig, ax = plt.subplots(figsize=(9, 4))
    bars = ax.bar(monthly.index, monthly.values, color=NETFLIX_RED, zorder=3)
    ax.bar_label(bars, fmt="%d", color="#f5f5f1", fontsize=9, padding=4)
    ax.set_title("Titles added by month (all years)", fontsize=14)
    ax.set_ylabel("Number of titles")
    ax.grid(axis="y", zorder=0)
    plt.tight_layout()
    _save(fig, "09_monthly_additions.png", save)


def plot_top_directors(df: pd.DataFrame, n: int = 10, save: bool = True):
    top = df.dropna(subset=["director"])["director"].value_counts().head(n)
    fig, ax = plt.subplots(figsize=(9, 4))
    bars = ax.barh(top.index[::-1], top.values[::-1], color=NETFLIX_RED, zorder=3)
    ax.bar_label(bars, fmt="%d", color="#f5f5f1", fontsize=9, padding=4)
    ax.set_title(f"Top {n} directors on Netflix", fontsize=14)
    ax.set_xlabel("Number of titles")
    ax.grid(axis="x", zorder=0)
    plt.tight_layout()
    _save(fig, "10_top_directors.png", save)


# ── Helper ────────────────────────────────────────────────────────────────────
def _save(fig, filename: str, save: bool):
    if save:
        path = os.path.join(OUT_DIR, filename)
        fig.savefig(path, dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
        print(f"  saved → {path}")
    plt.show()
    plt.close(fig)


# ── Run all ───────────────────────────────────────────────────────────────────
def run_all():
    print("Loading data …")
    df = load_data()
    print(f"  {len(df):,} rows | {df.shape[1]} columns\n")

    print("Missing values:")
    print(missing_summary(df).to_string())
    print()

    plots = [
        plot_content_split,
        plot_titles_added_yearly,
        plot_top_countries,
        plot_ratings,
        plot_genres,
        plot_release_year_trend,
        plot_movie_duration,
        plot_tv_seasons,
        plot_monthly_additions,
        plot_top_directors,
    ]

    print("Generating plots …")
    for fn in plots:
        print(f"  → {fn.__name__}")
        fn(df, save=True)

    print("\nAll done! Check the outputs/ folder.")


if __name__ == "__main__":
    run_all()
