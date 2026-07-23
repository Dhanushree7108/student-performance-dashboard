"""
data_processing.py
-------------------
Loads raw student records and derives the features the dashboard needs:
  - pass/fail flag
  - attendance bands (Low / Medium / High)
  - per-student performance trend (regression slope across terms)
  - risk flag (attendance + declining trend + low average)

Swap `load_raw()` to point at your real data source (SQL, API, Excel,
Google Sheets, an SIS export, etc.) -- everything downstream only
depends on the column schema, not the source.
"""

import numpy as np
import pandas as pd
from pathlib import Path

RAW_PATH = Path(__file__).resolve().parent.parent / "data" / "raw" / "student_records.csv"
PASS_MARK = 40
TERM_ORDER = ["Term 1", "Term 2", "Term 3", "Term 4"]


def load_raw(path: Path = RAW_PATH) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["term"] = pd.Categorical(df["term"], categories=TERM_ORDER, ordered=True)
    return df


def attendance_band(pct: float) -> str:
    if pct >= 90:
        return "High (90-100%)"
    elif pct >= 75:
        return "Medium (75-89%)"
    else:
        return "Low (<75%)"


def add_derived_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["pass_fail"] = np.where(df["score"] >= PASS_MARK, "Pass", "Fail")
    df["attendance_band"] = df["attendance_pct"].apply(attendance_band)
    df["term_num"] = df["term"].cat.codes + 1
    return df


def student_trend(df: pd.DataFrame) -> pd.DataFrame:
    """Per-student linear trend of average score across terms.

    Returns one row per student with slope (points/term), latest average
    score, latest attendance, and a risk flag.
    """
    agg = (
        df.groupby(["student_id", "name", "class_grade", "section", "term", "term_num"],
                    observed=True)
        .agg(avg_score=("score", "mean"), avg_attendance=("attendance_pct", "mean"))
        .reset_index()
    )

    slopes = []
    for sid, g in agg.groupby("student_id"):
        g = g.sort_values("term_num")
        if len(g) >= 2:
            slope = np.polyfit(g["term_num"], g["avg_score"], 1)[0]
        else:
            slope = 0.0
        latest = g.iloc[-1]
        slopes.append({
            "student_id": sid,
            "name": latest["name"],
            "class_grade": latest["class_grade"],
            "section": latest["section"],
            "trend_slope": round(slope, 2),
            "latest_avg_score": round(latest["avg_score"], 1),
            "latest_attendance": round(latest["avg_attendance"], 1),
            "overall_avg_score": round(g["avg_score"].mean(), 1),
            "overall_avg_attendance": round(g["avg_attendance"].mean(), 1),
        })

    trend_df = pd.DataFrame(slopes)
    trend_df["risk_flag"] = (
        (trend_df["overall_avg_attendance"] < 75)
        & (trend_df["trend_slope"] < -0.5)
        & (trend_df["overall_avg_score"] < 60)
    )
    trend_df["status"] = np.select(
        [
            trend_df["risk_flag"],
            trend_df["trend_slope"] > 1,
            trend_df["trend_slope"] < -1,
        ],
        ["At Risk", "Improving", "Declining"],
        default="Stable",
    )
    return trend_df


def get_processed_data():
    """Convenience entry point used by the dashboard."""
    raw = load_raw()
    detailed = add_derived_columns(raw)
    trends = student_trend(detailed)
    return detailed, trends


if __name__ == "__main__":
    detailed, trends = get_processed_data()
    out_dir = Path(__file__).resolve().parent.parent / "data" / "processed"
    out_dir.mkdir(parents=True, exist_ok=True)
    detailed.to_csv(out_dir / "student_records_processed.csv", index=False)
    trends.to_csv(out_dir / "student_trends.csv", index=False)
    print("Detailed shape:", detailed.shape)
    print("Trends shape:", trends.shape)
    print(trends["status"].value_counts())
