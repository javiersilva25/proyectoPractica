from rest_framework import generics
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from api.models import Noticia
from api.serializers import NoticiaSerializer


class NoticiaPagination(PageNumberPagination):
    page_size = 10  # Puedes ajustar esto

class NoticiaListView(generics.ListAPIView):
    queryset = Noticia.objects.all().order_by('-fecha_scraping')
    serializer_class = NoticiaSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['categoria']
    pagination_class = NoticiaPagination
