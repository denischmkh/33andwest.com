from django.utils import timezone
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from load_django import *
from parser_app.models import Artist
import time

today = timezone.now().date()

chrome_options = Options()
chrome_options.page_load_strategy = 'eager'
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--window-size=1920,1080")

url = f"https://insanity.com/collection/entertainment"
website_link = 'https://insanity.com'
agency_name = 'insanity.com'

current_names = set()

driver = webdriver.Chrome(options=chrome_options)
driver.get(url)
time.sleep(2)

html = driver.page_source

soup = BeautifulSoup(html, "html.parser")
#print(soup)
artists = soup.find_all("div",class_="talent-list-item_name__M_1H9")
for art in artists:
    text = art.text.strip()
    #print(f"Name: {text}")
    current_names.add(text)
print("\nNumber of names: ",len(current_names))

existing_artists = Artist.objects.filter(website_link=website_link).order_by('id')
existing_names = set(existing_artists.values_list('artist_name', flat=True))

for name in current_names:
    artist, created = Artist.objects.get_or_create(
        artist_name=name,
        website_link=website_link,
        defaults={
            'agency_name': 'insanity',
            'date_added': today
        }
    )

missing_names = existing_names - current_names
Artist.objects.filter(artist_name__in=missing_names, date_removed__isnull=True).update(date_removed=today)

print(f"🟢 Synchronization complete. New: {len(current_names - existing_names)}, Missing: {len(missing_names)}")
