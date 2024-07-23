from django.shortcuts import render, redirect
# Create your views here.
from .utils import scrape_email
from .models import Email
from .forms import ScrapeForm

def scrape_view(request):
    if request.method == 'POST':
        form = ScrapeForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            emails = scrape_email(url)
            for email in emails:
                Email.objects.create(url=url, email=email)
            return redirect('email_list')
    else:
        form = ScrapeForm()
    return render(request, 'scraper/scrape.html',{'form': form})

def email_list_view(request):
    emails = Email.objects.all()
    return render(request, 'scraper/email_list.html', {'emails': emails})