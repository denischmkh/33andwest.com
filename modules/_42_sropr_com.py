from save_in_db import *

url = 'http://sropr.com/client-roster/'
website_link = get_website_link(url)
agency_name = get_agency_name(url)


import cloudscraper
from bs4 import BeautifulSoup
def parse42():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-En,en;q=0.9,en-US;q=0.8,en;q=0.7'
    }

    current_names = set()
    response = cloudscraper.create_scraper().get(url, headers=headers)


    if not response.ok:
        raise Exception(f'Response error: {response.status_code} - {response.reason}')

    # //div[@class="thumb-title "]

    soup = BeautifulSoup(response.text, 'html.parser')
    # div class="thumb-title"
    artists = soup.find_all('div', class_="thumb-title")

    for h4 in artists:
        text = h4.get_text(strip=True)
        current_names.add(text)


    res = save_in(current_names,website_link,'sropr')
    return res
