
# https://addition-llc.com/all-talent
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

url = 'https://www.bighassle.com/clients'
website_link = 'https://www.bighassle.com'
agency_name = 'bighassle'

current_names = set()
response = cloudscraper.create_scraper().get(url, headers=headers)

# //div[@class="content"]//div[@class="fluid-engine fe-62dee08016f033f687f9b4d0"]//a

if not response.ok:
    raise Exception(f'Response error: {response.status_code} - {response.reason}')

soup = BeautifulSoup(response.text, 'html.parser')

# //div[@class="content"]//div[@class="fluid-engine fe-62dee08016f033f687f9b4d0"]//a
artists = soup.find('div', class_="content").find('div',class_="fluid-engine fe-62dee08016f033f687f9b4d0" ).find_all('a')

for div in artists:
    text = div.get_text(strip=True)
    current_names.add(text)
        
existing_artists = Artist.objects.filter(website_link = website_link).order_by('id')
existing_names = set(existing_artists.values_list('artist_name', flat=True))

for name in current_names:
    artist, created = Artist.objects.get_or_create(
        artist_name=name,
        website_link = website_link,
        defaults={
            # 'website_link': website_link ,
            'agency_name': agency_name,
            'date_added': today
        }
    )
    
missing_names = existing_names - current_names
Artist.objects.filter(artist_name__in=missing_names, date_removed__isnull=True).update(date_removed=today)

print(f"🟢 Синхронізація завершена. Нові: {len(current_names - existing_names)}, Зниклі: {len(missing_names)}")