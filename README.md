# 🎬 Netflix Content Analysis

> An end-to-end exploratory data analysis of Netflix's global catalog — uncovering trends in content type, geography, genres, ratings, and growth over time.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
![pandas](https://img.shields.io/badge/pandas-2.0%2B-150458?logo=pandas)
![matplotlib](https://img.shields.io/badge/matplotlib-3.7%2B-11557c)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-complete-brightgreen)

---

## 📌 Project Overview

This project performs a comprehensive exploratory data analysis (EDA) on the **Netflix Titles dataset** — a real-world dataset of 8,807 movies and TV shows available on Netflix as of mid-2021. The analysis covers data cleaning, missing-value auditing, and 10 distinct visualisations styled in Netflix's signature dark theme.

**Dataset source:** [Kaggle — Netflix Movies and TV Shows](https://www.kaggle.com/datasets/shivamb/netflix-shows)

---

## 📁 Project Structure

```
netflix-analysis/
│
├── data/
│   └── netflix_titles.csv          # Raw dataset (8,807 rows × 12 columns)
│
├── notebooks/
│   └── netflix_analysis.ipynb      # Full interactive analysis notebook
│
├── src/
│   └── analysis.py                 # Core module — loading, cleaning, all plot functions
│
├── outputs/                        # All generated chart PNGs (auto-created on run)
│   ├── 01_content_split.png
│   ├── 02_titles_added_yearly.png
│   ├── 03_top_countries.png
│   ├── 04_ratings.png
│   ├── 05_top_genres.png
│   ├── 06_release_year_trend.png
│   ├── 07_movie_duration.png
│   ├── 08_tv_seasons.png
│   ├── 09_monthly_additions.png
│   └── 10_top_directors.png
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🔍 Dataset at a Glance

| Property | Value |
|---|---|
| Total titles | 8,807 |
| Movies | 6,131 (69.6%) |
| TV Shows | 2,676 (30.4%) |
| Release year range | 1925 – 2021 |
| Countries represented | 190+ |
| Columns | 12 |

**Columns:** `show_id`, `type`, `title`, `director`, `cast`, `country`, `date_added`, `release_year`, `rating`, `duration`, `listed_in`, `description`

---

## 📊 Analysis Sections

### 1. Content Type Split
Movies account for nearly 70% of the Netflix catalog — TV shows are a significant but minority offering.

### 2. Growth Over Time
Netflix's catalog grew explosively from 2015 to 2019 (peak: ~2,000 titles added in 2019), before slowing in 2020–2021, likely reflecting COVID-19 production disruptions.

### 3. Top Content-Producing Countries
The United States leads with 2,818 titles — nearly 3× second-place India (972). South Korea, Japan, and Spain also feature prominently, reflecting Netflix's international content strategy.

### 4. Ratings Distribution
Over 70% of content is rated for mature audiences (TV-MA, TV-14, R). Children's content (TV-Y, TV-G, PG) makes up less than 10% of the catalog.

### 5. Genre Landscape
*International Movies* is the single largest genre tag, illustrating Netflix's deliberate global expansion. Dramas, Comedies, and Action & Adventure round out the top four.

### 6. Release Year Trend
Content production accelerated sharply from 2015, peaking at 1,147 titles in 2018 for films and 1,032 for TV. Post-2019 shows a plateau.

### 7. Movie Duration
The average movie on Netflix runs ~100 minutes (mean: 99.6 min, median: 98 min). Distribution is roughly normal with a right tail of extended features up to 312 minutes.

### 8. TV Show Seasons
67% of TV shows on Netflix have only one season — suggesting a mix of mini-series, cancelled shows, and limited series. Only 8% run beyond 3 seasons.

### 9. Monthly Additions
Content additions peak in Q4 (October–January), consistent with holiday viewing demand. July and August see the lowest addition rates.

### 10. Top Directors
Rajiv Chilaka leads with 19 titles (children's animation). Raúl Campos & Jan Suter follow at 18. Martin Scorsese (12) and Steven Spielberg (11) are the most prominent mainstream directors.

---

## 🚨 Data Quality Notes

| Column | Missing | % | Notes |
|---|---|---|---|
| `director` | 2,634 | 29.9% | Expected — TV shows rarely have a single director |
| `country` | 831 | 9.4% | Co-productions and original content |
| `cast` | 825 | 9.4% | Some titles have no credited cast in dataset |
| `date_added` | 10 | 0.1% | Negligible |
| `rating` | 4 | <0.1% | 3 rows contain duration values — data entry error |
| `title`, `type`, `description` | 0 | 0% | ✅ Complete |

---

## 💡 Key Insights

1. **Movies dominate** the catalog at nearly 70%, but Netflix has steadily grown its TV show library.
2. **2019 was peak Netflix growth** — nearly 2,000 titles added in one year. Post-2020 slowdown is notable.
3. **The US alone accounts for 32% of all content** by country; India is a distant second at 11%.
4. **Netflix skews heavily toward adult content** — TV-MA is the single most common rating.
5. **Most TV shows don't survive beyond Season 1** — 67% are single-season, suggesting aggressive cancellation or intentional limited-series commissioning.
6. **International content is a strategic priority** — "International Movies" is the #1 genre tag in the entire catalog.
7. **Average movie length is ~100 minutes** — consistent with theatrical norms, even for streaming-first titles.
8. **Monthly additions peak in Q4** — likely timed to subscriber acquisition drives during the holiday season.

---

## ⚙️ Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/netflix-analysis.git
cd netflix-analysis
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the full analysis (generates all plots)

```bash
python src/analysis.py
```

### 4. Or open the Jupyter notebook

```bash
jupyter notebook notebooks/netflix_analysis.ipynb
```

All charts are saved automatically to `outputs/`.

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| `pandas` | Data loading, cleaning, aggregation |
| `numpy` | Numerical operations |
| `matplotlib` | All visualisations |
| `seaborn` | Supplementary styling |
| `jupyter` | Interactive notebook environment |

---

## 📄 License

This project is released under the [MIT License](LICENSE).  
The Netflix Titles dataset is sourced from [Kaggle](https://www.kaggle.com/datasets/shivamb/netflix-shows) and is publicly available for educational use.

---

## 🙋 Author

**Your Name**  
[GitHub](https://github.com/YOUR_USERNAME) · [LinkedIn](https://linkedin.com/in/YOUR_PROFILE)

> *Built as a data analysis portfolio project. Feedback and contributions welcome.*
