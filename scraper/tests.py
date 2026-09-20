from unittest import mock

from django.contrib import admin
from django.test import TestCase
from django.urls import reverse

from .models import Email
from .scraper_engine import normalize_url, scrape_email
from .services import scrape_and_save


class ScrapeEmailTests(TestCase):
    @mock.patch("scraper.scraper_engine.requests.get")
    def test_extracts_emails(self, mock_get):
        def side_effect(url, **kwargs):
            response = mock.MagicMock()
            response.status_code = 200
            response.text = "<h1>Hello</h1><p>Contact sales@corp.org today.</p>"
            return response

        mock_get.side_effect = side_effect
        emails = scrape_email("https://example.com")
        self.assertIn("sales@corp.org", emails)

    @mock.patch("scraper.scraper_engine.requests.get")
    def test_filters_placeholder_domains(self, mock_get):
        def side_effect(url, **kwargs):
            response = mock.MagicMock()
            response.status_code = 404 if "robots.txt" in url else 200
            response.text = "no robots" if "robots.txt" in url else "info@example.com real@acme.io"
            return response

        mock_get.side_effect = side_effect
        emails = scrape_email("https://example.com")
        self.assertIn("real@acme.io", emails)
        self.assertNotIn("info@example.com", emails)

    @mock.patch("scraper.scraper_engine.requests.get", side_effect=OSError("offline"))
    def test_returns_empty_set_on_network_error(self, mock_get):
        self.assertEqual(scrape_email("https://example.com"), set())

    def test_normalize_url_adds_scheme(self):
        self.assertEqual(normalize_url("acme.io"), "https://acme.io")

    def test_normalize_url_rejects_unknown_scheme(self):
        with self.assertRaises(ValueError):
            normalize_url("ftp://acme.io")

    def test_normalize_url_rejects_empty(self):
        with self.assertRaises(ValueError):
            normalize_url("  ")

    @mock.patch("scraper.scraper_engine.requests.get")
    def test_robots_disallow_returns_empty(self, mock_get):
        def side_effect(url, **kwargs):
            response = mock.MagicMock()
            response.status_code = 200
            response.text = "User-agent: *\nDisallow: /"
            return response

        mock_get.side_effect = side_effect
        self.assertEqual(scrape_email("https://acme.io"), set())
        self.assertEqual(mock_get.call_count, 1)

    @mock.patch("scraper.scraper_engine.requests.get")
    def test_robots_allows_when_no_rules(self, mock_get):
        def side_effect(url, **kwargs):
            response = mock.MagicMock()
            response.status_code = 404 if "robots.txt" in url else 200
            response.text = "robots" if "robots.txt" in url else "sales@acme.io"
            return response

        mock_get.side_effect = side_effect
        self.assertEqual(scrape_email("https://acme.io"), {"sales@acme.io"})


class EmailModelTests(TestCase):
    def test_str_is_email(self):
        record = Email.objects.create(url="https://example.com", email="someone@corp.org")
        self.assertEqual(str(record), "someone@corp.org")


class ServicesTests(TestCase):
    @mock.patch("scraper.services.scrape_email")
    def test_scrape_and_save_dedupes(self, mock_scrape):
        Email.objects.create(url="https://example.com", email="keep@acme.io")
        mock_scrape.return_value = {"keep@acme.io", "extra@acme.io"}
        saved = scrape_and_save("https://example.com")
        self.assertEqual(saved, 1)
        self.assertEqual(Email.objects.filter(email="extra@acme.io").count(), 1)

    @mock.patch("scraper.services.scrape_email")
    def test_scrape_many_urls_counts_per_url(self, mock_scrape):
        from .services import scrape_many_urls

        mock_scrape.side_effect = [{"a@acme.io"}, {"b@acme.io", "a@acme.io"}]
        results = scrape_many_urls(["https://one.io", "https://two.io"])
        self.assertEqual(results[0]["saved"], 1)
        self.assertEqual(results[1]["saved"], 1)


class EmailListViewTests(TestCase):
    def test_page_renders(self):
        Email.objects.create(url="https://example.com", email="someone@corp.org")
        response = self.client.get(reverse("email_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "someone@corp.org")

    def test_pagination_shows_first_page(self):
        for index in range(55):
            Email.objects.create(url="https://example.com", email="user{}@acme.io".format(index))
        response = self.client.get(reverse("email_list"))
        self.assertContains(response, "Page 1 of 2")

    def test_search_filters_emails(self):
        Email.objects.create(url="https://example.com", email="x@acme.io")
        Email.objects.create(url="https://example.com", email="y@corp.org")
        response = self.client.get(reverse("email_list"), {"q": "acme"})
        self.assertContains(response, "x@acme.io")
        self.assertNotContains(response, "y@corp.org")

    def test_delete_email(self):
        record = Email.objects.create(url="https://example.com", email="bye@acme.io")
        response = self.client.post(reverse("email_delete", args=[record.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Email.objects.filter(pk=record.pk).count(), 0)


class BulkScrapeViewTests(TestCase):
    @mock.patch("scraper.services.scrape_email")
    def test_bulk_scrape_saves_emails(self, mock_scrape):
        mock_scrape.return_value = {"a@acme.io", "b@acme.io"}
        response = self.client.post(reverse("bulk_scrape"), {"urls": "https://one.io\nhttps://two.io"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Email.objects.count(), 2)


class AdminTests(TestCase):
    def test_email_model_registered(self):
        self.assertTrue(admin.site.is_registered(Email))
