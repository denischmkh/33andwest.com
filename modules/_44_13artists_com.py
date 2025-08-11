from save_in_db import *

url = 'https://www.13artists.com/artist-roster/'
website_link = get_website_link(url)
agency_name = get_agency_name(url)


import cloudscraper
from bs4 import BeautifulSoup
def parse44():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-En,en;q=0.9,en-US;q=0.8,en;q=0.7'
    }

    current_names = set()
    response = cloudscraper.create_scraper().get(url, headers=headers)


    if not response.ok:
        raise Exception(f'Response error: {response.status_code} - {response.reason}')


    soup = BeautifulSoup(response.text, 'html.parser')
    # //div[@class="vc_row wpb_row section vc_row-fluid vc_inner "]//li/a
    artists = soup.find_all('ul', class_="lcp_catlist")
    # .find_all('li')
    for ul in artists:
        li = ul.find_all('li')
        for a in li:
            text = a.find('a').get_text(strip=True)
            current_names.add(text)

    res = save_in(current_names,website_link,'13artists')
    return res
