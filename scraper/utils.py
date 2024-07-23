import  requests
from bs4 import BeautifulSoup
import re

def scrape_email(url):
    response=requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    emails = set(re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",soup.text))
    return emails
    