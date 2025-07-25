import requests
from save_in_db import *

url = "https://api.gigwell.com/api/agency/379614/roster/embed"

url_n = 'https://www.continentaltouring.us/roster'
website_link = get_website_link(url_n)
agency_name = get_agency_name(url_n)

print(f'url: {url_n}')
print(f'website_link: {website_link}')
print(f'agency_name: {agency_name}')

headers = {
    "accept": "application/json, text/plain, */*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "uk-UA,uk;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6",
    "cache-control": "no-cache",
    "origin": "https://www-continentaltouring-us.filesusr.com",
    "pragma": "no-cache",
    "referer": "https://www-continentaltouring-us.filesusr.com/",
    "sec-ch-ua": '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "cross-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
}

response = requests.get(url, headers=headers)
current_names = set()

# Print status and JSON content
print("Status Code:", response.status_code)
try:
    json_responce = response.json()
    artists = json_responce['data']['artists']

    for a in artists:
        artist = a['title']
        print(artist)
        current_names.add(artist)

    print(len(current_names))
    save_in(current_names,website_link,'continentaltouring')



except Exception:
    print("Response is not in JSON format:")
    print(response.text)
