import unittest
from unittest.mock import patch
from urllib.error import HTTPError, URLError

from app.monitor import check_url


class MonitorTests(unittest.TestCase):
    @patch("app.monitor.urlopen")
    def test_service_is_up(self, open_url):
        open_url.return_value.__enter__.return_value.status = 200
        self.assertEqual(check_url("http://test/health")["status"], "up")

    @patch("app.monitor.urlopen")
    def test_service_returns_an_error(self, open_url):
        open_url.side_effect = HTTPError("http://test", 503, "Unavailable", {}, None)
        result = check_url("http://test/health")
        self.assertEqual(result["status"], "down")
        self.assertEqual(result["http_status"], 503)

    @patch("app.monitor.urlopen")
    def test_service_cannot_be_reached(self, open_url):
        open_url.side_effect = URLError("Connection refused")
        result = check_url("http://test/health")
        self.assertEqual(result["status"], "down")
        self.assertIsNone(result["http_status"])

    @patch("app.monitor.urlopen")
    def test_request_times_out(self, open_url):
        open_url.side_effect = TimeoutError()
        self.assertEqual(check_url("http://test/health")["status"], "down")
