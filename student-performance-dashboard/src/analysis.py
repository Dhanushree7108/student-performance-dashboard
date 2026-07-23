"""
analysis.py
-----------
Reusable analytical functions consumed by the Streamlit dashboard.
Kept separate from the dashboard so they can also be unit-tested or
reused in a notebook / batch report.
"""

import numpy as np
import pandas as pd
from scipy.stats import pearsonr


def dashboard_insights(detailed: pd.DataFrame, trends: pd.DataFrame) -> dict:
    """Return concise, user-friendly insights for the dashboard overview."""
    subject_summary = (
        detailed.groupby("subject", observed=True)
        .agg(
            avg_score=("score", "mean"),
            pass_rate=("pass_fail", lambda x: (x == "Pass").mean() * 100),
            n=("student_id", "nunique"),
        )
        .reset_index()
    )
    if subject_summary.empty:
        return {
            "best_subject": "N/A",
            "weakest_subject": "N/A",
            "at_risk_count": 0,
            "improving_students": 0,
            "declining_students": 0,
            "top_student": "N/A",
        }

    best_subject = subject_summary.sort_values(["avg_score", "pass_rate"], ascending=False).iloc[0]
    weakest_subject = subject_summary.sort_values(["avg_score", "pass_rate"], ascending=True).iloc[0]

    top_student = None
    if not trends.empty:
        top_student_row = trends.sort_values("overall_avg_score", ascending=False).iloc[0]
        top_student = f"{top_student_row['name']} ({top_student_row['student_id']})"

    return {
        "best_subject": best_subject["subject"],
        "weakest_subject": weakest_subject["subject"],
        "at_risk_count": int(trends["risk_flag"].sum()) if not trends.empty else 0,
        "improving_students": int((trends["status"] == "Improving").sum()) if not trends.empty else 0,
        "declining_students": int((trends["status"] == "Declining").sum()) if not trends.empty else 0,
        "top_student": top_student or "N/A",
    }


def kpi_summary(df: pd.DataFrame) -> dict:
    """High-level KPI cards for the Overview tab."""
    return {
        "avg_score": round(df["score"].mean(), 1),
        "avg_attendance": round(df["attendance_pct"].mean(), 1),
        "pass_rate": round((df["pass_fail"] == "Pass").mean() * 100, 1),
        "n_students": df["student_id"].nunique(),
        "n_subjects": df["subject"].nunique(),
    }


def score_trend_by_term(df: pd.DataFrame, group_col: str | None = None) -> pd.DataFrame:
    """Average score per term, optionally split by a grouping column
    (e.g. gender, class_grade, subject)."""
    keys = ["term"] + ([group_col] if group_col else [])
    out = (
        df.groupby(keys, observed=True)["score"]
        .mean()
        .reset_index()
        .sort_values("term")
    )
    return out


def attendance_vs_score(df: pd.DataFrame):
    """Return per-student aggregate (attendance, score) pairs plus the
    Pearson correlation coefficient and p-value."""
    agg = (
        df.groupby("student_id", observed=True)
        .agg(avg_attendance=("attendance_pct", "mean"), avg_score=("score", "mean"))
        .reset_index()
    )
    r, p = pearsonr(agg["avg_attendance"], agg["avg_score"])
    return agg, r, p


def attendance_band_performance(df: pd.DataFrame) -> pd.DataFrame:
    """Average score and pass rate per attendance band."""
    out = (
        df.groupby("attendance_band", observed=True)
        .agg(
            avg_score=("score", "mean"),
            pass_rate=("pass_fail", lambda x: (x == "Pass").mean() * 100),
            n=("student_id", "nunique"),
        )
        .reset_index()
    )
    order = ["Low (<75%)", "Medium (75-89%)", "High (90-100%)"]
    out["attendance_band"] = pd.Categorical(out["attendance_band"], categories=order, ordered=True)
    return out.sort_values("attendance_band")


def subject_performance(df: pd.DataFrame) -> pd.DataFrame:
    """Average score, pass rate, std-dev (consistency) per subject."""
    out = (
        df.groupby("subject", observed=True)
        .agg(
            avg_score=("score", "mean"),
            pass_rate=("pass_fail", lambda x: (x == "Pass").mean() * 100),
            std_dev=("score", "std"),
            n=("student_id", "nunique"),
        )
        .reset_index()
        .sort_values("avg_score", ascending=False)
    )
    return out


def subject_by_class(df: pd.DataFrame) -> pd.DataFrame:
    """Average score per subject per class grade -- useful for a heatmap."""
    return (
        df.groupby(["class_grade", "subject"], observed=True)["score"]
        .mean()
        .reset_index()
    )


def top_bottom_students(trends: pd.DataFrame, n=10):
    top = trends.sort_values("overall_avg_score", ascending=False).head(n)
    bottom = trends.sort_values("overall_avg_score", ascending=True).head(n)
    return top, bottom
