from django.utils import timezone

from load_django import *
from parser_app.models import Artist

today = timezone.now().date()

url = 'https://www.redlightmanagement.com/roster/'

def get_website_link(url: str):
    split_url = url.replace('//', '**').split('/')[0]
    return split_url.replace('**','//')

def get_agency_name(url: str):
    split_url = url.replace('https://','').replace('http://','').replace('www.','').split('/')[0]
    return split_url

def save_in(current_names,website_link,agency_name):
    existing_artists = Artist.objects.filter(website_link = website_link).order_by('id')
    existing_names = set(existing_artists.values_list('artist_name', flat=True))

    for name in current_names:
        artist, created = Artist.objects.get_or_create(
            artist_name=name,
            website_link = website_link,
            defaults={
                # 'website_link': website_link ,
                'agency_name': agency_name,
                'date_added': today
            }
        )
    
    missing_names = existing_names - current_names
    Artist.objects.filter(artist_name__in=missing_names, date_removed__isnull=True).update(date_removed=today)

    print(f"🟢 Синхронізація завершена. Нові: {len(current_names - existing_names)}, Зниклі: {len(missing_names)}")
    return (len(current_names), len(current_names - existing_names), len(missing_names))


# print(get_agency_name(url))
# print(get_website_link(url))