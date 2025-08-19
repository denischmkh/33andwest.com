from django.utils import timezone
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from load_django import *
from parser_app.models import Artist
import time

today = timezone.now().date()

# chrome_options = Options()
# chrome_options.page_load_strategy = 'eager'
# # chrome_options.add_argument("--headless")
# chrome_options.add_argument("--disable-gpu")
# chrome_options.add_argument("--no-sandbox")
# chrome_options.add_argument("--window-size=1920,1080")

url = f"https://www.lb-agency.net/artists/"
website_link = 'https://www.lb-agency.net'
agency_name = 'lb-agency.net'

current_names = set()

# driver = webdriver.Chrome(options=chrome_options)
def parse104(driver):
    driver.get(url)
    time.sleep(2)

    html = driver.page_source

    soup = BeautifulSoup(html, "html.parser")
    #print(soup)
    artists_all = soup.find("div", class_="summary-item-list sqs-gallery sqs-gallery-design-autogrid")
    artists = soup.find_all("div",class_="artist")
    for art in artists:
        text = art.text.strip()
        if text:
            #print(f"Name: {text}")
            current_names.add(text)

    existing_artists = Artist.objects.filter(website_link=website_link).order_by('id')
    existing_names = set(existing_artists.values_list('artist_name', flat=True))

    for name in current_names:
        artist, created = Artist.objects.update_or_create(
            artist_name=name,
            website_link=website_link,
            defaults={
                "agency_name": 'lb-agency',
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
