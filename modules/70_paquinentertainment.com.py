import time
import threading
from django.utils import timezone
from playwright.sync_api import sync_playwright, Error
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
                'agency_name': 'paquinentertainment',
                'date_added': today
            }
        )

    missing_names = existing_names - current_names
    Artist.objects.filter(artist_name__in=missing_names, date_removed__isnull=True).update(date_removed=today)

    print(f"🟢 Synchronization complete. New: {len(current_names - existing_names)}, Missing: {len(missing_names)}")

today = timezone.now().date()

url = f"https://www.paquinentertainment.com/artists-roster"
website_link = 'https://www.paquinentertainment.com'
agency_name = 'paquinentertainment.com'

current_names = set()

with sync_playwright() as p:

    # Browser initialization
    try:
        browser = p.chromium.launch(
            channel="chrome",
            headless=True,
            args=["--disable-blink-features=AutomationControlled", ]
        )
    except Error as nameError:
        print(f"Unable to launch browser - {nameError}")
        exit()

    # Creating an isolated context
    try:
        context = browser.new_context(
            permissions=["geolocation"],
            geolocation={"latitude": 50.45, "longitude": 30.52},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
            viewport={"width": 1400, "height": 700},
            locale="en-US",
            timezone_id="Europe/Kyiv"
        )
    except Error as nameError:
        print(f"Failed to create context - {nameError}")
        browser.close()
        exit()

        # Go to the Brain page

    page = context.new_page()
    page.goto(url,wait_until="domcontentloaded")
    time.sleep(3)

    previous_height = 0
    while True:
        page.evaluate("window.scrollBy(0, 700)")
        time.sleep(4)

        current_height = page.evaluate("document.body.scrollHeight")

        if current_height == previous_height:
            print("End of page reached, exiting loop")
            break

        previous_height = current_height

    article_all = page.query_selector_all('xpath=//div[@separator=""]/a[@class="artist-roster-mini-card w-inline-block"]')
    for art in article_all:
        text = art.text_content().strip()
        #print(f"Name: {text}")
        current_names.add(text)
    print("\nNumber of names: ", len(current_names))

    browser.close()

    thread = threading.Thread(target=sync_artists_to_db, args=(current_names,))
    thread.start()
    thread.join()