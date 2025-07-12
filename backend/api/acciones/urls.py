# backend/acciones/urls.py
from django.urls import path
from . import views

app_name = 'acciones'

urlpatterns = [
    path('', views.obtener_acciones, name='obtener_acciones'),
]