from django.contrib import admin
from django.urls import path
from scraper.views import scrape_view, email_list_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('scrape/', scrape_view, name='scrape'),
    path('emails/', email_list_view, name='email_list'),
]
