from rest_framework import generics
from .models import Noticia
from .serializers import NoticiaSerializer
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination


class NoticiaPagination(PageNumberPagination):
    page_size = 10  # Puedes ajustar esto

class NoticiaListView(generics.ListAPIView):
    queryset = Noticia.objects.all().order_by('-fecha_scraping')
    serializer_class = NoticiaSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['categoria']
    pagination_class = NoticiaPagination
