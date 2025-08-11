from django.contrib import admin
from .models import Artist, Status
from django.utils.translation import gettext_lazy as _
from datetime import datetime


class DateAddedFilter(admin.SimpleListFilter):
    title = _('Date added')
    parameter_name = 'date_added'

    def lookups(self, request, model_admin):
        dates = Artist.objects.exclude(date_added__isnull=True).order_by('date_added') \
            .values_list('date_added', flat=True).distinct()
        return [(date.isoformat(), date.strftime('%d.%m.%Y')) for date in dates]

    def queryset(self, request, queryset):
        value = self.value()
        if value:
            return queryset.filter(date_added=value)
        return queryset


class DateRemovedFilter(admin.SimpleListFilter):
    title = _('Deletion date')
    parameter_name = 'date_removed'

    def lookups(self, request, model_admin):
        dates = Artist.objects.exclude(date_removed__isnull=True).order_by('date_removed') \
            .values_list('date_removed', flat=True).distinct()
        return [(date.isoformat(), date.strftime('%d.%m.%Y')) for date in dates]

    def queryset(self, request, queryset):
        value = self.value()
        if value:
            return queryset.filter(date_removed=value)
        return queryset


class AgencyNameFilter(admin.SimpleListFilter):
    title = _('Agency')
    parameter_name = 'agency_name'

    def lookups(self, request, model_admin):
        agencies = (
            Artist.objects
            .order_by('agency_name')  # сортировка по алфавиту
            .values_list('agency_name', flat=True)
            .distinct()
        )
        return [(agency, agency) for agency in agencies if agency]

    def queryset(self, request, queryset):
        value = self.value()
        if value:
            return queryset.filter(agency_name=value)
        return queryset


class ArtistAdmin(admin.ModelAdmin):
    list_display = ["artist_name", "agency_name", "date_added", "date_removed", "website_link"]
    list_filter = [DateAddedFilter, DateRemovedFilter, AgencyNameFilter]
    search_fields = ["artist_name", "agency_name"]
    ordering = ['agency_name']


admin.site.register(Artist, ArtistAdmin)

class StatusAdmin(admin.ModelAdmin):
    list_display = ['site', 'date', 'status']
    ordering = ['site']

admin.site.register(Status, StatusAdmin)