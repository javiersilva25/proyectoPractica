from django.urls import path
from . import views

urlpatterns = [
    path('', views.obtener_acciones, name='obtener_acciones'),
    path('<str:simbolo>/', views.obtener_accion_individual, name='obtener_accion_individual'),
    path('status/', views.obtener_status, name='obtener_status'),
]