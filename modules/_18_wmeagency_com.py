from pprint import pprint

import requests
from bs4 import BeautifulSoup as BS
from load_django import *
from parser_app.models import Artist
from django.utils import timezone

def parse18():
    website_link = 'https://music.wmeagency.com'
    today = timezone.now().date()

    current_names = set()

    for page in range(1, 100):

        url = f"https://music.wmeagency.com/Music/talents/infinite-scroll-grid/{page}?title=&field_profile_status_value=2&arg1=all"

        headers = {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            "referer": "https://music.wmeagency.com/",
            "sec-ch-ua": '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
            "x-requested-with": "XMLHttpRequest"
        }

        cookies = {
            "business_unit": "Music",
            "SSESS16e2f12c93288028dc80bf21bcbd0b80": "-UB1Oh4-be5UrfDTtb5cL7y6xWSsTWgooERCCnskzIM",
            "has_js": "1",
            "_gid": "GA1.2.2001595359.1754291187",
            "_ga_M8D3K6D88F": "GS2.1.s1754291187$o1$g1$t1754291192$j55$l0$h0",
            "_ga": "GA1.1.1806170073.1754291187",
            "OptanonAlertBoxClosed": "2025-08-04T07:06:32.264Z",
            "OptanonConsent": (
                "isGpcEnabled=0&datestamp=Mon+Aug+04+2025+10%3A06%3A37+GMT%2B0300+"
                "(%D0%92%D0%BE%D1%81%D1%82%D0%BE%D1%87%D0%BD%D0%B0%D1%8F+%D0%95%D0%B2%D1%80%D0%BE%D0%BF%D0%B0%2C+"
                "%D0%BB%D0%B5%D1%82%D0%BD%D0%B5%D0%B5+%D0%B2%D1%80%D0%B5%D0%BC%D1%8F)&version=202309.1.0&"
                "browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=110b507c-d086-4813-911d-8cbc6d96f9a0&"
                "interactionCount=2&landingPath=NotLandingPage&groups=1%3A1%2C2%3A1%2C3%3A1%2C4%3A1&AwaitingReconsent=false"
            )
        }

        response = requests.get(url, headers=headers, cookies=cookies)

        try:
            data = response.json().get('result')
            if isinstance(data, dict):
                for key, value in data.items():
                    for html in value:
                        soup = BS(html, 'html.parser')
                        name = soup.find(name='div', class_='grid-title').text.strip()
                        current_names.add(name)
            else:
                break
        except (ValueError, AttributeError) as e:
            raise Exception(e)

    existing_artists = Artist.objects.filter(website_link=website_link).order_by('id')
    existing_names = set(existing_artists.values_list('artist_name', flat=True))

    for name in current_names:
        artist, created = Artist.objects.update_or_create(
            artist_name=name,
            website_link=website_link,
            defaults={
                "agency_name": "wmeagency",
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