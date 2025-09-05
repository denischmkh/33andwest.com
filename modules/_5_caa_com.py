import requests
from django.utils import timezone

url = 'https://www.caa.com/entertainmenttalent/touring/search#all'
website_link = 'https://www.caa.com'

cookies = {
    "visid_incap_1696607": "dN7y+5HTRBq2ZUnnafC/rJGykWgAAAAAQUIPAAAAAADI0kUiObFdf5wVFjvdS9HR",
    "_gcl_au": "1.1.1549685629.1755260886",
    "OptanonAlertBoxClosed": "2025-08-15T12:29:40.570Z",
    "incap_ses_1688_1696607": "Kit1ZKRu7QdXaFOq8P1sF6VUrWgAAAAA1++dKrRP0GSfD6uHBAftEw==",
    "nlbi_1696607": "85BvS8lfESM2vPdf1InhBwAAAACI5MJxBrr63u4WA/nTNktv",
    "caaId": "ImV5SjBlWEFpT2lKS1YxUWlMQ0poYkdjaU9pSkZVelV4TWlKOS5leUowYjJ0bGJrbGtJam9pTmpSRFFUYzNRalF0TVVNMU1DMDBNa0UzTFVFek5EVXROak13UVRrd1FUUkNOVFJGSWl3aWJtRnRaVWxrWlc1MGFXWnBaWElpT2lKQk1FSTBOell6UWkxQk9UQXpMVFJCTVRjdFFrRTNSQzFET1RZMU5VTkdNa1ZFUVRjaUxDSnBaR1Z1ZEdsMGVWQnliM1pwWkdWeUlqb2lZMkZoTFdGd2FUSWdZVzV2Ym5sdGIzVnpJaXdpYm1GdFpTSTZJa0Z1YjI1NWJXOTFjeUJWYzJWeUlpd2ljMk52Y0dVaU9sc2lSVmhVWEZ4QlRrOU9XVTFQVlZNaVhTd2ljR0Z5ZEhsSlpDSTZJa0V3UWpRM05qTkNMVUU1TURNdE5FRXhOeTFDUVRkRUxVTTVOalUxUTBZeVJVUkJOeUlzSW1saGRDSTZNVFF6TVRNNE9ERTBNMzAuam9fZGU5cW4tY0JKX014ekRlalc2SG1Hb3h2blVENHRZNXZXWU1taFJrR2pZQlFEY2o1RWg5M25yS3dELWFwd2Y1VlBOblVqOF84S1gyT3JTM3I5eE5GOHNZNjJNbTJTa1NLVzdRVGR0SXMwTENkMTJhT0tvd3Y1QlZRSUNSNy1WQ2taQjNxNGxPM1lQa0lZd3JmeWJ0RXJKY1AzcmJraWd3TmstQVF0QjAwIg==",
    "OptanonConsent": "isGpcEnabled=0&datestamp=Tue+Aug+26+2025+09%3A31%3A57+GMT%2B0300+(%D0%92%D0%BE%D1%81%D1%82%D0%BE%D1%87%D0%BD%D0%B0%D1%8F+%D0%95%D0%B2%D1%80%D0%BE%D0%BF%D0%B0%2C+%D0%BB%D0%B5%D1%82%D0%BD%D0%B5%D0%B5+%D0%B2%D1%80%D0%B5%D0%BC%D1%8F)&version=6.20.0&isIABGlobal=false&hosts=&consentId=fb4efc17-d092-4542-a8f6-86f53bef1253&interactionCount=2&landingPath=NotLandingPage&groups=C0003%3A0%2CC0004%3A0%2CC0002%3A0%2CC0001%3A1&AwaitingReconsent=false&geolocation=%3B"
}

headers = {
    "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    "priority": "u=1, i",
    "referer": "https://www.caa.com/entertainmenttalent/touring/search",
    "sec-ch-ua": "\"Not;A=Brand\";v=\"99\", \"Google Chrome\";v=\"139\", \"Chromium\";v=\"139\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
    "x-requested-with": "XMLHttpRequest"
}

from bs4 import BeautifulSoup as BS
from load_django import *
from parser_app.models import Artist

def parse5():
    today = timezone.now().date()
    current_names = set()
    for page in range(0, 100):
        url = f'https://www.caa.com/touring/artists_page/all/{page}/a'
        response = requests.get(url=url, cookies=cookies, headers=headers)
        print(response.status_code)
        soup = BS(response.json().get('artist_grid'), 'html.parser')
        artists = [el.text.strip() for el in soup.find_all(name='span', class_='artist-name')]
        if not artists: break
        for artist in artists:
            current_names.add(artist)
    existing_artists = Artist.objects.filter(website_link=website_link).order_by('id')
    existing_names = set(existing_artists.values_list('artist_name', flat=True))

    print(len(current_names))


    for name in current_names:
        artist, created = Artist.objects.update_or_create(
            artist_name=name,
            website_link=website_link,
            defaults={
                "agency_name": "caa",
                "date_removed": None,  # оживляем артиста, если был помечен как удалённый
            }
        )
        if created:
            artist.date_added = today
            artist.save(update_fields=["date_added"])

    missing_names = existing_names - current_names
    count = Artist.objects.filter(website_link=website_link, date_removed__isnull=True).exclude(
        artist_name__in=current_names).update(date_removed=today)

    print(f"🟢 Синхронізація завершена. Нові: {len(current_names - existing_names)}, Зниклі: {count}")
    return (len(current_names), len(current_names - existing_names), count)



if __name__ == '__main__':
    print(parse5())