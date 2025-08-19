import time

from django.utils import timezone
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from load_django import *
from parser_app.models import Artist
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

today = timezone.now().date()
website_link = 'https://www.platformartists.com'
agency_name = 'platformartists.com'
current_names = set()

def parse78(driver):
    current_names = set()

    try:
        driver.get(website_link)
        time.sleep(5)  # Можно заменить на WebDriverWait при необходимости

        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        gallery_div = soup.find("div", id="791131336881775312-gallery")
        if gallery_div:
            artists = gallery_div.find_all("div", recursive=False)
            for art in artists:
                name = art.text.strip()
                if name:
                    current_names.add(name)
        else:
            print("⚠️ Не найден блок с артистами: #791131336881775312-gallery")

    except (TimeoutException, NoSuchElementException) as e:
        print(f"❌ Ошибка при парсинге страницы: {e}")
        return

    existing_artists = Artist.objects.filter(website_link=website_link).order_by('id')
    existing_names = set(existing_artists.values_list('artist_name', flat=True))

    for name in current_names:
        artist, created = Artist.objects.update_or_create(
            artist_name=name,
            website_link=website_link,
            defaults={
                "agency_name": 'platformartists',
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