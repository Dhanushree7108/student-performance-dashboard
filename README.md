# 🎓 Student Performance Analytical Dashboard

An interactive, data-driven analytics dashboard built with **Python, Streamlit, Pandas, NumPy, Plotly, and Scikit-learn** to monitor student academic performance, analyze attendance patterns, identify performance trends, and detect academically at-risk students.

The project transforms raw student academic records into meaningful visual insights, helping educational institutions make informed, data-driven decisions.

---

## 📌 Project Overview

Educational institutions generate large amounts of student data, including attendance records, examination scores, subject-wise performance, and academic progress across multiple terms.

However, identifying students who are struggling, understanding performance patterns, and tracking academic improvement can be challenging when working with raw datasets.

The **Student Performance Analytical Dashboard** addresses this challenge through an interactive analytics platform that processes student records, calculates meaningful performance indicators, and presents actionable insights through visualizations and student-level analysis.

The system supports both institution-wide performance monitoring and individual student performance tracking.

## 🎯 Project Objectives

- Monitor overall student academic performance.
- Analyze attendance and its relationship with academic scores.
- Track student performance across multiple academic terms.
- Compare performance across classes, sections, and subjects.
- Identify improving, stable, and declining students.
- Automatically flag potentially at-risk students using configurable analytical thresholds.
- Present educational data through interactive dashboards and visual reports.

## ✨ Key Features

### 1. 📊 Academic Performance Overview

Provides a consolidated view of institutional academic performance.

- Total student count.
- Overall average academic score.
- Average attendance percentage.
- Overall pass percentage.
- Student performance status distribution.
- Academic performance trends across terms.

### 2. 📈 Student Performance Trend Analysis

Analyzes longitudinal academic performance across multiple terms.

- Tracks individual student score progression.
- Calculates performance trend slopes using linear regression.
- Classifies students as Improving, Stable, or Declining.
- Visualizes score distributions across terms.
- Identifies changes in academic performance over time.

### 3. 🗓️ Attendance Impact Analysis

Examines the relationship between student attendance and academic outcomes.

- Attendance versus academic score analysis.
- Pearson correlation coefficient.
- Statistical significance using p-values.
- Performance comparison across Low, Medium, and High attendance groups.
- Pass-rate analysis by attendance category.

### 4. 📚 Subject-Wise Performance Analytics

Provides insights into academic performance across different subjects.

- Subject-wise average scores.
- Subject-wise pass percentages.
- Class and subject performance heatmaps.
- Score variability and standard deviation.
- Identification of subjects with inconsistent performance.

### 5. 🚨 At-Risk Student Identification

Uses analytical rules to identify students who may require additional academic support.

The risk identification logic considers:

- Low attendance percentage.
- Declining academic performance trend.
- Low overall academic average.

Default risk conditions:

- Attendance below 75%.
- Performance trend slope below -0.5.
- Overall average score below 60%.

These configurable conditions help identify students who may benefit from early academic intervention.

### 6. 🔍 Individual Student Analysis

Provides student-level performance insights.

- Individual academic profiles.
- Score progression across terms.
- Subject-wise score comparisons.
- Performance status.
- Identification of top and bottom performers.
- Student-level risk monitoring.

### 7. 🎛️ Interactive Data Exploration

- Filter records by class and section.
- Filter by subject, gender, and academic term.
- Explore filtered datasets.
- Inspect processed student records.
- Download available data as CSV files.
- Refresh and review dataset information.

All analytical views respond to the selected filters.

---

## 🧠 Data Processing and Analytics Workflow

The project follows a structured data analytics pipeline, starting from raw academic records and ending with interactive visual insights.

```text
             RAW STUDENT DATA
                    |
                    v
             DATA GENERATION
                    |
                    v
              DATA CLEANING
                    |
                    v
          FEATURE ENGINEERING
                    |
          +---------+---------+
          |                   |
          v                   v
     ATTENDANCE           SCORE ANALYSIS
      ANALYSIS                  |
          |                     |
          +----------+----------+
                     |
                     v
             TREND CALCULATION
                     |
                     v
            RISK IDENTIFICATION
                     |
                     v
           ANALYTICAL AGGREGATION
                     |
                     v
           STREAMLIT DASHBOARD
                     |
          +----------+----------+
          |          |          |
          v          v          v
       OVERVIEW   SUBJECT    STUDENT
                  ANALYSIS   INSIGHTS
```

### Core Analytical Methods

| Method | Application |
|---|---|
| Data Cleaning | Handling and preparing student records |
| Feature Engineering | Deriving attendance bands and performance indicators |
| Linear Regression | Calculating student performance trend slopes |
| Pearson Correlation | Measuring attendance-score relationships |
| Statistical Analysis | Evaluating correlation significance |
| Aggregation | Computing class, subject, and student-level KPIs |
| Rule-Based Risk Analysis | Identifying potentially at-risk students |

