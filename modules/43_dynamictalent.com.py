from save_in_db import *

url = 'https://www.dynamictalent.com/artists/'
website_link = get_website_link(url)
agency_name = get_agency_name(url)

print(f'url: {url}')
print(f'website_link: {website_link}')
print(f'agency_name: {agency_name}')

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

options = uc.ChromeOptions()
options.add_argument("--headless=new")  # обязательно!
options.add_argument("--disable-gpu")   # для совместимости
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-notifications")
options.add_argument("--lang=en-US")
options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36")

driver = uc.Chrome(options=options, version_main=137)
wait = WebDriverWait(driver, 20)

driver.get(url)
time.sleep(5)

current_names = set()

def find_elemets_on_page(locator):
    try:
        return wait.until(EC.presence_of_all_elements_located((By.XPATH,f'{locator}')))
    except (NoSuchElementException,TypeError, TimeoutException, AttributeError) as e:
        print(f"Error find_elemets_on_page: {e} \n error in :{locator}")
        return None
    

for _ in range(8):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

# //ul[@class="wpg-list-items"]/li/a
all_links = driver.find_elements(By.XPATH, '//ul[@class="wpg-list-items"]/li/a')

for link in all_links:
    link_text = link.text.strip()
    print(link_text)
    current_names.add(link_text)   

print(len(current_names))
save_in(current_names,website_link,agency_name)
