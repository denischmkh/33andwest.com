import time
import threading

import requests
from django.utils import timezone
from playwright.sync_api import sync_playwright, Error
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from bs4 import BeautifulSoup as BS
from load_django import *
from parser_app.models import Artist

headers = {
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    "origin": "https://thedigitaldept.com",
    "referer": "https://thedigitaldept.com/talent-roster/?paged=2",
    "sec-ch-ua": '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
    "x-requested-with": "XMLHttpRequest",
}


def sync_artists_to_db(current_names):
    existing_artists = Artist.objects.filter(website_link=website_link).order_by('id')
    existing_names = set(existing_artists.values_list('artist_name', flat=True))

    for name in current_names:
        artist, created = Artist.objects.update_or_create(
            artist_name=name,
            website_link=website_link,
            defaults={
                "agency_name": 'thedigitaldept',
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

url = "https://thedigitaldept.com/wp-admin/admin-ajax.php"
website_link = 'https://thedigitaldept.com'
agency_name = 'thedigitaldept.com'

current_names = set()


def parse64():
    current_names = set()

    for page in range(1, 1000):
        data = {
            "action": "get_posts_by_name",
            "paged": f"{page}",
            "current_url": f"https://thedigitaldept.com/talent-roster/?paged={page}",
        }

        response = requests.post(url, headers=headers, data=data, timeout=15)

        print("Status:", response.status_code)
        html = response.json().get('posts')

        soup = BS(html, 'html.parser')

        artists = [el.text.strip() for el in soup.find_all(name='h3')]

        for artist in artists:
            current_names.add(artist)
        if len(artists) == 0:
            break
        time.sleep(10)

    # Вызываем синхронизацию напрямую и возвращаем результат
    result = sync_artists_to_db(current_names)
    return result