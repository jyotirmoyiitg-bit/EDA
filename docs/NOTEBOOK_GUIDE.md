# What the notebook does (stage-by-stage guide)

This document explains the Jupyter notebook

`notebooks/campus_placement_eda.ipynb`

in the same order you should run it. Read a stage here, then execute that stage in the notebook. Do not skip ahead — later stages depend on a **cleaned** table from Stage 3.

---

## The problem in one paragraph

A 2nd-year BTech AIML student at a campus like SRM hears many opinions:

- “Only CGPA matters.”
- “CSE always gets placed, core branches do not.”
- “COVID years were bad.”
- “Learn Python and do internships.”

Those are **claims**. EDA is how you check claims with data: load a table, clean it, draw charts, and write a short evidence-based conclusion.

The dataset is a teaching file of about 1,500 BTech students across 2021–2025. It is synthetic (not official SRM data) but the relationships are realistic enough to practise on.

---

## How to run the notebook

1. Install Python 3.10+.
2. In a terminal, from the project folder:

```bash
pip install -r requirements.txt
jupyter notebook
```

3. Open `notebooks/campus_placement_eda.ipynb`.
4. From the menu: **Cell → Run All**, or run cell by cell with `Shift+Enter`.

The CSV path used in the notebook is:

```text
../data/campus_placement_btech.csv
```

That works when the notebook lives inside the `notebooks/` folder.

---

## Stage 1 — Import Python libraries

**Goal:** Load the four tools we need.

| Library | Why we need it |
| --- | --- |
| `pandas` | Tables (CSV → DataFrame), filtering, grouping |
| `numpy` | Simple numeric help (median, NaN) |
| `matplotlib.pyplot` | Draw plots |
| `seaborn` | Easier statistical plots on top of matplotlib |

This stage does not load data yet. If this cell fails, fix the install (`pip install -r requirements.txt`) before continuing.

---

## Stage 2 — Import data and examine the dataset

**Goal:** Answer “what is in this file?” before changing anything.

The notebook:

1. Reads the CSV into a DataFrame called `df`.
2. Shows `shape` (rows, columns).
3. Shows `head()` and `tail()`.
4. Uses `info()` for column types and non-null counts.
5. Uses `describe()` for numeric summaries.
6. Lists unique values of messy columns such as `branch` and `placement_status`.
7. Counts missing values and duplicate rows.

**What you should notice**

- About 1,508 rows, 16 columns.
- `placement_status` is not clean (`Placed`, `placed`, `NotPlaced`, …).
- `branch` has extra spaces and mixed case (`CSE  `, `aiml`).
- `internships`, `coding_skill`, `communication_skill` have missing cells.
- pandas may show `company_type` / `job_role` as missing because the file stores `NA` for unplaced students.
- A few duplicate student rows exist on purpose.

Examining first prevents you from plotting nonsense (for example treating `cse` and `CSE` as two different branches).

---

## Stage 3 — Clean the data

**Goal:** Make one trustworthy table `df_clean`.

Cleaning steps in the notebook:

1. **Copy** the raw frame so the original stays available.
2. **Strip and standardise** `branch` (uppercase, no extra spaces).
3. **Standardise** `placement_status` to only `Placed` / `Not Placed`.
4. **Drop duplicate** rows.
5. **Fix impossible numbers:** CGPA outside 0–10 becomes missing, then filled with the median. Negative backlogs become 0.
6. **Fill remaining missing values** with simple beginner rules:
   - numeric (`internships`) → median
   - categories (`coding_skill`, `communication_skill`) → most frequent value
7. **Fill company/role** with `Not Applicable` when the student is not placed.
8. Add helper columns:
   - `is_placed` (1 / 0) so averages are easy
   - `cgpa_band` (Below 6, 6–7, 7–8, 8+)

After this stage, prints in the notebook should show 0 duplicate rows and 0 missing values in the columns we use for charts.

---

