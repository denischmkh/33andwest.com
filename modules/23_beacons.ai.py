# https://addition-llc.com/all-talent
import time

import cloudscraper
from bs4 import BeautifulSoup
from django.utils import timezone
from django.utils import timezone
from playwright.sync_api import sync_playwright

from load_django import *
from parser_app.models import Artist

today = timezone.now().date()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept-Language': 'en-En,en;q=0.9,en-US;q=0.8,en;q=0.7'
}

url = 'https://beacons.ai/management/addition-talent-management/roster/all-creators'
website_link = 'https://beacons.ai'
agency_name = 'beacons'

current_names = set()


with sync_playwright() as sp:
    browser = sp.chromium.launch(
        headless=True,
        args=[
            '--disable-blink-features=AutomationControlled',
            '--no-sandbox',
            '--disable-dev-shm-usage',
        ]
    )
    context = browser.new_context(
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
        viewport={'width': 1920, 'height': 1080},
        java_script_enabled=True
    )
    page = context.new_page()

    page.goto(url)
    time.sleep(5)
    html = page.content()

    browser.close()

soup = BeautifulSoup(html, 'html.parser')

# //div[@class="summary-title"]
artists_block = soup.find('div', attrs={'id': 'roster-sheet-creator-list'})
artists = artists_block.find_all('div', class_="title-lg-strong")

for div in artists:
    text = div.get_text(strip=True)
    print(text)
    current_names.add(text)

print(len(current_names))

existing_artists = Artist.objects.filter(website_link=website_link).order_by('id')
existing_names = set(existing_artists.values_list('artist_name', flat=True))

for name in current_names:
    artist, created = Artist.objects.get_or_create(
        artist_name=name,
        website_link=website_link,
        defaults={
            # 'website_link': website_link ,
            'agency_name': 'beacons',
            'date_added': today
        }
    )

missing_names = existing_names - current_names
Artist.objects.filter(artist_name__in=missing_names, date_removed__isnull=True).update(date_removed=today)

print(f"🟢 Синхронізація завершена. Нові: {len(current_names - existing_names)}, Зниклі: {len(missing_names)}")