from django.urls import path
from . import views

urlpatterns = [
    # Rutas específicas PRIMERO (antes de las genéricas)
    path('status/', views.obtener_status, name='obtener_status'),
    path('indices/', views.obtener_indices_globales, name='obtener_indices_globales'),
    path('indices/<str:simbolo>/', views.obtener_indice_individual, name='obtener_indice_individual'),
    
    # Rutas genéricas DESPUÉS
    path('', views.obtener_acciones, name='obtener_acciones'),
    path('<str:simbolo>/', views.obtener_accion_individual, name='obtener_accion_individual'),
]