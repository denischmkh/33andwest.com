import requests

url = "https://chameleon.unitedtalent.com/speakers/speakers"
website_link = 'https://chameleon.unitedtalent.com'

from load_django import *
from parser_app.models import Artist

from django.utils import timezone
today = timezone.now().date()

headers = {
    "accept": "application/json, text/plain, */*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "uk-UA,uk;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6",
    "authorization": "Bearer undefined", 
    "cache-control": "no-cache",
    "connection": "keep-alive",
    "host": "chameleon.unitedtalent.com",
    "ocp-apim-subscription-key": "a183519df84541f884dd64767e563749",
    "origin": "https://www.utaspeakers.com",
    "pragma": "no-cache",
    "referer": "https://www.utaspeakers.com/",
    "sec-ch-ua": '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "cross-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
}

params = {
    "query": "",
    "categories": "",
    "type": "",
    "order": "fields.lastName",
    # "limit": 600,
    "skip": 0
}

all_links = []
def parse6():
    response = requests.get(url, headers=headers, params=params)


    data_json = response.json()
    data = data_json['data']


    current_names = set()


    for name in data:
        artist_name = name['name'].strip()
        # all_links.append(artist_name)
        current_names.add(artist_name)



    existing_artists = Artist.objects.filter(website_link=website_link, date_removed__isnull=True).order_by('id')
    existing_names = set(existing_artists.values_list('artist_name', flat=True))

    for name in current_names:
        artist, created = Artist.objects.get_or_create(
            artist_name=name,
            website_link = website_link,
            defaults={
                # 'website_link': website_link ,
                'agency_name': 'chameleon.unitedtalent',
                'date_added': today
            }
        )

    missing_names = existing_names - current_names
    Artist.objects.filter(website_link=website_link, date_removed__isnull=True).exclude(artist_name__in=current_names).update(date_removed=today)

    print(f"🟢 Синхронізація завершена. Нові: {len(current_names - existing_names)}, Зниклі: {len(missing_names)}")
    return (len(current_names), len(current_names - existing_names), len(missing_names))
