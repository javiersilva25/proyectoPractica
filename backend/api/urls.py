# backend/api/urls.py
from django.urls import path
from api.views import NoticiaListView, indicadores_banco_central

urlpatterns = [
    path('noticias/', NoticiaListView.as_view(), name='noticias-list'),
    path("indicadores/", indicadores_banco_central, name='indicadores'),
]