from pprint import pprint

import requests
import pdfplumber
from django.utils import timezone

from load_django import *
from parser_app.models import Artist

website_link = 'https://clewisgroup.com/roster'
agency_name = 'clewisgroup'

today = timezone.now().date()

def parse143():
    try:
        url = "https://img1.wsimg.com/blobby/go/fdfd814d-d08c-47e3-b4cd-77afd89ca8f9/CLG%20ROSTER%202025.pdf"
        response = requests.get(url)
        with open("file.pdf", "wb") as f:
            f.write(response.content)

        # Открываем PDF
        with pdfplumber.open("file.pdf") as pdf:
            page = pdf.pages[0]
            chars = page.chars

        # Сортируем символы по вертикали и горизонтали
        chars_sorted = sorted(chars, key=lambda x: (x['top'], x['x0']))

        left_column = []
        right_column = []

        current_line_left = []
        current_line_right = []

        for i, char in enumerate(chars_sorted):
            if char['x0'] < 300:
                current_line_left.append(char['text'])
            else:
                current_line_right.append(char['text'])

            # Проверяем, есть ли следующий символ
            if i + 1 < len(chars_sorted):
                next_char = chars_sorted[i + 1]
                if abs(next_char['top'] - char['top']) > 2:  # новая строка
                    left_column.append(''.join(current_line_left).strip())
                    right_column.append(''.join(current_line_right).strip())
                    current_line_left = []
                    current_line_right = []
            else:
                # Последний символ — сохраняем текущую строку
                left_column.append(''.join(current_line_left).strip())
                right_column.append(''.join(current_line_right).strip())

        left_column = [name for name in left_column if '@' not in name and not any(c.isdigit() for c in name)][2:]
        right_column = [name for name in right_column if '@' not in name and not any(c.isdigit() for c in name)][2:-1]

        current_names = set(left_column + right_column)
        existing_artists = Artist.objects.filter(website_link=website_link).order_by('id')
        existing_names = set(existing_artists.values_list('artist_name', flat=True))

        for name in current_names:
            artist, created = Artist.objects.update_or_create(
                artist_name=name,
                website_link=website_link,
                defaults={
                    "agency_name": 'clewisgroup',
                    "date_removed": None,
                }
            )
            if created:
                artist.date_added = today
                artist.save(update_fields=["date_added"])

        count = Artist.objects.filter(website_link=website_link, date_removed__isnull=True).exclude(
            artist_name__in=current_names).update(date_removed=today)
        print(count)

        print(f"🟢 Синхронізація завершена. Нові: {len(current_names - existing_names)}, Зниклі: {count}")
        return (len(current_names), len(current_names - existing_names), count)
    except Exception :
        raise Exception(f'Response error: {response.status_code} - {response.reason}')

