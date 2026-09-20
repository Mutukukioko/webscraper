import logging
import re

import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

EMAIL_RE = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
TIMEOUT_SECONDS = 10
HEADERS = {"User-Agent": "WebScraper/1.0 email-scraper"}
IGNORED_DOMAINS = {"example.com", "example.org", "example.net"}


def scrape_email(url):
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
