import json

from save_in_db import *

url_n = 'https://www.pitchperfectpr.com/clients/'
website_link = get_website_link(url_n)
agency_name = get_agency_name(url_n)
import gzip
import io


import requests

url = "https://tools.squarewebsites.org/sqs-response/www-pitchperfectpr-com/json/lazy-blog.js"

params = {
    "ver": "2025-07-23T09-3"
}

headers = {
    "accept": "*/*",
    # "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "uk-UA,uk;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6",
    "cache-control": "no-cache",
    "content-type": "application/json;charset=UTF-8",
    "origin": "https://www.pitchperfectpr.com",
    "pragma": "no-cache",
    "referer": "https://www.pitchperfectpr.com/",
    "sec-ch-ua": '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "cross-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
    "x-requested-with": "XMLHttpRequest"
}

response = requests.get(url, headers=headers, params=params)


current_names = set()

try:
    if response.headers.get('Content-Encoding') == 'gzip':
        buf = io.BytesIO(response.content)
        f = gzip.GzipFile(fileobj=buf)
        decoded = f.read().decode('utf-8')
    else:
        decoded = response.text

    print("Decoded text (truncated):", decoded[:500])
    json_respoce = json.loads(decoded)
    items = json_respoce['items']

    for itm in items:
        current_names.add(itm['title'])

    save_in(current_names, website_link, 'pitchperfectpr')

except Exception as e:
    raise Exception(f"Error: {e}")
