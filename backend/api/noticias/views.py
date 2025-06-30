# api/views/noticias.py

from rest_framework import generics
from rest_framework.filters import OrderingFilter
from rest_framework.pagination import PageNumberPagination
from api.models import Noticia
from api.serializers import NoticiaSerializer

class NoticiaPagination(PageNumberPagination):
    page_size = 10  # Puedes ajustar

class NoticiaListView(generics.ListAPIView):
    serializer_class = NoticiaSerializer
    pagination_class = NoticiaPagination
    filter_backends = [OrderingFilter]

    def get_queryset(self):
        categoria = self.request.query_params.get('categoria')
        queryset = Noticia.objects.all().order_by('-fecha_scraping')

        if categoria:
            queryset = queryset.filter(categoria__iexact=categoria)

        return queryset
