# BTech Campus Placement — Beginner EDA Project

A first **Exploratory Data Analysis (EDA)** project for **2nd-year BTech AIML** students (written with campuses like **SRM** in mind).

You will study a simple question that already matters to you:

> *What is associated with getting placed after BTech, and how did that look over the last five years?*

Python is kept basic: `pandas`, `numpy`, `matplotlib`, and `seaborn`. No machine learning.

---

## What is in this repository

| Path | Purpose |
| --- | --- |
| [docs/PROJECT_IDEAS.md](docs/PROJECT_IDEAS.md) | More EDA ideas + **how to get data without wasting time** |
| [docs/NOTEBOOK_GUIDE.md](docs/NOTEBOOK_GUIDE.md) | Stage-by-stage explanation of the notebook |
| [notebooks/campus_placement_eda.ipynb](notebooks/campus_placement_eda.ipynb) | The EDA notebook (run this) |
| [data/campus_placement_btech.csv](data/campus_placement_btech.csv) | Ready-to-use dataset |
| [data/DATA_DICTIONARY.md](data/DATA_DICTIONARY.md) | Meaning of every column |
| [requirements.txt](requirements.txt) | Python packages |
| [scripts/generate_dataset.py](scripts/generate_dataset.py) | Rebuilds the CSV (optional) |

---

## 1. Project ideas (short list)

Full write-up: [docs/PROJECT_IDEAS.md](docs/PROJECT_IDEAS.md)

1. **Campus placement (this repo)** — best first project; data is already here.
2. **MBA campus recruitment** — tiny public CSV on GitHub (215 rows).
3. **AMEO / AMCAT engineering salaries** — skills vs first job.
4. **Student exam scores** — study hours vs marks.
5. **Stack Overflow survey** — languages used in real jobs.
6. **AISHE on data.gov.in** — Indian higher-education counts.

---

## 2. Gathering data (do not spend a week on this)

The placement CSV is **already in this folder**. Start analysing.

If you pick another idea, use a **direct CSV link** or a government / UCI / Kaggle download. Do not scrape websites. Details and copy-paste URLs are in [docs/PROJECT_IDEAS.md](docs/PROJECT_IDEAS.md).

---

## 3. How to run the notebook

```bash
pip install -r requirements.txt
jupyter notebook
```

Open `notebooks/campus_placement_eda.ipynb` and run cells from top to bottom (`Shift+Enter`).

The notebook is split into stages:

1. Import Python libraries  
2. Import data and examine the dataset  
3. Clean the data  
4. Univariate analysis (one column at a time)  
5. Bivariate analysis (what relates to placement)  
6. Five-year trends and a bigger picture  
7. Insights and takeaways for a 2nd-year student  

What each stage is doing: [docs/NOTEBOOK_GUIDE.md](docs/NOTEBOOK_GUIDE.md)

---

## About the dataset

Educational / synthetic BTech records for **2021–2025** (about 1,500 students).  
It is **not** official SRM or NIRF data. It is designed so that:

- the story feels like a real Indian engineering campus, and
- the file is slightly messy (missing values, duplicate rows, mixed labels) so you can practise cleaning.

---

## Licence / classroom use

Use freely for teaching and student assignments. If you later switch to a Kaggle or UCI file, cite that source in your report.
