from django.contrib import admin
from django.urls import path

from scraper.views import email_list_view, index_view, scrape_view, stats_view

urlpatterns = [
    path("", index_view, name="index"),
    path("admin/", admin.site.urls),
    path("scrape/", scrape_view, name="scrape"),
    path("emails/", email_list_view, name="email_list"),
    path("stats/", stats_view, name="stats"),
]
