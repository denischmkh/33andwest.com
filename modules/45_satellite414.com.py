from save_in_db import *

url = 'https://satellite414.com/representing/?category=music&alphabet=all'
website_link = get_website_link(url)
agency_name = get_agency_name(url)

import cloudscraper
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept-Language': 'en-En,en;q=0.9,en-US;q=0.8,en;q=0.7'
}

current_names = set()
response = cloudscraper.create_scraper().get(url, headers=headers)


if not response.ok:
    raise Exception(f'Response error: {response.status_code} - {response.reason}')


soup = BeautifulSoup(response.text, 'html.parser')
# print(soup.prettify())
# //div[@class="artist-list-container"]//a[@class="open-popup block__link"]
artists = soup.find('div', class_="artist-list-container").find_all('a',class_="open-popup block__link")

for li in artists:
    text = li.get_text(strip=True)
    current_names.add(text)

save_in(current_names,website_link,'satellite414')
