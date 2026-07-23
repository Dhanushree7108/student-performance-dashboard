import unittest

from dashboard.app import app


class WebsiteTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_homepage_renders(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)
        self.assertIn("BrightPath Analytics", html)
        self.assertIn("Student Performance Dashboard", html)

    def test_digital_twin_route_renders(self):
        response = self.client.get("/digital-twin")
        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)
        self.assertIn("Student Digital Twin", html)

    def test_creative_dashboard_route_renders(self):
        response = self.client.get("/overall-dashboard")
        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)
        self.assertIn("Overall Creative Dashboard", html)


if __name__ == "__main__":
    unittest.main()
