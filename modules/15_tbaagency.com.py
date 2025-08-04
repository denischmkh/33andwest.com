url = 'https://tbaagency.com/roster/'
website_link = 'https://tbaagency.com'

import cloudscraper
from bs4 import BeautifulSoup
from django.utils import timezone
from django.utils import timezone

from load_django import *
from parser_app.models import Artist

today = timezone.now().date()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept-Language': 'en-En,en;q=0.9,en-US;q=0.8,en;q=0.7'
}

current_names = set()
response = cloudscraper.create_scraper().get(url, headers=headers)

soup = BeautifulSoup(response.text, 'html.parser')
# print(soup.prettify())

if not response.ok:
    raise Exception(f'Response error: {response.status_code} - {response.reason}')
# //a[@class="artistLink"]
artists = soup.select('a.artistLink')
for a in artists:
    text = a.get_text(strip=True)
    current_names.add(text)

existing_artists = Artist.objects.filter(website_link = website_link).order_by('id')
existing_names = set(existing_artists.values_list('artist_name', flat=True))

for name in current_names:
    artist, created = Artist.objects.get_or_create(
        artist_name=name,
        website_link = website_link,
        defaults={
            # 'website_link': website_link ,
            'agency_name': 'tbaagency',
            'date_added': today
        }
    )


missing_names = existing_names - current_names
Artist.objects.filter(website_link=website_link, date_removed__isnull=True).exclude(artist_name__in=current_names).update(date_removed=today)

print(f"🟢 Синхронізація завершена. Нові: {len(current_names - existing_names)}, Зниклі: {len(missing_names)}")