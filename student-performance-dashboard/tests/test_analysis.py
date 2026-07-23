import sys
from pathlib import Path
import unittest

sys.path.append(str(Path(__file__).resolve().parent.parent / "src"))

from analysis import dashboard_insights
from data_processing import get_processed_data


class DashboardInsightsTests(unittest.TestCase):
    def test_dashboard_insights_returns_expected_keys(self):
        detailed, trends = get_processed_data()
        insights = dashboard_insights(detailed, trends)

        self.assertIn("best_subject", insights)
        self.assertIn("weakest_subject", insights)
        self.assertIn("at_risk_count", insights)
        self.assertIn("improving_students", insights)
        self.assertGreaterEqual(insights["at_risk_count"], 0)
        self.assertGreaterEqual(insights["improving_students"], 0)


if __name__ == "__main__":
    unittest.main()
