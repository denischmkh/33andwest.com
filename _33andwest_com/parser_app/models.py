import datetime

from django.db import models
from django.utils import timezone

# Create your models here.

class Artist(models.Model):
    status = models.CharField(max_length=255, default='new')
    artist_name = models.CharField(max_length=255)
    agency_name = models.CharField( max_length=255, blank=True, null=True)
    website_link = models.CharField( max_length=255, blank=True, null=True)
    date_added = models.DateField(blank=True, null=True)
    date_removed = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.artist_name


class Status(models.Model):
    site = models.CharField(max_length=255, null=False)
    date = models.DateField(default=datetime.date.today)
    status = models.CharField(max_length=255, null=False)

    class Meta:
        verbose_name = "Status"
        verbose_name_plural = "Status"

    def __str__(self):
        return f"{self.site} - {self.status} ({self.date})"