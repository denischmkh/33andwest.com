import tempfile

import undetected_chromedriver
from django.utils import timezone
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
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

url = f"https://www.unitedagents.co.uk/clients/actors?#acting"
website_link = 'https://www.unitedagents.co.uk'
agency_name = 'unitedagents.co.uk'

# options = Options()
# # options.add_argument("--headless")
# options.add_argument("--no-sandbox")
# options.add_argument("--disable-dev-shm-usage")
#
# user_data_dir = tempfile.mkdtemp()
# options.add_argument(f'--user-data-dir={user_data_dir}')
#
# driver = webdriver.Chrome(options=options)
def parse114(driver):
    driver.get(url)
    time.sleep(10)
    try:
        cookie_accept_button = WebDriverWait(driver, 15).until(
                    EC.element_to_be_clickable((By.ID, "cookiescript_accept"))
                )
        cookie_accept_button.click()
    except TimeoutException:
        pass
    time.sleep(2.5)

    current_names = set()
    for page in range(45):
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        artists = soup.find_all("div", class_='client-name')
        for art in artists:
            text = art.text.strip()
            if text:
                #print(f"Name: {text}")
                current_names.add(text)
        try:
            next_page_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//li[@class="next last"]/a[@class="jquery-once-1-processed"]'))
            )
            next_page_button.click()
            time.sleep(2.5)
        except TimeoutException:
            break

    existing_artists = Artist.objects.filter(website_link=website_link).order_by('id')
    existing_names = set(existing_artists.values_list('artist_name', flat=True))

    for name in current_names:
        artist, created = Artist.objects.update_or_create(
            artist_name=name,
            website_link=website_link,
            defaults={
                "agency_name": 'unitedagents',
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

