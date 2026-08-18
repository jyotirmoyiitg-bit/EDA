"""Build the beginner campus-placement EDA notebook."""

from __future__ import annotations

from pathlib import Path

import nbformat as nbf

OUT = Path(__file__).resolve().parents[1] / "notebooks" / "campus_placement_eda.ipynb"

nb = nbf.v4.new_notebook()
nb["metadata"] = {
    "kernelspec": {
        "display_name": "Python 3",
        "language": "python",
        "name": "python3",
    },
    "language_info": {"name": "python", "pygments_lexer": "ipython3"},
}

cells = []


def md(text: str) -> None:
    cells.append(nbf.v4.new_markdown_cell(text.strip() + "\n"))


def code(text: str) -> None:
    cells.append(nbf.v4.new_code_cell(text.strip() + "\n"))


md(
    """
# Campus Placement EDA for BTech Students

**Who this is for:** 2nd-year BTech **AIML** students (for example at SRM) who are starting data analysis with Python.

**Question we will study:**

> What is associated with getting a campus placement, and how did that look over the last five graduating years (2021–2025)?

**Why this problem?**
You already know CGPA, internships, backlogs, and placement talks. EDA is how we check those stories with a table and a few charts — before anyone builds a machine-learning model.

**How to use this notebook**
1. Run the cells **in order** (Stage 1 → Stage 7) using `Shift+Enter`.
2. Read the short note above each code cell.
3. Try the extra questions at the end.

The CSV is already in this project: `data/campus_placement_btech.csv`.  
It is a **teaching dataset** (synthetic). It is not official SRM / company data, but the patterns are realistic enough to learn from.

A full written explanation of every stage is in `docs/NOTEBOOK_GUIDE.md`.
"""
)

md(
    """
---
# Stage 1 — Import Python libraries

We only need four libraries:

| Library | Role |
| --- | --- |
| **pandas** | Load the CSV and work with tables |
| **numpy** | Simple numeric helpers (for example filling missing numbers) |
| **matplotlib** | Draw graphs |
| **seaborn** | Slightly nicer statistical graphs |

If this cell gives `ModuleNotFoundError`, run `pip install -r requirements.txt` in a terminal and restart the kernel.
"""
)

code(
    """
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

sns.set_theme(style="whitegrid")
plt.rcParams["figure.figsize"] = (8, 4.5)
plt.rcParams["axes.titlesize"] = 12
plt.rcParams["axes.labelsize"] = 11

print("Libraries imported successfully.")
print("pandas version:", pd.__version__)
print("seaborn version:", sns.__version__)
"""
)

md(
    """
---
# Stage 2 — Import data and examine the dataset

First we **load** the file, then we **look** at it. We do not clean or plot yet.

Good habit: never trust a CSV until you have seen its size, column names, a few rows, missing values, and odd category labels.
"""
)

code(
    """
# Works whether you opened Jupyter from the notebooks/ folder or the project root
candidates = [
    Path("../data/campus_placement_btech.csv"),
    Path("data/campus_placement_btech.csv"),
]
data_path = next(path for path in candidates if path.exists())
print("Reading:", data_path.resolve())

df = pd.read_csv(data_path)
print("Done. The table is stored in a variable called df.")
"""
)

md(
    """
### 2.1 Size, first rows, last rows

- `shape` → (number of rows, number of columns)
- `head()` → first 5 students
- `tail()` → last 5 students
"""
)

code(
    """
print("Rows, columns:", df.shape)
print()
print("Column names:")
print(list(df.columns))
print()
print("First 5 rows:")
df.head()
"""
)

code(
    """
print("Last 5 rows:")
df.tail()
"""
)

md(
    """
### 2.2 Column types and missing-value counts

`info()` tells you whether a column is text (`object`) or a number (`int64` / `float64`), and how many values are non-null.
"""
)

code(
    """
df.info()
"""
)

md(
    """
### 2.3 Numeric summary

`describe()` gives count, mean, min, max, and quartiles for numeric columns. This is a quick way to spot impossible values (for example a CGPA of 11).
"""
)

code(
    """
df.describe()
"""
)

md(
    """
### 2.4 Look at category labels (this is where mess hides)

In a clean file, `branch` should have 7 labels and `placement_status` should have 2. Let us check the raw file.
"""
)

code(
    """
print("placement_status labels:")
print(df["placement_status"].value_counts(dropna=False))
print()
print("branch labels:")
print(df["branch"].value_counts(dropna=False))
print()
print("coding_skill labels:")
print(df["coding_skill"].value_counts(dropna=False))
"""
)

