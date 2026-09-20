from django.shortcuts import redirect, render

from .export import emails_to_csv_response
from .forms import ScrapeForm
from .models import Email
from .utils import scrape_email


def _known_emails():
    return set(Email.objects.values_list("email", flat=True))


def scrape_view(request):
    if request.method == "POST":
        form = ScrapeForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data["url"]
            known = _known_emails()
            for email in scrape_email(url):
                if email in known:
                    continue
                Email.objects.create(url=url, email=email)
                known.add(email)
            return redirect("email_list")
    else:
        form = ScrapeForm()
    return render(request, "scraper/scrape.html", {"form": form})


def email_list_view(request):
    emails = Email.objects.all()
    if request.GET.get("export") == "csv":
        return emails_to_csv_response(emails)
    return render(request, "scraper/email_list.html", {"emails": emails})


def stats_view(request):
    emails = Email.objects.all()
    domains = {}
    for email in emails:
        domain = email.email.rsplit("@", 1)[-1].lower()
        domains[domain] = domains.get(domain, 0) + 1
    top_domains = sorted(domains.items(), key=lambda item: item[1], reverse=True)[:10]
    context = {
        "total": emails.count(),
        "url_count": emails.values("url").distinct().count(),
        "domain_count": len(domains),
        "top_domains": top_domains,
    }
    return render(request, "scraper/stats.html", context)
