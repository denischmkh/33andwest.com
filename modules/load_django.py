import os
import sys
import django

# путь до Django-проекта (где manage.py и папка _33andwest_com с settings.py)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "_33andwest_com"))
sys.path.append(BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "_33andwest_com.settings")

django.setup()
