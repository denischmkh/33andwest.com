# https://addition-llc.com/all-talent
import time

import cloudscraper
from bs4 import BeautifulSoup
from django.utils import timezone
from django.utils import timezone
from playwright.sync_api import sync_playwright

from load_django import *
from parser_app.models import Artist
import undetected_chromedriver as uc

today = timezone.now().date()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept-Language': 'en-En,en;q=0.9,en-US;q=0.8,en;q=0.7'
}

url = 'https://beacons.ai/management/addition-talent-management/roster/all-creators'
website_link = 'https://beacons.ai'
agency_name = 'beacons'

current_names = set()
def parse23(driver: uc.Chrome):
    driver.get(url)
    time.sleep(5)
    html = driver.page_source

    soup = BeautifulSoup(html, 'html.parser')

    # //div[@class="summary-title"]
    artists_block = soup.find('div', attrs={'id': 'roster-sheet-creator-list'})
    artists = artists_block.find_all('div', class_="title-lg-strong")

    for div in artists:
        text = div.get_text(strip=True)
        current_names.add(text)


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
    return (len(current_names), len(current_names - existing_names), len(missing_names))