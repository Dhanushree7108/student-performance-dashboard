from flask import Flask, render_template_string
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from analysis import dashboard_insights, kpi_summary
from data_processing import get_processed_data

app = Flask(__name__)

HTML_TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>BrightPath Analytics</title>
  <style>
    :root { color-scheme: light; }
    body { font-family: 'Segoe UI', Arial, sans-serif; margin: 0; background: linear-gradient(135deg, #f3ebff 0%, #e8fbff 100%); color: #2d1b69; }
    header { background: linear-gradient(135deg, #5b21b6, #22d3ee); color: white; padding: 56px 24px 32px; }
    nav { display: flex; justify-content: space-between; align-items: center; max-width: 1200px; margin: 0 auto; }
    nav a { color: white; text-decoration: none; margin-left: 16px; font-weight: 600; }
    .hero { max-width: 1200px; margin: 24px auto 0; display: grid; grid-template-columns: 1.2fr 0.8fr; gap: 24px; align-items: center; }
    .hero h1 { font-size: 2.5rem; margin-bottom: 10px; }
    .hero p { font-size: 1.05rem; line-height: 1.6; opacity: 0.95; }
    .card { background: white; border-radius: 18px; padding: 20px; box-shadow: 0 12px 35px rgba(91, 33, 182, 0.12); }
    section { max-width: 1200px; margin: 24px auto; padding: 0 24px 30px; }
    .grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; }
    .metric { background: white; border: 1px solid #e7dcff; border-radius: 16px; padding: 18px; box-shadow: 0 10px 24px rgba(91, 33, 182, 0.08); }
    .metric strong { display: block; font-size: 1.3rem; margin-top: 8px; color: #5b21b6; }
    .pill { display: inline-block; padding: 8px 12px; border-radius: 999px; background: rgba(255,255,255,0.2); color: white; font-weight: 700; font-size: 0.9rem; }
    .login-box { background: rgba(255,255,255,0.15); padding: 18px; border-radius: 14px; }
    .login-box input, .login-box select { width: 100%; padding: 10px; border-radius: 10px; border: 1px solid #d8c8ff; margin-top: 8px; font-size: 0.95rem; }
    .login-box button { margin-top: 10px; padding: 10px 14px; border: none; border-radius: 10px; background: white; color: #5b21b6; font-weight: 700; cursor: pointer; }
    .bar-row { display: flex; align-items: center; gap: 10px; margin-top: 8px; }
    .bar { flex: 1; background: #f1e9ff; height: 10px; border-radius: 999px; overflow: hidden; }
    .bar > span { display: block; height: 100%; background: linear-gradient(90deg, #5b21b6, #22d3ee); border-radius: 999px; }
    .dashboard-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px; }
    footer { text-align: center; padding: 30px 20px 40px; color: #5b6472; }
    @media (max-width: 900px) { .hero, .grid, .dashboard-grid { grid-template-columns: 1fr; } nav { flex-direction: column; gap: 10px; } }
  </style>
</head>
<body>
  <header>
    <nav>
      <div><strong>BrightPath Analytics</strong></div>
      <div>
        <a href="/">Student Portal</a>
        <a href="/performance">Performance</a>
        <a href="/early-warning">Early Warning</a>
        <a href="/placement-readiness">Placement</a>
        <a href="/overall-dashboard">Overall Dashboard</a>
      </div>
    </nav>
    <div class="hero">
      <div>
        <span class="pill">Student Success Platform</span>
        <h1>Student Portal</h1>
        <p>Select a class and section, review the student count and roll range, and enter the student success experience with creative dashboards.</p>
      </div>
      <div class="card">
        <h3>Student Access</h3>
        <div class="login-box">
          <label>Class</label>
          <select><option>Class 10</option><option>Class 11</option><option>Class 12</option></select>
          <label>Section</label>
          <select><option>A</option><option>B</option><option>C</option></select>
          <label>Roll Number</label>
          <input placeholder="Enter roll number" />
          <button onclick="window.location.href='/overall-dashboard'">Open Dashboard</button>
        </div>
      </div>
    </div>
  </header>

  <section>
    <h2>Quick Overview</h2>
    <div class="grid">
      <div class="metric">Class <strong>{{ selected_class }}</strong></div>
      <div class="metric">Section <strong>{{ selected_section }}</strong></div>
      <div class="metric">Roll Number <strong>{{ roll_range }}</strong></div>
      <div class="metric">Portal Status <strong>Ready</strong></div>
    </div>
  </section>

  <section>
    <h2>Featured Dashboard Views</h2>
    <div class="dashboard-grid">
      <div class="card"><h3>Why am I performing poorly?</h3><div class="bar-row"><span>Trend</span><div class="bar"><span style="width: 72%"></span></div></div></div>
      <div class="card"><h3>AI Success Score</h3><div class="bar-row"><span>AI Readiness</span><div class="bar"><span style="width: 84%"></span></div></div></div>
      <div class="card"><h3>Early Warning Success</h3><div class="bar-row"><span>Recovery</span><div class="bar"><span style="width: 68%"></span></div></div></div>
      <div class="card"><h3>Placement Readiness</h3><div class="bar-row"><span>Readiness</span><div class="bar"><span style="width: 79%"></span></div></div></div>
      <div class="card"><h3>Weak Areas</h3><div class="bar-row"><span>Support Need</span><div class="bar"><span style="width: 61%"></span></div></div></div>
      <div class="card"><h3>Student Digital Twin</h3><div class="bar-row"><span>Profile</span><div class="bar"><span style="width: 88%"></span></div></div></div>
    </div>
  </section>

  <footer>
    BrightPath Analytics • Creative school performance experience.
  </footer>
</body>
</html>
"""


@app.route("/")
def home():
    detailed, _ = get_processed_data()
    student_count = int(detailed["student_id"].nunique())
    selected_class = "Class 10"
    selected_section = "A"
    roll_range = "01 - 40"
    return render_template_string(
        HTML_TEMPLATE,
        student_count=student_count,
        selected_class=selected_class,
        selected_section=selected_section,
        roll_range=roll_range,
    )


@app.route("/performance")
def performance_dashboard():
    detailed, trends = get_processed_data()
    insights = dashboard_insights(detailed, trends)
    kpi = kpi_summary(detailed)
    return render_template_string(
        """
        <!doctype html>
        <html><head><title>Performance Dashboard</title>
        <style>body{font-family:Segoe UI,Arial,sans-serif; background:#f5f9ff; padding:24px;} .card{background:white;padding:20px;border-radius:16px;box-shadow:0 10px 24px rgba(15,76,129,0.1);margin:12px 0;} .grid{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;} .metric{padding:16px;border-radius:12px;background:#f8fbff;border:1px solid #dce9ff;} a{color:#0f4c81;font-weight:700;text-decoration:none;} @media(max-width:900px){.grid{grid-template-columns:1fr;}}</style></head>
        <body>
        <a href="/">← Back to Hub</a>
        <h1>Performance Dashboard</h1>
        <div class="grid">
          <div class="metric">Students <strong>{{ students }}</strong></div>
          <div class="metric">Average Score <strong>{{ avg_score }}</strong></div>
          <div class="metric">Attendance <strong>{{ avg_attendance }}%</strong></div>
          <div class="metric">Pass Rate <strong>{{ pass_rate }}%</strong></div>
        </div>
        <div class="card"><h3>Why am I performing poorly?</h3><p>Attendance dips, weak subject areas, and declining trend signals are the main reasons behind lowered performance.</p></div>
        <div class="card"><h3>Best vs Weakest Subject</h3><p><strong>Best:</strong> {{ best_subject }}<br><strong>Weakest:</strong> {{ weakest_subject }}</p></div>
        <div class="card"><h3>At-Risk and Improving Students</h3><p>{{ at_risk_count }} at-risk students and {{ improving_students }} improving students.</p></div>
        </body></html>
        """,
        students=kpi["n_students"],
        avg_score=f"{kpi['avg_score']:.1f}",
        avg_attendance=f"{kpi['avg_attendance']:.1f}",
        pass_rate=f"{kpi['pass_rate']:.1f}",
        best_subject=insights["best_subject"],
        weakest_subject=insights["weakest_subject"],
        at_risk_count=insights["at_risk_count"],
        improving_students=insights["improving_students"],
    )


@app.route("/early-warning")
def early_warning_dashboard():
    detailed, trends = get_processed_data()
    insights = dashboard_insights(detailed, trends)
    return render_template_string(
        """
        <!doctype html>
        <html><head><title>Early Warning Dashboard</title><style>body{font-family:Segoe UI,Arial,sans-serif;background:#f5f9ff;padding:24px;} .card{background:white;padding:20px;border-radius:16px;box-shadow:0 10px 24px rgba(15,76,129,0.1);margin:12px 0;} .pill{display:inline-block;padding:8px 12px;border-radius:999px;background:#e8f2ff;color:#0f4c81;font-weight:700;} a{color:#0f4c81;font-weight:700;text-decoration:none;}</style></head>
        <body>
        <a href="/">← Back to Hub</a>
        <h1>Early Warning Dashboard</h1>
        <div class="card"><span class="pill">Early Warning Success</span><p>This view focuses on students moving from risk toward stability. It highlights {{ at_risk_count }} students who still need intervention support.</p></div>
        <div class="card"><h3>Intervention Focus</h3><p>Students with low attendance, weak academic trend, and lower scores should receive immediate support.</p></div>
        </body></html>
        """,
        at_risk_count=insights["at_risk_count"],
    )


@app.route("/placement-readiness")
def placement_readiness_dashboard():
    detailed, trends = get_processed_data()
    insights = dashboard_insights(detailed, trends)
    return render_template_string(
        """
        <!doctype html>
        <html><head><title>Placement Readiness Dashboard</title><style>body{font-family:Segoe UI,Arial,sans-serif;background:#f5f9ff;padding:24px;} .card{background:white;padding:20px;border-radius:16px;box-shadow:0 10px 24px rgba(15,76,129,0.1);margin:12px 0;} a{color:#0f4c81;font-weight:700;text-decoration:none;}</style></head>
        <body>
        <a href="/">← Back to Hub</a>
        <h1>Placement Readiness Dashboard</h1>
        <div class="card"><h3>Placement Signal</h3><p>Students with stronger attendance and solid subject performance are better prepared for placements and future opportunities.</p></div>
        <div class="card"><h3>Readiness Score</h3><p>Current readiness is supported by strong performance in {{ best_subject }} and healthy attendance trends.</p></div>
        </body></html>
        """,
        best_subject=insights["best_subject"],
    )


@app.route("/digital-twin")
def digital_twin_dashboard():
    detailed, trends = get_processed_data()
    insights = dashboard_insights(detailed, trends)
    return render_template_string(
        """
        <!doctype html>
        <html><head><title>Student Digital Twin</title><style>body{font-family:Segoe UI,Arial,sans-serif;background:#f5f9ff;padding:24px;} .card{background:white;padding:20px;border-radius:16px;box-shadow:0 10px 24px rgba(15,76,129,0.1);margin:12px 0;} a{color:#0f4c81;font-weight:700;text-decoration:none;}</style></head>
        <body>
        <a href="/">← Back to Student Portal</a>
        <h1>Student Digital Twin</h1>
        <div class="card"><h3>Student Digital Twin</h3><p>This simulated profile summarises the student learning state with a focus on performance, attendance, and support needs.</p></div>
        <div class="card"><h3>Current Profile</h3><p>Best subject: {{ best_subject }}<br>Weakest subject: {{ weakest_subject }}<br>At-risk count: {{ at_risk_count }}</p></div>
        </body></html>
        """,
        best_subject=insights["best_subject"],
        weakest_subject=insights["weakest_subject"],
        at_risk_count=insights["at_risk_count"],
    )


@app.route("/overall-dashboard")
def overall_dashboard():
    detailed, trends = get_processed_data()
    insights = dashboard_insights(detailed, trends)
    kpi = kpi_summary(detailed)
    return render_template_string(
        """
        <!doctype html>
        <html><head><title>Overall Creative Dashboard</title><style>body{font-family:Segoe UI,Arial,sans-serif;background:#f5f9ff;padding:24px;} .card{background:white;padding:20px;border-radius:16px;box-shadow:0 10px 24px rgba(15,76,129,0.1);margin:12px 0;} .grid{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;} .metric{padding:16px;border-radius:12px;background:#f8fbff;border:1px solid #dce9ff;} a{color:#0f4c81;font-weight:700;text-decoration:none;} @media(max-width:900px){.grid{grid-template-columns:1fr;}}</style></head>
        <body>
        <a href="/">← Back to Student Portal</a>
        <h1>Overall Creative Dashboard</h1>
        <div class="grid">
          <div class="metric">Students <strong>{{ students }}</strong></div>
          <div class="metric">Average Score <strong>{{ avg_score }}</strong></div>
          <div class="metric">Attendance <strong>{{ avg_attendance }}%</strong></div>
          <div class="metric">Pass Rate <strong>{{ pass_rate }}%</strong></div>
        </div>
        <div class="card"><h3>Performance Story</h3><p>This overall view brings together performance, attendance, weak areas, and student support health into a single creative dashboard.</p></div>
        <div class="card"><h3>Insights</h3><p>Best subject: {{ best_subject }}<br>Weakest subject: {{ weakest_subject }}<br>At-risk students: {{ at_risk_count }}<br>Improving students: {{ improving_students }}</p></div>
        </body></html>
        """,
        students=kpi["n_students"],
        avg_score=f"{kpi['avg_score']:.1f}",
        avg_attendance=f"{kpi['avg_attendance']:.1f}",
        pass_rate=f"{kpi['pass_rate']:.1f}",
        best_subject=insights["best_subject"],
        weakest_subject=insights["weakest_subject"],
        at_risk_count=insights["at_risk_count"],
        improving_students=insights["improving_students"],
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
