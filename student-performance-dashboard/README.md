# 🎓 Student Performance Analytical Dashboard

An end-to-end, interactive analytics dashboard for tracking student
performance — built to surface **performance trends**, **attendance
impact**, and **subject-wise analysis**, with student-level drill-down
and at-risk flagging.

---

## 1. Project Structure

```
student-performance-dashboard/
├── data/
│   ├── raw/                     # source data (CSV export from school system)
│   │   └── student_records.csv
│   └── processed/                # cleaned + feature-engineered output
│       ├── student_records_processed.csv
│       └── student_trends.csv
├── src/
│   ├── data_generator.py         # generates realistic synthetic demo data
│   ├── data_processing.py        # loads, cleans, engineers features
│   └── analysis.py               # KPIs, correlations, aggregations
├── dashboard/
│   └── app.py                    # Streamlit interactive dashboard (main entry point)
├── notebooks/                    # optional exploratory analysis (Jupyter)
├── outputs/                      # exported charts / reports
├── requirements.txt
└── README.md
```

---

## 2. Tools & Tech Stack

| Layer                  | Tool                                   | Why |
|-------------------------|-----------------------------------------|-----|
| Language                | **Python 3.10+**                        | Data ecosystem, fast to build & extend |
| Data wrangling          | **pandas / numpy**                      | Cleaning, aggregation, feature engineering |
| Statistics              | **scipy / scikit-learn**                | Correlation tests, trend regression |
| Visualization            | **Plotly Express**                      | Interactive charts (zoom, hover, filter) natively in-browser |
| Dashboard framework      | **Streamlit**                           | Turns Python scripts into a full interactive web app with no frontend code |
| Data storage (demo)      | **CSV**                                 | Simple, swappable — replace with SQL/Excel/API in production |

**Why this stack:** it's the fastest path from raw data to a shareable,
interactive dashboard, and it's 100% Python — no separate frontend
build step. It's also easy to swap pieces later (e.g. plug in a real
database, or migrate the frontend to a React + FastAPI app if you need
multi-user auth, role-based access, etc. — see "Scaling Up" below).

---

## 3. Setup & Run

```bash
# 1. Create a virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Generate the demo dataset (skip this if you have real data)
python3 src/data_generator.py

# 4. (Optional) pre-process and cache derived tables to disk
python3 src/data_processing.py

# 5. Launch the dashboard
streamlit run dashboard/app.py
```

The dashboard opens at `http://localhost:8501`.

---

## 4. Using Your Own Data

Replace `data/raw/student_records.csv` with your real export, keeping
this schema (one row = one student + subject + term):

| Column                  | Type    | Description |
|---------------------------|---------|--------------|
| `student_id`               | string  | Unique student identifier |
| `name`                     | string  | Student name |
| `gender`                   | string  | Male / Female / Other |
| `class_grade`              | int/str | Grade or class level |
| `section`                  | string  | Section/division |
| `parental_support`         | string  | Low / Medium / High (optional) |
| `extracurricular`          | string  | Yes / No (optional) |
| `term`                     | string  | Term/semester label, e.g. "Term 1" |
| `subject`                  | string  | Subject name |
| `attendance_pct`           | float   | Attendance % for that term/subject |
| `score`                    | float   | Score achieved |
| `max_score`                | float   | Maximum possible score |
| `study_hours_per_week`     | float   | Optional, enables extra analysis |

If your source is a SQL database, Excel file, or an API instead of a
CSV, only `src/data_processing.py::load_raw()` needs to change —
everything downstream (feature engineering, analysis, dashboard) is
schema-driven and doesn't care where the data came from.

---

## 5. Dashboard Features

### 📊 Overview
- KPI cards: total students, average score, average attendance, pass rate
- Overall score trend across terms
- Pass/fail split
- Student status breakdown (Improving / Stable / Declining / At Risk)

### 📈 Performance Trends
- Score trend over terms, segmentable by gender, class, section, or subject
- Score distribution (box plot) per term
- Histogram of per-student improvement/decline slopes

### 🗓️ Attendance Impact
- Scatter plot of attendance vs. score with trendline + Pearson correlation (r, p-value)
- Performance and pass rate broken down by attendance band (Low / Medium / High)

### 📚 Subject-wise Analysis
- Average score and pass rate ranked by subject
- Class × Subject performance heatmap
- Score consistency (standard deviation) per subject — flags subjects with inconsistent outcomes

### 🔍 Student Drill-down
- Auto-generated at-risk list (low attendance + declining trend + low average)
- Individual student profile: score-by-term line chart, score-by-subject bar chart
- Top 10 / bottom 10 performers

All tabs respect the **sidebar filters** (class, section, subject, gender, term), so every chart reflects the currently selected slice of data.

---

## 6. How the Analytics Work

- **Trend slope**: for each student, a linear regression of average
  score vs. term number is fit; the slope (points/term) determines
  whether they're `Improving`, `Stable`, or `Declining`.
- **At-risk flag**: attendance < 75% **and** declining trend (slope < -0.5) **and** overall average score < 60.
  These thresholds are configurable in `src/data_processing.py`.
- **Attendance impact**: Pearson correlation between per-student
  average attendance and average score, plus a banded comparison
  (Low/Medium/High attendance) for a more actionable, less
  statistics-heavy view.
- **Subject-wise**: average score, pass rate, and standard deviation
  (as a consistency/difficulty signal) per subject, plus a class ×
  subject heatmap to spot where specific grades struggle with specific
  subjects.

---

## 7. Extending the Project

- **Authentication / multi-user**: wrap with `streamlit-authenticator`, or migrate to a FastAPI backend + React frontend for role-based access (teachers vs. admins vs. parents).
- **Live data**: replace the CSV loader with a SQLAlchemy connection to your school's SIS/database; add `st.cache_data(ttl=...)` for periodic refresh.
- **Predictive modeling**: `scikit-learn` is already in the stack — add a classifier (e.g. logistic regression / gradient boosting) to predict at-risk students *before* the term ends, rather than only flagging after the fact.
- **Export/reporting**: add a "Download PDF report" button per student/class using the same data already computed in `analysis.py`.
- **Deployment**: `streamlit run dashboard/app.py` works locally; for sharing, deploy to Streamlit Community Cloud, a Docker container, or an internal server.

---

## 8. Notes

- The bundled dataset (`data/raw/student_records.csv`) is **synthetic**, generated by `src/data_generator.py` with reproducible seeding (480 students × 5 subjects × 4 terms = 9,600 rows). It's built to have realistic, non-trivial correlations (attendance → score, term-over-term drift, parental support effect) so every chart in the dashboard shows a meaningful pattern out of the box.
- Delete `data/raw/student_records.csv` and re-run `python3 src/data_generator.py` any time you want a fresh demo dataset, or with a different `n_students`/`seed`.