md(
    """
### 2.5 Missing values and duplicate rows

- Missing values: cells pandas could not read as a real value (`NaN`).
- Duplicates: the same row twice (a data-entry accident).
"""
)

code(
    """
print("Missing values in each column:")
print(df.isna().sum())
print()
print("Duplicate rows:", df.duplicated().sum())
print("Unique student_id values:", df["student_id"].nunique())
"""
)

md(
    """
**What Stage 2 should have shown you**

1. About **1,508 rows** and **16 columns** (a few extra rows are duplicates).
2. `placement_status` is inconsistent: `Placed`, `placed`, `Not Placed`, `not placed`, `NotPlaced`.
3. `branch` has extra spaces and mixed case (`CSE  `, `aiml`).
4. Some internships / skills are missing.
5. `company_type` and `job_role` look missing for many students. In the CSV those cells were written as `NA` (not placed). pandas treats the text `NA` as missing by default. We will label them properly in Stage 3.

If you skip cleaning, a chart would treat `CSE` and `cse` as two different branches. That would be wrong.
"""
)

md(
    """
---
# Stage 3 — Clean the data

We create `df_clean` so the original `df` is still there if we need it.

Cleaning plan (keep it simple):

1. Standardise `branch` and `placement_status` text.
2. Remove duplicate rows.
3. Fix impossible numbers (CGPA outside 0–10, negative backlogs).
4. Fill remaining missing values with a median (numbers) or the most common label (categories).
5. Add helper columns for charts.
"""
)

code(
    """
df_clean = df.copy()

# 1a. Branch: remove spaces and make uppercase so 'cse', 'CSE ', 'CSE' become 'CSE'
df_clean["branch"] = df_clean["branch"].astype(str).str.strip().str.upper()

# 1b. Placement status: one spelling only
status = df_clean["placement_status"].astype(str).str.strip().str.lower()
status = status.replace({"notplaced": "not placed"})
df_clean["placement_status"] = status.map({"placed": "Placed", "not placed": "Not Placed"})

print("Clean branch labels:")
print(sorted(df_clean["branch"].unique()))
print()
print("Clean placement labels:")
print(df_clean["placement_status"].value_counts())
"""
)

code(
    """
# 2. Duplicate rows
print("Duplicates before:", df_clean.duplicated().sum())
df_clean = df_clean.drop_duplicates()
print("Duplicates after:", df_clean.duplicated().sum())
print("Rows now:", df_clean.shape[0])
"""
)

code(
    """
# 3. Impossible numbers
print("CGPA min / max before fix:", df_clean["cgpa"].min(), "/", df_clean["cgpa"].max())
print("Backlogs with negative values:", (df_clean["backlogs"] < 0).sum())

# CGPA must be between 0 and 10. Impossible values → missing, then fill with median
bad_cgpa = (df_clean["cgpa"] < 0) | (df_clean["cgpa"] > 10)
df_clean.loc[bad_cgpa, "cgpa"] = np.nan
df_clean["cgpa"] = df_clean["cgpa"].fillna(df_clean["cgpa"].median())

# Backlogs cannot be negative
df_clean.loc[df_clean["backlogs"] < 0, "backlogs"] = 0

print("CGPA min / max after fix:", df_clean["cgpa"].min(), "/", df_clean["cgpa"].max())
"""
)

code(
    """
# 4. Fill remaining missing values
intern_median = df_clean["internships"].median()
coding_mode = df_clean["coding_skill"].mode()[0]
comm_mode = df_clean["communication_skill"].mode()[0]

print("Filling internships with median:", intern_median)
print("Filling coding_skill with mode:", coding_mode)
print("Filling communication_skill with mode:", comm_mode)

df_clean["internships"] = df_clean["internships"].fillna(intern_median).astype(int)
df_clean["coding_skill"] = df_clean["coding_skill"].fillna(coding_mode)
df_clean["communication_skill"] = df_clean["communication_skill"].fillna(comm_mode)

# Unplaced students: company and role are not applicable
unplaced = df_clean["placement_status"] == "Not Placed"
df_clean.loc[unplaced, "company_type"] = df_clean.loc[unplaced, "company_type"].fillna("Not Applicable")
df_clean.loc[unplaced, "job_role"] = df_clean.loc[unplaced, "job_role"].fillna("Not Applicable")
"""
)

code(
    """
# 5. Helper columns (make later charts easier)
df_clean["is_placed"] = (df_clean["placement_status"] == "Placed").astype(int)

df_clean["cgpa_band"] = pd.cut(
    df_clean["cgpa"],
    bins=[0, 6, 7, 8, 10],
    labels=["Below 6", "6–7", "7–8", "8+"],
    include_lowest=True,
)

print("Missing values left in df_clean:")
print(df_clean.isna().sum())
print()
print("Placement rate (share of students placed):", round(df_clean["is_placed"].mean() * 100, 1), "%")
df_clean.head()
"""
)