## Stage 4 — Understand one column at a time (univariate)

**Goal:** See the shape of each important variable alone.

Charts / tables:

- How many students are Placed vs Not Placed (overall placement percentage).
- Count of students in each branch.
- Histogram of CGPA.
- Count of internships.
- Package (LPA) histogram for placed students only.

**Why it matters:** You cannot explain “AIML vs MECH” until you know how many students are in each branch. You cannot talk about “high packages” until you see the salary distribution.

---

## Stage 5 — Relate two things (bivariate)

**Goal:** Connect student profile → placement outcome.

The notebook compares:

| Comparison | Question it answers |
| --- | --- |
| Branch vs placement % | Do CSE / AIML really place better than CIVIL / MECH? |
| CGPA band vs placement % | Is there a CGPA threshold where placement jumps? |
| Internships vs placement % | Is 0 internship very different from 2 internships? |
| Coding skill vs placement % | Does “Advanced” help? |
| Python vs placement (especially AIML/CSE) | Is Python associated with better outcomes? |
| Backlogs vs placement % | Do backlogs hurt? |
| Package by branch (boxplot) | Who gets higher CTC among those who are placed? |
| Company type vs package | Product vs Service vs Startup vs Core |

This is the heart of the project. Write one sentence under each chart in your own words.

---

## Stage 6 — Time trends and a bigger picture

**Goal:** Use the 5-year window.

The notebook:

- Plots placement percentage by `graduation_year` (COVID-year dip vs recovery).
- Plots median package by year and by branch (AIML / CSE growth).
- Shows a correlation heatmap of numeric columns.
- Cross-tab of branch × year placement rates.

You should be able to say whether 2021 looks weaker, and whether AIML packages moved up in 2024–2025.

---

## Stage 7 — Insights, limitations, and what a 2nd-year student can do

**Goal:** Turn charts into a short, honest conclusion.

Typical evidence-based takeaways (confirm them with your own output; do not memorise blindly):

1. Placement is high overall in this teaching dataset, but **not equal across branches**.
2. **Internships** and **coding skill** move with placement rate.
3. **CGPA** helps, especially below vs above the 7–8 band, but it is not the only factor.
4. **Backlogs** are associated with lower placement.
5. **2021** is a weaker year — a reminder that the job market is not only about the student.
6. For AIML students, **Python + projects + internships** line up with better roles (ML Engineer / Data Analyst) and packages.
7. A few very high packages are **outliers** (dream offers). Median is a fairer number than the maximum.

**Limitations you must mention in a viva / report**

- The file is synthetic / educational, not official campus statistics.
- Correlation is not causation (students who do internships may also have higher CGPA).
- “College type” is generic; it is not a ranking of named universities.

**Practical motivation for an SRM 2nd-year AIML student**

- Keep CGPA in a healthy band now; it is harder to repair in 4th year.
- Do at least one internship before final year.
- Treat Python as a default skill, not an optional extra.
- Build 2–3 projects you can explain.
- Practise communication (interviews are not only coding).

---

## What to submit (if this is a college assignment)

1. The executed notebook (charts visible).
2. This guide is already written for you; add a 1–2 page summary in your own words.
3. Three extra questions you tried (the notebook has “Try it yourself” cells).

Suggested extra questions:

- Is there a gender gap in placement % or in package?
- Among placed AIML students, what is the most common job role?
- Which college type has the highest median package?

---

## Mapping: document stage → notebook headings

| This guide | Notebook heading |
| --- | --- |
| Stage 1 | Stage 1 — Import Python libraries |
| Stage 2 | Stage 2 — Import data and examine the dataset |
| Stage 3 | Stage 3 — Clean the data |
| Stage 4 | Stage 4 — Univariate analysis |
| Stage 5 | Stage 5 — Bivariate analysis |
| Stage 6 | Stage 6 — Trends (5 years) and multivariate view |
| Stage 7 | Stage 7 — Insights and student takeaways |
