url = 'https://www.loaded.gg/creators/'
website_link = 'https://www.loaded.gg'
agency_name = 'loaded'

import re
import time
import random
from selenium import webdriver

import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException,NoSuchAttributeException, InvalidArgumentException,TimeoutException
from django.utils import timezone

from load_django import *
from parser_app.models import Artist

today = timezone.now().date()

# options = uc.ChromeOptions()
# # options.add_argument("--headless=new")  # обязательно!
# options.add_argument("--disable-gpu")   # для совместимости
# options.add_argument("--disable-blink-features=AutomationControlled")
# options.add_argument("--disable-notifications")
# options.add_argument("--lang=en-US")
# options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36")
#
# driver = uc.Chrome(options=options, version_main=137)
def parse24(driver):
    wait = WebDriverWait(driver, 20)

    driver.get(url)
    time.sleep(5)

    current_names = set()

    def find_elemets_on_page(locator):
        try:
            return wait.until(EC.presence_of_all_elements_located((By.XPATH,f'{locator}')))
        except (NoSuchElementException,TypeError, TimeoutException, AttributeError) as e:
            raise Exception(f"Error find_elemets_on_page: {e} \n error in :{locator}")

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

    all_links = driver.find_elements(By.XPATH, '//ul[@id="result_creators"]/li')

    for link in all_links:
        link_text = link.text.strip()
        current_names.add(link_text)

    existing_artists = Artist.objects.filter(website_link=website_link).order_by('id')
    existing_names = set(existing_artists.values_list('artist_name', flat=True))

    for name in current_names:
        artist, created = Artist.objects.update_or_create(
            artist_name=name,
            website_link=website_link,
            defaults={
                "agency_name": agency_name,
                "date_removed": None,  # оживляем артиста, если был помечен как удалённый
            }
        )
        if created:
            artist.date_added = today
            artist.save(update_fields=["date_added"])

    missing_names = existing_names - current_names
    Artist.objects.filter(artist_name__in=missing_names, date_removed__isnull=True).update(date_removed=today)

    print(f"🟢 Синхронізація завершена. Нові: {len(current_names - existing_names)}, Зниклі: {len(missing_names)}")
    return (len(current_names), len(current_names - existing_names), len(missing_names))