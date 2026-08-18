# EDA Project Ideas for 2nd-Year BTech AIML Students

Use this page to pick a first analysis topic. The **recommended starter project** is campus placement (the notebook in this repository). The other ideas are equally valid if you want a different story — every idea below uses data that is already on the internet.

## Why start with a student-life problem?

Exploratory Data Analysis (EDA) is the habit of **looking at data before modelling**.
For a 2nd-year AIML student the best first dataset is one you already understand:

- You know what CGPA, internships, backlogs, and campus placement mean.
- You can judge whether a chart looks sensible.
- The conclusion can change how you spend the next two years (projects, Python, internships).

That is why this repository uses **BTech campus placement over the last 5 years**.

---

## Idea 1 (this project) — Campus placement of BTech students

**Question:** What actually helps a BTech student get placed, and how did that change from 2021 to 2025?

**Why it is relevant:** Placement is the outcome most engineering students worry about. EDA turns “I hope I get placed” into evidence: *internships, CGPA band, branch, Python, and communication*.

**Ready data (no hunting):** `data/campus_placement_btech.csv` in this repo.

**What you will practise:** missing values, duplicate rows, messy category labels, bar charts, box plots, year-wise trends.

---

## Idea 2 — Factors affecting MBA / campus recruitment (classic public dataset)

**Question:** Do 10th marks, degree percentage, and work experience change placement chance?

**Ready data (direct download, no Kaggle login):**

```python
url = "https://raw.githubusercontent.com/ShuklaPrashant21/Campus_Recruitment/master/Placement_Data_Full_Class.csv"
df = pd.read_csv(url)
```

Small (215 rows), clean, famous. Good if you want a tiny dataset first. It is MBA-oriented, not BTech.

---

## Idea 3 — Engineering graduate salary and skills (AMEO / AMCAT)

**Question:** Do quantitative, English, and coding scores relate to first-job salary for Indian engineering graduates?

**Where to get it:** Search GitHub for `AMEO.csv` or `aspiring_minds_employability_outcomes_2015`. Many teaching repos already host the file.

This dataset is larger and has more columns. Use it **after** you finish the placement notebook.

---

## Idea 4 — Student exam performance

**Question:** How do study hours, attendance, and previous scores relate to final marks?

**Ready data:**

```python
url = "https://raw.githubusercontent.com/AdiPersonalWorks/Random/master/student_scores%20-%20student_scores.csv"
df = pd.read_csv(url)   # very small: hours vs scores
```

Kaggle also has *Students Performance in Exams* (math / reading / writing). Needs a free Kaggle account.

---

## Idea 5 — Programming skills and developer careers

**Question:** Which languages and tools do developers actually use, and how does that line up with AIML career paths?

**Ready data:** Stack Overflow Developer Survey (official CSV download each year)  
https://insights.stackoverflow.com/survey

Good second project after placement EDA. The file is large; start with a few columns only (`LanguageHaveWorkedWith`, `DevType`, `ConvertedCompYearly`, `EdLevel`).

---

## Idea 6 — Higher-education numbers in India (AISHE / data.gov.in)

**Question:** How has BTech / AI-ML enrolment grown? Are there gender or state gaps?

**Ready data:** [data.gov.in](https://data.gov.in) — search **AISHE** (All India Survey on Higher Education). Download the CSV. No scraping.

---

## Idea 7 — Superstore / retail sales (if you want a business dataset)

**Question:** Which category, region, or month makes the most profit?

**Ready data:**

```python
# Example public mirror of the Tableau Superstore sample
# Prefer downloading the CSV once and saving it next to your notebook.
```

Search GitHub for `SampleSuperstore.csv`. Very common beginner EDA dataset, but less personal than placement data.

---

# How to gather data without wasting time

Students often spend days collecting data and never reach analysis. **Do not do that for a first EDA project.**

Follow this order:

### 1. Use a file that is already in the project (best)

This repository already contains:

```
data/campus_placement_btech.csv
```

Open the notebook and start. That is the intended path.

### 2. Load a CSV straight from a public URL

If the file is on GitHub, click **Raw**, copy the URL, then:

```python
import pandas as pd
df = pd.read_csv("https://raw.githubusercontent.com/....../file.csv")
```

If GitHub blocks the download, save the file once and use a local path:

```python
df = pd.read_csv("../data/campus_placement_btech.csv")
```

### 3. Use well-known open portals (still no scraping)

| Portal | What you get | Login? |
| --- | --- | --- |
| This repo / GitHub Raw | Placement CSV, campus recruitment CSV | No |
| [UCI ML Repository](https://archive.ics.uci.edu) | Classic teaching datasets | No |
| [data.gov.in](https://data.gov.in) | Indian government CSVs (education, employment) | Free account sometimes |
| [Kaggle Datasets](https://www.kaggle.com/datasets) | Huge variety, including Indian placement sets | Free account + one-click download |
| [Our World in Data](https://ourworldindata.org) | Clean CSVs for global topics | No |

### 4. What you should *not* do as a beginner

- Do not scrape college websites or LinkedIn.
- Do not type 1,000 rows by hand from a PDF.
- Do not wait for “real SRM placement Excel from the T&P cell” unless a teacher already gave it to you.
- Do not mix 10 different files on day 1.

If a teacher later gives you a real placement Excel from your campus, you can **reuse this same notebook**: change the file name and column names, keep the stages.

### 5. If you do use Kaggle (optional)

1. Create a free account.
2. Open the dataset page.
3. Click **Download** (CSV).
4. Put the file in a `data/` folder next to your notebook.
5. Search examples:
   - “Campus Recruitment” (benroshan)
   - “Indian Engineering College Placement Dataset”
   - “Students Performance in Exams”

Kaggle is optional. This project does not need it.

### 6. Tiny quality checklist before you start EDA

Ask only these questions:

1. Is it a CSV or Excel file I can open in pandas?
2. Does each **row** mean one student / one record?
3. Is there a clear **question** (for example: who gets placed)?
4. Are there at least a few hundred rows? (50 rows is too small; 1 million is too heavy for a first project.)
5. Is the licence OK for college use? (this repo’s teaching file is fine; cite Kaggle / UCI if you use those.)

If all five are yes, stop gathering and start analysing.
