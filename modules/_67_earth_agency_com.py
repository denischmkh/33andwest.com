
import time

from django.utils import timezone
import requests
from bs4 import BeautifulSoup as BS

from load_django import *
from parser_app.models import Artist

def sync_artists_to_db(current_names):
    existing_artists = Artist.objects.filter(website_link=website_link).order_by('id')
    existing_names = set(existing_artists.values_list('artist_name', flat=True))

    for name in current_names:
        artist, created = Artist.objects.update_or_create(
            artist_name=name,
            website_link=website_link,
            defaults={
                "agency_name": 'earth-agency',
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


today = timezone.now().date()

website_link = 'https://earth-agency.com'
agency_name = 'earth-agency.com'

current_names = set()

url = "https://earth-agency.com/wp/wp-admin/admin-ajax.php"

headers = {
    "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    "connection": "keep-alive",
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    "origin": "https://earth-agency.com",
    "referer": "https://earth-agency.com/artists/",
    "sec-ch-ua": '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
    "x-requested-with": "XMLHttpRequest"
}



def parse67():
    for offset in range(0, 10000, 16):
        data = {
            "action": "get_artists_unfilt",
            "data": f'{{"offset":{offset}}}'
        }

        response = requests.post(url, headers=headers, data=data)
        html = response.json().get('html')
        if not html:
            break
        soup = BS(response.json().get('html'), 'html.parser')
        artists = soup.find_all(name='li', class_='tile-shape-square')
        for artist in artists:
            current_names.add(artist.text.strip())
    res = sync_artists_to_db(current_names=current_names)
    return res

if __name__ == '__main__':
    parse67()