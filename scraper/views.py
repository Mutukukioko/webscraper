from django.core.paginator import Paginator
from django.shortcuts import redirect, render

from .export import emails_to_csv_response
from .forms import ScrapeForm
from .models import Email
from .services import scrape_and_save


def index_view(request):
    return render(request, "scraper/index.html", {"total": Email.objects.count()})


def scrape_view(request):
    if request.method == "POST":
        form = ScrapeForm(request.POST)
        if form.is_valid():
            scrape_and_save(form.cleaned_data["url"])
            return redirect("email_list")
    else:
        form = ScrapeForm()
    return render(request, "scraper/scrape.html", {"form": form})


def _filtered_emails(request):
    emails = Email.objects.all().order_by("email")
    query = request.GET.get("q", "").strip()
    domain = request.GET.get("domain", "").strip()
    if query:
        emails = emails.filter(email__icontains=query)
    if domain:
        emails = emails.filter(email__iendswith="@" + domain.lstrip("@"))
    return emails, query, domain


def email_list_view(request):
    emails, query, domain = _filtered_emails(request)
    if request.GET.get("export") == "csv":
        return emails_to_csv_response(emails)
    page_obj = Paginator(emails, 50).get_page(request.GET.get("page"))
    return render(request, "scraper/email_list.html", {
        "page_obj": page_obj,
        "q": query,
        "domain": domain,
    })


def delete_email_view(request, pk):
    if request.method == "POST":
        Email.objects.filter(pk=pk).delete()
    return redirect("email_list")


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
