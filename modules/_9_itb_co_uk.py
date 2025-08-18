import requests

from load_django import *
from parser_app.models import Artist

from django.utils import timezone
today = timezone.now().date()

def parse9():
    url = "https://www.itb.co.uk/artists?format=page-context"
    website_link = 'https://www.itb.co.uk'

    params = {
        "format": "page-context",
        # "cache": "2025-07-19T13-4",
        # "offset" : 1712246174530

    }

    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "uk-UA,uk;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6",
        "cache-control": "no-cache",
        "cookie": (
            "crumb=BdaguLlLjwVcM2U3NmZhYmJlZGYxZTkyOGZkMjVhZWUxNmYzOGJm; "
            "ss_cvr=fcecb71c-7309-41b6-9f89-09011747ce81|1752929503213|1752929503213|1752929503213|1; "
            "ss_cvt=1752929503213"
        ),
        "pragma": "no-cache",
        "referer": "https://www.itb.co.uk/artists?",
        "sec-ch-ua": '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-model": '""',
        "sec-ch-ua-platform": '"Windows"',
        "sec-ch-ua-platform-version": '"19.0.0"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/138.0.0.0 Safari/537.36"
        )
    }
    response = requests.get(url, headers=headers, params=params)

    current_names = set()

    while True:

        data_json = response.json()
        data = data_json['items']

        for name in data:
            current_names.add(name['title'].strip())

        data_pagination = None

        try:
            data_pagination = data_json['pagination']['nextPageOffset']
        except KeyError as e:
            print(e)
            break

        params = {
            "format": "page-context",
            # "cache": "2025-07-19T13-4",
            "offset" : data_pagination

        }
        response = requests.get(url, headers=headers, params=params)

    existing_artists = Artist.objects.filter(website_link=website_link).order_by('id')
    existing_names = set(existing_artists.values_list('artist_name', flat=True))

    for name in current_names:
        artist, created = Artist.objects.update_or_create(
            artist_name=name,
            website_link=website_link,
            defaults={
                "agency_name": "itb.co",
                "date_removed": None,  # оживляем артиста, если был помечен как удалённый
            }
        )
        if created:
            artist.date_added = today
            artist.save(update_fields=["date_added"])

    missing_names = existing_names - current_names
    Artist.objects.filter(website_link=website_link, date_removed__isnull=True).exclude(artist_name__in=current_names).update(date_removed=today)

    print(f"🟢 Синхронізація завершена. Нові: {len(current_names - existing_names)}, Зниклі: {len(missing_names)}")
    return (len(current_names), len(current_names - existing_names), len(missing_names))