md(
    """
`df_clean` is the table we will use from here. If a later chart looks strange, scroll back — the usual cause is running Stage 4 without running Stage 3.
"""
)

md(
    """
---
# Stage 4 — Univariate analysis (one column at a time)

Look at each important field **alone** before relating it to placement. This answers: *How many? What is typical? Are there extremes?*
"""
)

code(
    """
# Overall placement count
ax = sns.countplot(data=df_clean, x="placement_status", color="steelblue")
ax.set_title("How many students were placed?")
ax.set_xlabel("Placement status")
ax.set_ylabel("Number of students")
plt.tight_layout()
plt.show()

n = len(df_clean)
n_placed = df_clean["is_placed"].sum()
print(f"Placed: {n_placed} out of {n}  ({n_placed / n * 100:.1f}%)")
"""
)

code(
    """
# Students in each branch
order = df_clean["branch"].value_counts().index
ax = sns.countplot(data=df_clean, x="branch", order=order, color="teal")
ax.set_title("Number of students by branch")
ax.set_xlabel("Branch")
ax.set_ylabel("Count")
plt.tight_layout()
plt.show()
"""
)

code(
    """
# CGPA spread
ax = sns.histplot(data=df_clean, x="cgpa", bins=20, color="slateblue", kde=True)
ax.set_title("Distribution of CGPA")
ax.set_xlabel("CGPA")
ax.set_ylabel("Number of students")
plt.tight_layout()
plt.show()

print("Typical CGPA (median):", df_clean["cgpa"].median())
print("Average CGPA (mean):  ", round(df_clean["cgpa"].mean(), 2))
"""
)

code(
    """
# Internships
ax = sns.countplot(data=df_clean, x="internships", color="darkorange")
ax.set_title("How many internships did students complete?")
ax.set_xlabel("Number of internships")
ax.set_ylabel("Count")
plt.tight_layout()
plt.show()
"""
)

code(
    """
# Packages of placed students only (LPA = lakhs per annum)
placed = df_clean[df_clean["is_placed"] == 1]

ax = sns.histplot(data=placed, x="package_lpa", bins=25, color="seagreen")
ax.set_title("Package (LPA) for placed students")
ax.set_xlabel("Package in LPA")
ax.set_ylabel("Count")
plt.tight_layout()
plt.show()

print("Median package (LPA):", placed["package_lpa"].median())
print("Mean package (LPA):  ", round(placed["package_lpa"].mean(), 2))
print("Maximum package (LPA):", placed["package_lpa"].max())
print()
print("Notice: the maximum can be a rare 'dream offer'. Median is the fairer typical number.")
"""
)

md(
    """
**Pause.** From Stage 4 you should be able to say, in one line each:

- roughly what fraction of students got placed,
- which branches have more students in this file,
- whether CGPA is centred around 7,
- that a few packages are much higher than the rest (outliers).
"""
)

md(
    """
---
# Stage 5 — Bivariate analysis (what relates to placement?)

Now we connect **student profile → outcome**. Each block answers one practical question.

We often plot **placement percentage** (a rate) rather than raw counts, so a small branch is comparable to a large branch.
"""
)

code(
    """
def placement_percent(column):
    \"\"\"Share of students placed, as a percentage, grouped by one column.\"\"\"
    table = (
        df_clean.groupby(column, observed=True)["is_placed"]
        .mean()
        .mul(100)
        .sort_values(ascending=False)
    )
    return table.round(1)


def bar_percent(column, title, color="steelblue"):
    table = placement_percent(column)
    ax = table.plot(kind="bar", color=color)
    ax.set_title(title)
    ax.set_ylabel("Placement %")
    ax.set_xlabel(column)
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.show()
    print(table)


bar_percent("branch", "Placement percentage by branch", color="teal")
"""
)

md(
    """
**How to read this:** a higher bar means a larger share of that branch got placed. CSE / AIML / IT usually sit above core branches in campus data like this. That is a market pattern, not a value judgement of the branch.
"""
)

code(
    """
bar_percent("cgpa_band", "Placement percentage by CGPA band", color="slateblue")
"""
)

code(
    """
bar_percent("internships", "Placement percentage by number of internships", color="darkorange")
"""
)

code(
    """
bar_percent("coding_skill", "Placement percentage by coding skill", color="purple")
"""
)

