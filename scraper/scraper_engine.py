import logging
import re
import urllib.parse

import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

EMAIL_RE = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
TIMEOUT_SECONDS = 10
HEADERS = {"User-Agent": "WebScraper/1.0 email-scraper"}
IGNORED_DOMAINS = {"example.com", "example.org", "example.net"}
ALLOWED_SCHEMES = ("http", "https")


def normalize_url(url):
    url = (url or "").strip()
    if not url:
        raise ValueError("URL is empty")
    if "://" not in url:
        url = "https://" + url
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme not in ALLOWED_SCHEMES or not parsed.netloc:
        raise ValueError("Unsupported URL scheme: {}".format(url))
    return url


def scrape_email(url):
    url = normalize_url(url)
    try:
        response = requests.get(url, timeout=TIMEOUT_SECONDS, headers=HEADERS)
        response.raise_for_status()
    except (requests.RequestException, OSError) as exc:
        logger.warning("Could not fetch %s: %s", url, exc)
        return set()
    soup = BeautifulSoup(response.text, "html.parser")
    return {
        match.lower()
        for match in EMAIL_RE.findall(soup.get_text(" "))
        if match.rsplit("@", 1)[-1].lower() not in IGNORED_DOMAINS
    }
