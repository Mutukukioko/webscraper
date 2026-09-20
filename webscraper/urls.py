from django.contrib import admin
from django.urls import include, path

handler404 = "scraper.views.handler404"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("scraper.urls")),
]