code(
    """
bar_percent("knows_python", "Placement percentage by Python knowledge", color="green")

print()
print("Python vs placement inside AIML / CSE only:")
tech = df_clean[df_clean["branch"].isin(["AIML", "CSE"])]
print(
    tech.groupby("knows_python")["is_placed"].mean().mul(100).round(1).rename("placement_%")
)
"""
)

code(
    """
bar_percent("backlogs", "Placement percentage by number of backlogs", color="firebrick")
print()
print("Communication skill:")
print(placement_percent("communication_skill"))
"""
)

md(
    """
### Packages among those who *did* get placed

Placement is yes/no. Package is a second question: *among placed students, who got higher CTC?*
"""
)

code(
    """
placed = df_clean[df_clean["is_placed"] == 1]

order = (
    placed.groupby("branch")["package_lpa"].median().sort_values(ascending=False).index
)
ax = sns.boxplot(data=placed, x="branch", y="package_lpa", order=order, color="lightseagreen")
ax.set_title("Package (LPA) by branch — placed students")
ax.set_xlabel("Branch")
ax.set_ylabel("Package (LPA)")
plt.tight_layout()
plt.show()

print("Median package (LPA) by branch:")
print(placed.groupby("branch")["package_lpa"].median().sort_values(ascending=False).round(2))
"""
)

code(
    """
placed = df_clean[df_clean["is_placed"] == 1]
# Exclude 'Not Applicable' if any slipped through
placed_co = placed[placed["company_type"] != "Not Applicable"]

ax = sns.boxplot(data=placed_co, x="company_type", y="package_lpa", color="goldenrod")
ax.set_title("Package (LPA) by company type")
ax.set_xlabel("Company type")
ax.set_ylabel("Package (LPA)")
plt.tight_layout()
plt.show()

print("Median package (LPA) by company type:")
print(placed_co.groupby("company_type")["package_lpa"].median().sort_values(ascending=False).round(2))
print()
print("Common job roles for placed AIML students:")
aiml_jobs = placed[placed["branch"] == "AIML"]["job_role"].value_counts()
print(aiml_jobs)
"""
)

md(
    """
**Pause.** Write one sentence for each:

- internships,
- CGPA band,
- coding skill,
- backlogs.

Example: *“Students with 2 internships have a higher placement rate than students with 0 internships in this dataset.”*
"""
)

md(
    """
---
# Stage 6 — Five-year trends and a bigger picture

Campus results are not only about one student. The **year** matters (for example the 2021 hiring slowdown). AIML as a branch also grew in the later years.
"""
)

code(
    """
year_place = (
    df_clean.groupby("graduation_year")["is_placed"].mean().mul(100)
)

ax = year_place.plot(kind="line", marker="o", color="navy")
ax.set_title("Placement percentage by graduation year")
ax.set_xlabel("Graduation year")
ax.set_ylabel("Placement %")
ax.set_xticks(year_place.index)
plt.tight_layout()
plt.show()

print(year_place.round(1))
"""
)

code(
    """
placed = df_clean[df_clean["is_placed"] == 1]

year_pkg = placed.groupby("graduation_year")["package_lpa"].median()
ax = year_pkg.plot(kind="line", marker="o", color="seagreen")
ax.set_title("Median package (LPA) by graduation year")
ax.set_xlabel("Graduation year")
ax.set_ylabel("Median LPA")
ax.set_xticks(year_pkg.index)
plt.tight_layout()
plt.show()

print("Median LPA by year:")
print(year_pkg.round(2))
print()
print("Median LPA by year for AIML vs MECH:")
print(
    placed[placed["branch"].isin(["AIML", "MECH"])]
    .pivot_table(index="graduation_year", columns="branch", values="package_lpa", aggfunc="median")
    .round(2)
)
"""
)

code(
    """
# Placement % for every branch in every year (heatmap)
rate = (
    df_clean.pivot_table(
        index="branch",
        columns="graduation_year",
        values="is_placed",
        aggfunc="mean",
    )
    * 100
)

ax = sns.heatmap(rate.round(0), annot=True, fmt=".0f", cmap="YlGnBu")
ax.set_title("Placement % by branch and year")
ax.set_xlabel("Graduation year")
ax.set_ylabel("Branch")
plt.tight_layout()
plt.show()
"""
)

code(
    """
# Correlation of numeric columns (–1 to +1)
# A number near +1 means two columns rise together.
num_cols = ["cgpa", "internships", "projects", "backlogs", "is_placed", "package_lpa"]
corr = df_clean[num_cols].corr()

ax = sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", vmin=-1, vmax=1)
ax.set_title("Correlation between numeric columns")
plt.tight_layout()
plt.show()

print("Read this as association, not proof of cause.")
print("Example: internships may go with placement because stronger students also get internships.")
"""
)

