# urls.py
from django.urls import path
from . import views

app_name = 'acciones'

urlpatterns = [
    path('', views.obtener_acciones, name='obtener_acciones'),
    path('<str:simbolo>/', views.obtener_accion_individual, name='obtener_accion_individual'),
]