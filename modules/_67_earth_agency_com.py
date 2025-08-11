import time
import threading
from django.utils import timezone
from playwright.sync_api import sync_playwright, Error
from selenium.webdriver.common.by import By

from load_django import *
from parser_app.models import Artist

def sync_artists_to_db(current_names):
    existing_artists = Artist.objects.filter(website_link=website_link).order_by('id')
    existing_names = set(existing_artists.values_list('artist_name', flat=True))

    for name in current_names:
        artist, created = Artist.objects.get_or_create(
            artist_name=name,
            website_link=website_link,
            defaults={
                'agency_name': 'earth-agency',
                'date_added': today
            }
        )

    missing_names = existing_names - current_names
    Artist.objects.filter(artist_name__in=missing_names, date_removed__isnull=True).update(date_removed=today)

    print(f"🟢 Synchronization complete. New: {len(current_names - existing_names)}, Missing: {len(missing_names)}")
    return (len(current_names), len(current_names - existing_names), len(missing_names))


today = timezone.now().date()

url = f"https://earth-agency.com/artists/?initial="
website_link = 'https://earth-agency.com'
agency_name = 'earth-agency.com'

current_names = set()

def parse67(driver):
    driver.get(url)
    time.sleep(3)

    previous_height = 0
    while True:
        driver.execute_script("window.scrollBy(0, 1500);")
        time.sleep(3)
        current_height = driver.execute_script("return document.body.scrollHeight;")

        if current_height == previous_height:
            break
        previous_height = current_height

    try:
        articles = driver.find_elements(By.XPATH, '//li[@class="artist-tile tile-shape-square"]')
        for art in articles:
            text = art.text.strip()
            current_names.add(text)
    except Exception as e:
        print(f"❌ Ошибка при парсинге элементов: {e}")

    # Синхронизация и возврат результата
    result = sync_artists_to_db(current_names)
    return result