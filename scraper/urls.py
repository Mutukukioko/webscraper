from django.contrib import admin
from django.urls import path

from scraper.views import (
    bulk_scrape_view,
    delete_email_view,
    domain_detail_view,
    email_list_view,
    index_view,
    scrape_view,
    stats_view,
)

urlpatterns = [
    path("", index_view, name="index"),
    path("admin/", admin.site.urls),
    path("scrape/", scrape_view, name="scrape"),
    path("scrape/bulk/", bulk_scrape_view, name="bulk_scrape"),
    path("emails/", email_list_view, name="email_list"),
    path("emails/<int:pk>/delete/", delete_email_view, name="email_delete"),
    path("domains/<str:domain>/", domain_detail_view, name="domain_detail"),
    path("stats/", stats_view, name="stats"),
]
