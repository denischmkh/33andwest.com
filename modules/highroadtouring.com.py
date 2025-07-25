url = 'https://www.highroadtouring.com/artists/'

website_link = 'https://www.highroadtouring.com'
# //ul[@class="visual block-grid hide-on-print"]/li


import cloudscraper
from bs4 import BeautifulSoup
from django.utils import timezone

from load_django import *
from parser_app.models import Artist

today = timezone.now().date()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept-Language': 'en-En,en;q=0.9,en-US;q=0.8,en;q=0.7'
}
response = cloudscraper.create_scraper().get(url, headers=headers)
print(response.status_code)
if not response.ok:
    print("❌ Failed to load the page.")
    exit()

soup = BeautifulSoup(response.text, 'html.parser')
artist_buttons = soup.find('ul', class_="visual block-grid hide-on-print")
ul = artist_buttons.find_all('li')
# print(ul)

current_names = set()
for li in ul:
    text = li.get_text(strip=True)
    current_names.add(text)
    print(text)

print(f"✅ Знайдено {len(current_names)} артистів")

existing_artists = Artist.objects.filter(website_link = website_link).order_by('id')
existing_names = set(existing_artists.values_list('artist_name', flat=True))

for name in current_names:
    artist, created = Artist.objects.get_or_create(
        artist_name=name,
        website_link = website_link,

        defaults={
            # 'website_link': 'https://www.33andwest.com/music',
            'agency_name': 'highroadtouring',
            'date_added': today
        }
    )

missing_names = existing_names - current_names
Artist.objects.filter(website_link=website_link, date_removed__isnull=True).exclude(artist_name__in=current_names).update(date_removed=today)

print(f"🟢 Синхронізація завершена. Нові: {len(current_names - existing_names)}, Зниклі: {len(missing_names)}")
         