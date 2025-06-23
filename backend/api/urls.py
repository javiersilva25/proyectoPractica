from django.urls import path
from .noticias.views import NoticiasView

urlpatterns = [
    path('noticias/', NoticiasView.as_view(), name='noticias'),
]
