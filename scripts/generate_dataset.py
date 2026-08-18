"""Generate the educational BTech campus-placement dataset.

The file is synthetic and is meant for classroom EDA. Patterns inside it
are inspired by typical Indian engineering placement outcomes
(branch gaps, internship effect, COVID-year dip, AIML package growth).
It is NOT official SRM / NIRF / company data.

Run from the repository root:

    python scripts/generate_dataset.py
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

RNG = np.random.default_rng(42)
N_STUDENTS = 1500
OUTPUT = Path(__file__).resolve().parents[1] / "data" / "campus_placement_btech.csv"

BRANCHES = np.array(["CSE", "AIML", "IT", "ECE", "EEE", "MECH", "CIVIL"])
BRANCH_P = np.array([0.22, 0.14, 0.12, 0.16, 0.10, 0.14, 0.12])
YEARS = np.array([2021, 2022, 2023, 2024, 2025])
COLLEGE_TYPES = np.array(
    ["Deemed University", "Private Engineering College", "NIT", "State University"]
)
COLLEGE_P = np.array([0.40, 0.32, 0.12, 0.16])
CODING = np.array(["Beginner", "Intermediate", "Advanced"])
COMM = np.array(["Poor", "Average", "Good", "Excellent"])

BRANCH_PLACE_BASE = {
    "CSE": 0.82,
    "AIML": 0.80,
    "IT": 0.78,
    "ECE": 0.70,
    "EEE": 0.62,
    "MECH": 0.55,
    "CIVIL": 0.48,
}
YEAR_PLACE_ADJ = {2021: -0.12, 2022: -0.04, 2023: 0.02, 2024: 0.05, 2025: 0.06}
COLLEGE_PLACE_ADJ = {
    "NIT": 0.10,
    "Deemed University": 0.04,
    "Private Engineering College": -0.03,
    "State University": -0.05,
}
BRANCH_PACKAGE_BASE = {
    "CSE": 7.5,
    "AIML": 8.0,
    "IT": 6.8,
    "ECE": 5.8,
    "EEE": 5.0,
    "MECH": 4.6,
    "CIVIL": 4.2,
}
YEAR_PACKAGE_MULT = {2021: 0.88, 2022: 0.95, 2023: 1.00, 2024: 1.08, 2025: 1.14}


def clip01(x: np.ndarray | float) -> np.ndarray | float:
    return np.clip(x, 0.04, 0.96)


def choose_company_and_role(branch: str, coding: str, python_yes: bool, cgpa: float) -> tuple[str, str]:
    tech = branch in {"CSE", "AIML", "IT"}
    if tech and coding == "Advanced" and cgpa >= 8.0:
        company = RNG.choice(["Product", "Startup", "Service"], p=[0.45, 0.25, 0.30])
    elif tech:
        company = RNG.choice(["Product", "Startup", "Service"], p=[0.20, 0.20, 0.60])
    elif branch in {"ECE", "EEE"}:
        company = RNG.choice(["Product", "Service", "Core"], p=[0.15, 0.55, 0.30])
    else:
        company = RNG.choice(["Service", "Core", "Startup"], p=[0.45, 0.45, 0.10])

    if branch == "AIML" and python_yes:
        role = RNG.choice(
            ["ML Engineer", "Data Analyst", "Data Scientist", "Software Developer"],
            p=[0.35, 0.30, 0.15, 0.20],
        )
    elif tech:
        role = RNG.choice(
            ["Software Developer", "Data Analyst", "QA Engineer", "DevOps Engineer"],
            p=[0.55, 0.20, 0.15, 0.10],
        )
    elif branch in {"ECE", "EEE"}:
        role = RNG.choice(
            ["Embedded Engineer", "Software Developer", "Core Engineer", "QA Engineer"],
            p=[0.30, 0.30, 0.25, 0.15],
        )
    else:
        role = RNG.choice(
            ["Core Engineer", "Operations", "Software Developer", "Analyst"],
            p=[0.45, 0.25, 0.15, 0.15],
        )
    return company, role


def package_lpa(branch: str, year: int, company: str, cgpa: float, internships: int) -> float:
    base = BRANCH_PACKAGE_BASE[branch] * YEAR_PACKAGE_MULT[year]
    company_mult = {"Product": 1.55, "Startup": 1.25, "Service": 0.85, "Core": 0.90}[company]
    skill_boost = 1 + 0.08 * internships + 0.06 * max(cgpa - 7.0, 0)
    value = RNG.normal(base * company_mult * skill_boost, 0.9)
    # A few dream offers
    if RNG.random() < 0.018 and branch in {"CSE", "AIML", "IT"} and company == "Product":
        value = RNG.uniform(18, 32)
    return round(float(np.clip(value, 2.4, 34.0)), 2)


def main() -> None:
    rows = []
    for i in range(1, N_STUDENTS + 1):
        year = int(RNG.choice(YEARS))
        branch = str(RNG.choice(BRANCHES, p=BRANCH_P))
        college = str(RNG.choice(COLLEGE_TYPES, p=COLLEGE_P))
        gender = str(RNG.choice(["Male", "Female"], p=[0.62, 0.38]))

        cgpa = float(np.clip(RNG.normal(7.15, 0.95), 5.0, 9.8))
        internships = int(np.clip(RNG.poisson(1.1), 0, 4))
        projects = int(np.clip(RNG.poisson(2.4), 0, 8))
        backlogs = int(np.clip(RNG.poisson(0.6 if cgpa < 7 else 0.15), 0, 6))
        coding = str(RNG.choice(CODING, p=[0.28, 0.48, 0.24]))
        communication = str(RNG.choice(COMM, p=[0.10, 0.38, 0.37, 0.15]))
        python_yes = bool(
            RNG.random()
            < (0.85 if branch in {"AIML", "CSE", "IT"} else 0.35)
        )

        p = BRANCH_PLACE_BASE[branch]
        p += YEAR_PLACE_ADJ[year]
        p += COLLEGE_PLACE_ADJ[college]
        p += 0.10 * (cgpa - 7.0)
        p += 0.07 * internships
        p += {"Beginner": -0.10, "Intermediate": 0.03, "Advanced": 0.12}[coding]
        p += {"Poor": -0.08, "Average": 0.0, "Good": 0.04, "Excellent": 0.07}[communication]
        p -= 0.07 * backlogs
        if python_yes and branch in {"AIML", "CSE", "IT"}:
            p += 0.04
        if year >= 2023 and branch == "AIML":
            p += 0.04
        placed = RNG.random() < clip01(p)

        if placed:
            company, role = choose_company_and_role(branch, coding, python_yes, cgpa)
            pkg = package_lpa(branch, year, company, cgpa, internships)
            status = "Placed"
        else:
            company, role, pkg, status = "NA", "NA", np.nan, "Not Placed"

        rows.append(
            {
                "student_id": f"BT{year}{i:04d}",
                "graduation_year": year,
                "college_type": college,
                "branch": branch,
                "gender": gender,
                "cgpa": round(cgpa, 2),
                "internships": internships,
                "projects": projects,
                "backlogs": backlogs,
                "coding_skill": coding,
                "communication_skill": communication,
                "knows_python": "Yes" if python_yes else "No",
                "placement_status": status,
                "company_type": company,
                "package_lpa": pkg,
                "job_role": role,
            }
        )

    df = pd.DataFrame(rows)

    # --- Intentional messiness so beginners practise cleaning ---
    messy = df.copy()

    # Extra spaces / mixed case in a few branch labels
    dirty_idx = RNG.choice(messy.index, size=35, replace=False)
    messy.loc[dirty_idx[:12], "branch"] = messy.loc[dirty_idx[:12], "branch"] + " "
    messy.loc[dirty_idx[12:22], "branch"] = messy.loc[dirty_idx[12:22], "branch"].str.lower()
    messy.loc[dirty_idx[22:28], "branch"] = "aiml"
    messy.loc[dirty_idx[28:], "branch"] = "CSE  "

    # Mixed placement labels
    placed_idx = messy.index[messy["placement_status"] == "Placed"]
    not_idx = messy.index[messy["placement_status"] == "Not Placed"]
    messy.loc[RNG.choice(placed_idx, size=18, replace=False), "placement_status"] = "placed"
    messy.loc[RNG.choice(not_idx, size=12, replace=False), "placement_status"] = "not placed"
    messy.loc[RNG.choice(not_idx, size=8, replace=False), "placement_status"] = "NotPlaced"

    # Missing values
    messy.loc[RNG.choice(messy.index, size=55, replace=False), "internships"] = np.nan
    messy.loc[RNG.choice(messy.index, size=40, replace=False), "communication_skill"] = np.nan
    messy.loc[RNG.choice(messy.index, size=25, replace=False), "coding_skill"] = np.nan

    # Invalid values (data-entry mistakes)
    messy.loc[RNG.choice(messy.index, size=6, replace=False), "cgpa"] = RNG.choice(
        [10.4, 11.2, 0.0, 12.0]
    )
    messy.loc[RNG.choice(messy.index, size=5, replace=False), "backlogs"] = -1

    # Duplicate rows
    dupes = messy.sample(8, random_state=7)
    messy = pd.concat([messy, dupes], ignore_index=True)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    messy.to_csv(OUTPUT, index=False)
    print(f"Wrote {len(messy)} rows to {OUTPUT}")
    print(messy.head(3).to_string(index=False))


if __name__ == "__main__":
    main()
