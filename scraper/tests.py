from unittest import mock

from django.test import TestCase

from .models import Email
from .utils import scrape_email


class ScrapeEmailTests(TestCase):
    @mock.patch("scraper.scraper_engine.requests.get")
    def test_extracts_emails(self, mock_get):
        response = mock_get.return_value
        response.status_code = 200
        response.text = "<h1>Hello</h1><p>Contact sales@corp.org today.</p>"
        emails = scrape_email("https://example.com")
        self.assertIn("sales@corp.org", emails)

    @mock.patch("scraper.scraper_engine.requests.get")
    def test_filters_placeholder_domains(self, mock_get):
        response = mock_get.return_value
        response.status_code = 200
        response.text = "Write to info@example.com or real@acme.io"
        emails = scrape_email("https://example.com")
        self.assertIn("real@acme.io", emails)
        self.assertNotIn("info@example.com", emails)

    @mock.patch("scraper.scraper_engine.requests.get", side_effect=OSError("offline"))
    def test_returns_empty_set_on_network_error(self, mock_get):
        self.assertEqual(scrape_email("https://example.com"), set())


class EmailModelTests(TestCase):
    def test_str_is_email(self):
        record = Email.objects.create(url="https://example.com", email="someone@corp.org")
        self.assertEqual(str(record), "someone@corp.org")


class EmailListViewTests(TestCase):
    def test_page_renders(self):
        Email.objects.create(url="https://example.com", email="someone@corp.org")
        response = self.client.get("/scrape/emails/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "someone@corp.org")
