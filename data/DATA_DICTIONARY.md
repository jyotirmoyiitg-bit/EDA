# Data Dictionary — BTech Campus Placement Dataset

**File:** `data/campus_placement_btech.csv`

**Type:** Educational / synthetic dataset for classroom EDA.  
It is **not** official SRM, NIRF, or company placement data.  
Patterns are inspired by typical Indian BTech campus-recruitment outcomes so that the analysis still feels real to a 2nd-year AIML student.

| Column | Meaning | Example values | Notes for students |
| --- | --- | --- | --- |
| `student_id` | Unique student code | `BT20240002` | Year is encoded in the ID. |
| `graduation_year` | Year the student graduated | 2021–2025 | Use this for 5-year trends. |
| `college_type` | Kind of engineering college | Deemed University, Private Engineering College, NIT, State University | Names are generic on purpose. |
| `branch` | BTech branch | CSE, AIML, IT, ECE, EEE, MECH, CIVIL | Raw file has messy labels (`cse`, `AIML `, `CSE  `). Clean these first. |
| `gender` | Gender | Male, Female |  |
| `cgpa` | Cumulative GPA on a 10-point scale | 5.0–9.8 | A few impossible values (for example `11.2`) are data-entry errors. |
| `internships` | Number of internships completed | 0–4 | Some rows are blank. |
| `projects` | Academic / personal projects | 0–8 |  |
| `backlogs` | Number of backlogs | 0–6 | A few rows have `-1` (invalid). |
| `coding_skill` | Self / test coding level | Beginner, Intermediate, Advanced | Some missing values. |
| `communication_skill` | Communication level | Poor, Average, Good, Excellent | Some missing values. |
| `knows_python` | Whether the student knows Python | Yes, No | Especially relevant for AIML / CSE. |
| `placement_status` | Campus placement result | Placed, Not Placed | Raw file also has `placed`, `not placed`, `NotPlaced`. |
| `company_type` | Type of recruiting company | Product, Service, Startup, Core, NA | `NA` means not placed. pandas may read `NA` as missing. |
| `package_lpa` | Annual package in lakhs | 2.4–32 | Blank when the student is not placed. |
| `job_role` | Role offered | Software Developer, ML Engineer, … | `NA` when not placed. |

**Size:** about 1,500 students + a few duplicate rows (cleaning practice).

**How the file was created:** `scripts/generate_dataset.py` (fixed random seed `42`). Re-run that script only if you want to rebuild the CSV.