---

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core application development |
| Pandas | Data manipulation and analysis |
| NumPy | Numerical computation |
| Scikit-learn | Regression and analytical methods |
| SciPy | Statistical analysis and correlation |
| Plotly Express | Interactive data visualizations |
| Streamlit | Interactive dashboard development |
| CSV | Dataset storage and processing |

## 📂 Project Structure

```text
student-performance-dashboard/
│
├── data/
│   ├── raw/
│   │   └── student_records.csv
│   │
│   └── processed/
│       ├── student_records_processed.csv
│       └── student_trends.csv
│
├── src/
│   ├── data_generator.py
│   ├── data_processing.py
│   └── analysis.py
│
├── dashboard/
│   └── app.py
│
├── notebooks/
│
├── outputs/
│
├── requirements.txt
│
└── README.md
```

### Main Components

**`data_generator.py`**
- Generates synthetic student academic records.
- Creates data with meaningful academic performance patterns.
- Supports reproducible dataset generation.

**`data_processing.py`**
- Loads and prepares raw student data.
- Performs data cleaning and feature engineering.
- Calculates attendance bands and performance indicators.
- Generates student-level performance trends.
- Identifies potentially at-risk students.

**`analysis.py`**
- Computes academic KPIs.
- Performs statistical analysis.
- Calculates correlations and aggregated metrics.
- Prepares analytical results for visualization.

**`dashboard/app.py`**
- Implements the interactive Streamlit dashboard.
- Displays KPIs, charts, tables, and student-level insights.
- Provides filtering and data exploration functionality.

---

## 📊 Dataset Information

The project includes a synthetic educational dataset generated for demonstration and analytical testing.

| Dataset Attribute | Value |
|---|---:|
| Total Students | 480 |
| Subjects | 5 |
| Academic Terms | 4 |
| Total Records | 9,600 |
| Records per Student | 20 |

Each record represents one student's performance in a particular subject and academic term.

### Dataset Features

| Column | Description |
|---|---|
| student_id | Unique student identifier |
| name | Student name |
| gender | Student gender category |
| class_grade | Academic grade or class |
| section | Class section |
| parental_support | Parental support category |
| extracurricular | Extracurricular participation |
| term | Academic term |
| subject | Subject name |
| attendance_pct | Attendance percentage |
| score | Marks obtained |
| max_score | Maximum possible marks |
| study_hours_per_week | Weekly study hours |
| pass_fail | Academic result |
| attendance_band | Categorized attendance level |
| term_num | Numerical term representation |

**Note:** The included dataset is synthetic and is not intended to represent actual student records.

---

## ⚙️ Installation and Setup

### Prerequisites

- Python 3.10 or later.
- Git.
- pip package manager.

### Step 1: Clone the Repository

```bash
git clone https://github.com/Dhanushree7108/student-performance-dashboard.git
```

### Step 2: Navigate to the Project

```bash
cd student-performance-dashboard
```

### Step 3: Create a Virtual Environment

```bash
python -m venv venv
```

Activate it:

**Windows**

```bash
venv\Scripts\activate
```

**macOS / Linux**

```bash
source venv/bin/activate
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 5: Generate the Dataset

```bash
python src/data_generator.py
```

If the generated dataset is already available, this step can be skipped.

### Step 6: Process the Data

```bash
python src/data_processing.py
```

### Step 7: Launch the Dashboard

```bash
streamlit run dashboard/app.py
```

Open the application in your browser:

```text
http://localhost:8501
```

---

## 📉 Analytical Insights

The dashboard is designed to help answer important educational questions:

1. What is the overall academic performance of the institution?
2. Which students are showing consistent academic improvement?
3. Which students have declining performance across terms?
4. How strongly is attendance associated with academic scores?
5. Which subjects have lower average performance?
6. Which classes require additional academic attention?
7. Which students meet the defined at-risk criteria?
8. How does student performance change across academic terms?

---

## 🔐 Data Privacy and Limitations

- The bundled dataset contains synthetic student information.
- Real student records should be handled according to applicable data protection and institutional policies.
- At-risk identification is rule-based, not a clinical or definitive prediction of academic failure.
- Correlation does not establish causation between attendance and academic performance.
- Results depend on data quality, completeness, and the selected analytical thresholds.
- The current implementation uses CSV-based data storage.

---

## 🔮 Future Enhancements

Potential improvements to expand the platform include:

- PostgreSQL integration for centralized academic data management.
- Automated ETL pipelines for periodic student record updates.
- Machine learning models for early academic risk prediction.
- AI-powered academic insights and personalized recommendations.
- Role-based dashboards for teachers, administrators, and parents.
- Student progress reports with PDF export.
- Real-time analytics and institutional reporting.
- Secure authentication and access management.

These are proposed enhancements and are not represented as completed features.

---

## 🎓 Learning Outcomes

Through this project, I gained practical experience in:

- End-to-end data analytics workflows.
- Data cleaning and feature engineering.
- Exploratory data analysis.
- Statistical analysis and correlation
