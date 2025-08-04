from django.utils import timezone

import requests
from bs4 import BeautifulSoup
from load_django import *
from parser_app.models import Artist

today = timezone.now().date()

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "ru,en-US;q=0.9,en;q=0.8,ja;q=0.7",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "priority": "u=0, i",
    "referer": "https://panoramafirm.pl/lekarz/mazowieckie,,warszawa",
    "sec-ch-ua": "\"Not)A;Brand\";v=\"8\", \"Chromium\";v=\"138\", \"Google Chrome\";v=\"138\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
}

cookies = {
    "PHPSESSID": "8b0834r2um5voomqoo7147jjk3",
    "_ga": "GA1.1.1953643909.1752041975",
    "_fbp": "fb.1.1752041975018.154255081105307490",
    "_clck": "62uc0r%7C2%7Cfxg%7C0%7C2016",
    "_gcl_au": "1.1.366828597.1752041975",
    "cookiefirst-consent": "{\"necessary\":true,\"performance\":true,\"functional\":false,\"advertising\":true,\"timestamp\":1752041974,\"type\":\"category\",\"version\":\"6076f259-200c-4ab7-8465-610082ff5ea0\"}",
    "_clsk": "zeijpc%7C1752042113316%7C3%7C1%7Co.clarity.ms%2Fcollect",
    "_ga_HT6F8M7DR7": "GS2.1.s1752041974$o1$g1$t1752042113$j57$l0$h0",
    "_ga_D2BLTJ927S": "GS2.1.s1752041974$o1$g1$t1752042113$j57$l0$h0"
}

url = f"https://crushmusic.com/"
website_link = 'https://crushmusic.com'
agency_name = 'crushmusic.com'

current_names = set()

response = requests.get(url, headers=headers, cookies=cookies)

if response.status_code == 200:

    soup = BeautifulSoup(response.text, "html.parser")
    artists = soup.find_all("div",class_="Index-gallery-wrapper")
    article = artists[0].find_all("article")

    for art in article:
        text = art.text.strip()
        #print(f"Name: {text}")
        current_names.add(text)

    existing_artists = Artist.objects.filter(website_link=website_link).order_by('id')
    existing_names = set(existing_artists.values_list('artist_name', flat=True))

    for name in current_names:
        artist, created = Artist.objects.get_or_create(
            artist_name=name,
            website_link=website_link,
            defaults={
                'agency_name': 'crushmusic',
                'date_added': today
            }
        )

    missing_names = existing_names - current_names
    Artist.objects.filter(artist_name__in=missing_names, date_removed__isnull=True).update(date_removed=today)

    print(f"🟢 Synchronization complete. New: {len(current_names - existing_names)}, Missing: {len(missing_names)}")

else:
    raise Exception(f'Response error: {response.status_code} - {response.reason}')