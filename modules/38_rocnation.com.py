import requests



import cloudscraper
from bs4 import BeautifulSoup
from django.utils import timezone

from load_django import *
from parser_app.models import Artist

today = timezone.now().date()

url = "https://www.rocnation.com/wp-admin/admin-ajax.php"
website_link = 'https://www.rocnation.com'
agency_name = 'rocnation'

headers = {
    "Accept-Language": "uk-UA,uk;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6",
    "Cache-Control": "no-cache",
    "Content-Type": "application/x-www-form-urlencoded",
    "Cookie": "_lscache_vary=5a441e04c2b67f7a7daa7006ee0b4e6a; _ga=GA1.2.1416131276.1753086022; _gid=GA1.2.656967783.1753086022; _ga_X73D9F46C8=GS2.2.s1753086022$o1$g1$t1753086280$j60$l0$h0",
    "Origin": "https://www.rocnation.com",
    "Pragma": "no-cache",
    "Referer": "https://www.rocnation.com/music/?paged=4",
    "Sec-Ch-Ua": "\"Not)A;Brand\";v=\"8\", \"Chromium\";v=\"138\", \"Google Chrome\";v=\"138\"",
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "\"Windows\"",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
}
lst = ["athlete","artist"]
current_names = set()

for typr_person in lst:
    payload = {
        "action": "get_posts",
        # "page": "4",
        "post_type": f"{typr_person}",
        "per_page": "100000",
        "order": "ASC",
        "orderby": "title",
        "search": "undefined",
        "isFilter": "undefined",
        "category": "undefined"
    }

    response = requests.post(url, headers=headers, data=payload)
    # print("Response Headers:\n", response.headers)
    # print("Response Body:\n", response.text)

    soup = BeautifulSoup(response.text, 'html.parser')
    # //h3[@class="teaser__heading tick"]
    artists = soup.find_all('h3',class_="teaser__heading tick" )

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
            'agency_name': agency_name,
            'date_added': today
        }
    )
    
missing_names = existing_names - current_names
Artist.objects.filter(artist_name__in=missing_names, date_removed__isnull=True).update(date_removed=today)
# //div[@id="music"]//a
print(f"🟢 Синхронізація завершена. Нові: {len(current_names - existing_names)}, Зниклі: {len(missing_names)}")