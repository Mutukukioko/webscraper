from .models import Email
from .utils import scrape_email


def scrape_and_save(url):
    known = set(Email.objects.values_list("email", flat=True))
    saved = 0
    for email in scrape_email(url):
        if email in known:
            continue
        Email.objects.create(url=url, email=email)
        known.add(email)
        saved += 1
    return saved
