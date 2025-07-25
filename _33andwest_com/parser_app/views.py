from rest_framework import viewsets, filters
from .models import Artist
from .serializers import ArtistSerializer

class ArtistViewSet(viewsets.ModelViewSet):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer

    # 🔍 Добавляем поиск и фильтрацию
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['artist_name', 'agency_name', 'status']
    ordering_fields = ['date_added', 'artist_name']