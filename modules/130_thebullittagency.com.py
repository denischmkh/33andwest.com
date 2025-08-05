from django.utils import timezone
from selenium import webdriver
import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from load_django import *
from parser_app.models import Artist
import time

today = timezone.now().date()

chrome_options = uc.ChromeOptions()
chrome_options.page_load_strategy = 'eager'
chrome_options.add_argument("--headless=new")  # Лучше использовать new (совместимо с последним Chrome)
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--window-size=1920,1080")

# Создание драйвера
from config import VERSION_MAIN
driver = uc.Chrome(options=chrome_options, version_main=VERSION_MAIN)

url = f"https://thebullittagency.com/roster/"
website_link = 'https://thebullittagency.com'
agency_name = 'thebullittagency.com'

current_names = set()

driver.get(url)
time.sleep(10)

html = driver.page_source

print(html)

soup = BeautifulSoup(html, "html.parser")
#print(soup)
artists = soup.find_all("a",class_="gigwell-roster-artist")
for art in artists:
    text = art.text.strip()
    #print(f"Name: {text}")
    current_names.add(text)

existing_artists = Artist.objects.filter(website_link=website_link).order_by('id')
existing_names = set(existing_artists.values_list('artist_name', flat=True))

for name in current_names:
    artist, created = Artist.objects.get_or_create(
        artist_name=name,
        website_link=website_link,
        defaults={
            'agency_name': 'thebullittagency',
            'date_added': today
        }
    )

missing_names = existing_names - current_names
Artist.objects.filter(artist_name__in=missing_names, date_removed__isnull=True).update(date_removed=today)

print(f"🟢 Synchronization complete. New: {len(current_names - existing_names)}, Missing: {len(missing_names)}")
