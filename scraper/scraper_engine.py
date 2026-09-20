import logging
import re
import threading
import time
import urllib.parse

import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

EMAIL_RE = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
TIMEOUT_SECONDS = 10
HEADERS = {"User-Agent": "WebScraper/1.0 email-scraper"}
IGNORED_DOMAINS = {"example.com", "example.org", "example.net"}
ALLOWED_SCHEMES = ("http", "https")
MIN_REQUEST_INTERVAL = 0.5

_throttle_lock = threading.Lock()
_last_request_time = [0.0]


def _throttle():
    with _throttle_lock:
        elapsed = time.time() - _last_request_time[0]
        if elapsed < MIN_REQUEST_INTERVAL:
            time.sleep(MIN_REQUEST_INTERVAL - elapsed)
        _last_request_time[0] = time.time()


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


def allowed_by_robots(url):
    parsed = urllib.parse.urlparse(url)
    robots_url = "{}://{}/robots.txt".format(parsed.scheme, parsed.netloc)
    _throttle()
    try:
        response = requests.get(robots_url, timeout=TIMEOUT_SECONDS, headers=HEADERS)
    except (requests.RequestException, OSError):
        return True
    if response.status_code >= 400:
        return True
    lines = [line for line in (raw.strip().lower() for raw in response.text.splitlines())
             if line and not line.startswith("#")]
    disallowed = [line.split(":", 1)[1].strip() for line in lines if line.startswith("disallow:")]
    path = parsed.path or "/"
    return not any(rule and path.startswith(rule) for rule in disallowed)


def scrape_email(url):
    url = normalize_url(url)
    if not allowed_by_robots(url):
        logger.warning("Blocked by robots.txt: %s", url)
        return set()
    _throttle()
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
