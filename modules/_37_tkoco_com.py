# //h6[@itemprop="name"]

# http://tkoco.com/roster/

url = 'http://tkoco.com/roster'
website_link = 'http://tkoco.com'
agency_name = 'tkoco'

import cloudscraper
from bs4 import BeautifulSoup
from django.utils import timezone

from load_django import *
from parser_app.models import Artist

today = timezone.now().date()
def parse37():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-En,en;q=0.9,en-US;q=0.8,en;q=0.7'
    }

    current_names = set()
    response = cloudscraper.create_scraper().get(url, headers=headers)

    if not response.ok:
        raise Exception(f'Response error: {response.status_code} - {response.reason}')

    soup = BeautifulSoup(response.text, 'html.parser')

    artists = soup.find_all('h6', itemprop="name")

    for a in artists:
        text = a.get_text(strip=True)
        current_names.add(text)

    existing_artists = Artist.objects.filter(website_link=website_link).order_by('id')
    existing_names = set(existing_artists.values_list('artist_name', flat=True))

    for name in current_names:
        artist, created = Artist.objects.update_or_create(
            artist_name=name,
            website_link=website_link,
            defaults={
                "agency_name": agency_name,
                "date_removed": None,  # оживляем артиста, если был помечен как удалённый
            }
        )
        if created:
            artist.date_added = today
            artist.save(update_fields=["date_added"])

    missing_names = existing_names - current_names
    Artist.objects.filter(artist_name__in=missing_names, date_removed__isnull=True).update(date_removed=today)
    # //div[@id="music"]//a
    print(f"🟢 Синхронізація завершена. Нові: {len(current_names - existing_names)}, Зниклі: {len(missing_names)}")
    return (len(current_names), len(current_names - existing_names), len(missing_names))