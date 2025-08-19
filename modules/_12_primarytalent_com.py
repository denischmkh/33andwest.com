url_1='https://primarytalent.com/roster/'
url_2='https://primarytalent.com/roster/'

website_link = 'https://primarytalent.com'

# //div[@id="rosterlists"]//li
# //div[@id="alphabetmenu"]//li[not(contains(@class, "active"))]
# //div[@id="alphabetmenu"]//li


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
# options.add_argument("--disable-gpu")
# options.add_argument("--disable-blink-features=AutomationControlled")
# options.add_argument("--disable-notifications")
# options.add_argument("--lang=en-US")
# options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36")

# from config import VERSION_MAIN
# driver = uc.Chrome(options=options, version_main=VERSION_MAIN, use_subprocess=True)
def parse12(driver):
    wait = WebDriverWait(driver, 20)

    driver.get(url_1)
    time.sleep(5)

    # driver.execute_script()
    current_names = set()

    def find_elemets_on_page(locator):
        try:
            return wait.until(EC.presence_of_all_elements_located((By.XPATH,f'{locator}')))
        except (NoSuchElementException,TypeError, TimeoutException, AttributeError) as e:
            raise Exception(f"Error find_elemets_on_page: {e} \n error in :{locator}")

    all_links = []

    ul_alph = find_elemets_on_page('//div[@id="alphabetmenu"]//li/a')

    for i in range(len(ul_alph)-7):
        ul_alph = find_elemets_on_page('//div[@id="alphabetmenu"]//li/a')  # заново

        li = ul_alph[i]
        href_check = li.get_attribute('href')

        if href_check:
            driver.execute_script("arguments[0].click();", li)

            time.sleep(2)

            links = find_elemets_on_page('//div[@id="rosterlists"]//li')

            for link in links:

                link_text = link.text.strip()
                current_names.add(link_text)


    driver.get(url_2)
    time.sleep(5)

    all_links = []

    links = find_elemets_on_page('//div[@id="rosterlists"]//li/a')

    for link in links:

        link_text = link.text.strip()
        current_names.add(link_text)

            # all_links.extend(links)


    existing_artists = Artist.objects.filter(website_link=website_link).order_by('id')
    existing_names = set(existing_artists.values_list('artist_name', flat=True))

    for name in current_names:
        artist, created = Artist.objects.update_or_create(
            artist_name=name,
            website_link=website_link,
            defaults={
                "agency_name": "primarytalent",
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