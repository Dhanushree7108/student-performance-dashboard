"""
data_generator.py
------------------
Generates a realistic synthetic dataset for the Student Performance
Analytical Dashboard. Replace this with a loader for your real
school/institution data once available (see data_processing.py for the
expected schema).

Output: data/raw/student_records.csv
Schema (one row = one student, one subject, one term):
    student_id, name, gender, class_grade, section,
    term, subject, attendance_pct, score, max_score,
    study_hours_per_week, parental_support, extracurricular
"""

import numpy as np
import pandas as pd
from pathlib import Path

RNG = np.random.default_rng(42)

CLASSES = [9, 10, 11, 12]
SECTIONS = ["A", "B", "C"]
SUBJECTS = ["Mathematics", "Science", "English", "Social Studies", "Computer Science"]
TERMS = ["Term 1", "Term 2", "Term 3", "Term 4"]
N_STUDENTS = 480

FIRST_NAMES = [
    "Aarav", "Vivaan", "Aditya", "Vihaan", "Arjun", "Sai", "Reyansh", "Krishna",
    "Ishaan", "Rohan", "Ananya", "Diya", "Saanvi", "Aadhya", "Kiara", "Myra",
    "Anika", "Riya", "Isha", "Tara", "Kabir", "Dev", "Yash", "Neha", "Priya",
    "Meera", "Aryan", "Zara", "Nikhil", "Sneha"
]
LAST_NAMES = [
    "Sharma", "Verma", "Gupta", "Iyer", "Nair", "Reddy", "Rao", "Patel",
    "Singh", "Mehta", "Kumar", "Das", "Chopra", "Malhotra", "Bose", "Pillai"
]


def _student_master(n=N_STUDENTS):
    """Create one row per student with fixed attributes."""
    ids = [f"STU{1000 + i}" for i in range(n)]
    names = [f"{RNG.choice(FIRST_NAMES)} {RNG.choice(LAST_NAMES)}" for _ in range(n)]
    genders = RNG.choice(["Male", "Female"], size=n, p=[0.51, 0.49])
    classes = RNG.choice(CLASSES, size=n)
    sections = RNG.choice(SECTIONS, size=n)
    parental_support = RNG.choice(["Low", "Medium", "High"], size=n, p=[0.2, 0.5, 0.3])
    extracurricular = RNG.choice(["Yes", "No"], size=n, p=[0.4, 0.6])

    # Each student has a hidden "ability" and "engagement" trait that
    # drives correlated attendance + scores across subjects/terms.
    ability = RNG.normal(0, 1, size=n)
    engagement = RNG.normal(0, 1, size=n)

    return pd.DataFrame({
        "student_id": ids,
        "name": names,
        "gender": genders,
        "class_grade": classes,
        "section": sections,
        "parental_support": parental_support,
        "extracurricular": extracurricular,
        "_ability": ability,
        "_engagement": engagement,
    })


def generate(n_students=N_STUDENTS, seed=42, out_path="data/raw/student_records.csv"):
    global RNG
    RNG = np.random.default_rng(seed)

    students = _student_master(n_students)
    rows = []

    support_bonus = {"Low": -4, "Medium": 0, "High": 4}
    subject_difficulty = {
        "Mathematics": -3, "Science": -1, "English": 2,
        "Social Studies": 3, "Computer Science": 0,
    }

    for _, s in students.iterrows():
        # a slow trend so some students improve/decline across terms
        trend_slope = RNG.normal(0, 2.2)

        for t_idx, term in enumerate(TERMS):
            # attendance depends on engagement + mild term fatigue + noise
            base_att = 78 + 10 * s["_engagement"] - 1.5 * t_idx
            attendance = np.clip(RNG.normal(base_att, 6), 45, 100)

            for subject in SUBJECTS:
                base_score = (
                    68
                    + 9 * s["_ability"]
                    + 0.18 * (attendance - 75)          # attendance impact
                    + support_bonus[s["parental_support"]]
                    + subject_difficulty[subject]
                    + trend_slope * t_idx * 0.6          # term-over-term drift
                    + (3 if s["extracurricular"] == "Yes" and s["_engagement"] > 0 else 0)
                )
                score = np.clip(RNG.normal(base_score, 7), 0, 100)
                study_hours = np.clip(
                    RNG.normal(6 + 3 * s["_engagement"], 2), 0, 25
                )

                rows.append({
                    "student_id": s["student_id"],
                    "name": s["name"],
                    "gender": s["gender"],
                    "class_grade": s["class_grade"],
                    "section": s["section"],
                    "parental_support": s["parental_support"],
                    "extracurricular": s["extracurricular"],
                    "term": term,
                    "subject": subject,
                    "attendance_pct": round(attendance, 1),
                    "score": round(score, 1),
                    "max_score": 100,
                    "study_hours_per_week": round(study_hours, 1),
                })

    df = pd.DataFrame(rows)

    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_path, index=False)
    print(f"Generated {len(df):,} rows for {n_students} students -> {out_path}")
    return df


if __name__ == "__main__":
    generate()