md(
    """
---
# Stage 7 — Insights and takeaways for a 2nd-year AIML student

Below we print a compact summary. Then we interpret it in words. Your numbers should match these tables.
"""
)

code(
    """
print("=== Snapshot ===")
print("Students after cleaning:", len(df_clean))
print("Overall placement %:    ", round(df_clean["is_placed"].mean() * 100, 1))
print()
print("Placement % by branch")
print(placement_percent("branch"))
print()
print("Placement % by internships")
print(placement_percent("internships"))
print()
print("Placement % by CGPA band")
print(placement_percent("cgpa_band"))
print()
placed = df_clean[df_clean["is_placed"] == 1]
print("Median package (LPA) overall:", placed["package_lpa"].median())
print("Median package (LPA) AIML:   ", placed.loc[placed["branch"] == "AIML", "package_lpa"].median())
"""
)

md(
    """
## What the analysis is saying (in plain language)

Use this as a **template**. Adjust the wording if your printed numbers differ.

1. **Placement is not the same for every branch.** CSE, AIML, and IT typically show higher placement rates than CIVIL or MECH in this file. That reflects hiring demand, not “which branch is smarter”.
2. **Internships matter.** The placement rate usually rises as internships go from 0 to 2. For a 2nd-year student this is the most actionable chart in the notebook.
3. **CGPA helps, especially leaving the bottom band.** Moving from “Below 6” toward “7–8” is associated with a large jump. Perfect 9+ is not required for a first offer in this dataset.
4. **Coding skill and Python** move with better outcomes, particularly inside CSE / AIML. That matches what AIML interviews actually test.
5. **Backlogs hurt.** Even one backlog is associated with a lower placement rate here.
6. **Year matters.** 2021 is typically weaker (COVID hiring). Later years recover, and AIML packages trend up. Your effort still matters, but the market is a second factor.
7. **Do not worship the highest CTC.** A few dream offers pull the mean up. Quote the **median** package in a report.

## What this does *not* prove

- The file is educational / synthetic, not official SRM placement statistics.
- Charts show **association**. They do not prove “if I do an internship I will definitely be placed”.
- Many things are missing: interview performance, location, family support, luck.

## Practical motivation (what to do this year)

| Do this in 2nd year | Why the data points that way |
| --- | --- |
| Keep CGPA in a healthy band (aim 7+) | Lower bands have weaker placement rates |
| Plan at least one internship before final year | 0 internships is the weakest group |
| Treat Python as a default skill | Linked with placement in AIML / CSE |
| Build 2–3 projects you can explain | `projects` is in the file; interviews ask for them |
| Clear backlogs instead of carrying them | Negative association with placement |
| Practise speaking about your work | Communication skill is part of the table |

EDA does not replace hard work. It shows **where to aim** so 3rd-year and 4th-year effort is not random.
"""
)

md(
    """
---
# Try it yourself

Run these extra questions and write two lines of answer under each. They use `df_clean` from Stage 3.
"""
)

code(
    """
# Q1. Is there a gender gap in placement percentage?
print(placement_percent("gender"))

# Q2. Which college type has the highest placement %?
print()
print(placement_percent("college_type"))

# Q3. Among placed AIML students, what is the median package for Product vs Service companies?
aiml_placed = df_clean[(df_clean["branch"] == "AIML") & (df_clean["is_placed"] == 1)]
print()
print(aiml_placed.groupby("company_type")["package_lpa"].median().round(2))
"""
)

code(
    """
# Optional extra: scatter of CGPA vs package for placed students
placed = df_clean[df_clean["is_placed"] == 1]
ax = sns.scatterplot(data=placed, x="cgpa", y="package_lpa", hue="branch", alpha=0.5)
ax.set_title("CGPA vs package (placed students)")
ax.legend(bbox_to_anchor=(1.02, 1), loc="upper left", title="Branch")
plt.tight_layout()
plt.show()
"""
)

md(
    """
## Next step (only after this notebook feels easy)

- Repeat the same stages on another CSV from `docs/PROJECT_IDEAS.md`.
- Do **not** jump to scikit-learn until you can explain every chart in Stage 5 in your own words.

You have now done a full beginner EDA loop: **import → inspect → clean → plot → interpret**.
"""
)

nb["cells"] = cells
OUT.parent.mkdir(parents=True, exist_ok=True)
nbf.write(nb, OUT)
print(f"Wrote {OUT} with {len(cells)} cells")
