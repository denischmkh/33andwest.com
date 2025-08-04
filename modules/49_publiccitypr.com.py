# //span[@class="sqsrte-text-color--accent"]

from save_in_db import *

url = 'http://publiccitypr.com/public-city-artists'
website_link = get_website_link(url)
agency_name = get_agency_name(url)

import cloudscraper
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept-Language': 'en-En,en;q=0.9,en-US;q=0.8,en;q=0.7'
}

current_names = set()
def get_artists(url):
    response = cloudscraper.create_scraper().get(url, headers=headers)

    if not response.ok:
        raise Exception(f'Response error: {response.status_code} - {response.reason}')

    soup = BeautifulSoup(response.text, 'html.parser')
    # print(soup.prettify())
    # //div[@class="image-slide-title"]
    artists = soup.find_all('div',class_="image-slide-title")

    for span in artists:
        text = span.get_text(strip=True).split('(')[0]
        current_names.add(text)


get_artists(url)
save_in(current_names,website_link,'publiccitypr')
