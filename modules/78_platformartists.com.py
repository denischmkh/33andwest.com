from django.utils import timezone
from load_django import *
from parser_app.models import Artist
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

today = timezone.now().date()
website_link = 'https://www.platformartists.com'
agency_name = 'platformartists.com'
current_names = set()

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    try:
        page.goto(website_link, timeout=60000)  # увеличим таймаут
        page.wait_for_selector('div#791131336881775312-gallery', timeout=15000)
        html = page.content()
        soup = BeautifulSoup(html, "html.parser")

        artists = soup.find("div", id="791131336881775312-gallery").find_all("div", recursive=False)

        for art in artists:
            name = art.text.strip()
            current_names.add(name)

        print("\nNumber of names: ", len(current_names))

        existing_artists = Artist.objects.filter(website_link=website_link).order_by('id')
        existing_names = set(existing_artists.values_list('artist_name', flat=True))

        for name in current_names:
            Artist.objects.get_or_create(
                artist_name=name,
                website_link=website_link,
                defaults={
                    'agency_name': 'platformartists',
                    'date_added': today
                }
            )

        missing_names = existing_names - current_names
        Artist.objects.filter(artist_name__in=missing_names, date_removed__isnull=True).update(date_removed=today)

        print(f"🟢 Synchronization complete. New: {len(current_names - existing_names)}, Missing: {len(missing_names)}")

    except Exception as e:
        print("❌ Ошибка при загрузке или парсинге:", e)

    finally:
        browser.close()