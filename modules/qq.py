import time

import requests
from bs4 import BeautifulSoup as BS

url = "https://thedigitaldept.com/wp-admin/admin-ajax.php"

headers = {
    "accept": "*/*",
    "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    "origin": "https://thedigitaldept.com",
    "referer": "https://thedigitaldept.com/talent-roster/?paged=2",
    "sec-ch-ua": '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
    "x-requested-with": "XMLHttpRequest",
}

artists_full = []

for page in range(1, 1000):
    data = {
        "action": "get_posts_by_name",
        "paged": f"{page}",
        "current_url": f"https://thedigitaldept.com/talent-roster/?paged={page}",
    }

    response = requests.post(url, headers=headers, data=data, timeout=15)

    print("Status:", response.status_code)
    html = response.json().get('posts')

    soup = BS(html, 'html.parser')

    artists = [el.text.strip() for el in soup.find_all(name='h3')]

    artists_full.extend(artists)
    if len(artists) == 0:
        break
    time.sleep(10)
for el in artists_full:
    print(el)