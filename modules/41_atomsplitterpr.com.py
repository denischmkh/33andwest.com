from save_in_db import *

url = 'https://atomsplitterpr.com/category/artists/'
website_link = get_website_link(url)
agency_name = get_agency_name(url)

print(f'url: {url}')
print(f'website_link: {website_link}')
print(f'agency_name: {agency_name}')

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
# //div[@class="talent-tiles"]//h4/a
artists = soup.find_all('h3')

for h4 in artists:
    text = h4.get_text(strip=True)
    current_names.add(text)


save_in(current_names,website_link,'atomsplitterpr')
