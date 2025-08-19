url = 'https://www.mbartists.co.uk'
website_link = 'https://www.mbartists.co.uk'

import cloudscraper
from bs4 import BeautifulSoup
from django.utils import timezone

from load_django import *
from parser_app.models import Artist

today = timezone.now().date()
def parse10():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-En,en;q=0.9,en-US;q=0.8,en;q=0.7'
    }
    response = cloudscraper.create_scraper().get(url, headers=headers)

    if not response.ok:
        raise Exception(f'Response error: {response.status_code} - {response.reason}')

    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.select('div#artists a')
    current_names = set()

    for link in set(links):
        n_url = url + link.get('href')

        response = cloudscraper.create_scraper().get(n_url, headers=headers)

        if not response.ok:
            raise Exception(f'Response error: {response.status_code} - {response.reason}')

        soup = BeautifulSoup(response.text, 'html.parser')

        artist_buttons = soup.select('div.content a')

        for a in artist_buttons:
            text = a.get_text(strip=True)

            current_names.add(text)

        print(f"✅ Знайдено {len(current_names)} артистів")

    existing_artists = Artist.objects.filter(website_link=website_link).order_by('id')
    existing_names = set(existing_artists.values_list('artist_name', flat=True))


    for name in current_names:
        artist, created = Artist.objects.update_or_create(
            artist_name=name,
            website_link=website_link,
            defaults={
                "agency_name": "mbartists",
                "date_removed": None,  # оживляем артиста, если был помечен как удалённый
            }
        )
        if created:
            artist.date_added = today
            artist.save(update_fields=["date_added"])

    missing_names = existing_names - current_names
    count = Artist.objects.filter(website_link=website_link, date_removed__isnull=True).exclude(
        artist_name__in=current_names).update(date_removed=today)
    print(count)

    print(f"🟢 Синхронізація завершена. Нові: {len(current_names - existing_names)}, Зниклі: {count}")
    return (len(current_names), len(current_names - existing_names), count)
         