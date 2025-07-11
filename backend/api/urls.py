# api/urls.py
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from api.views.cliente_dashboard import ClienteDashboardView
from api.views import NoticiaListView, indicadores_banco_central
from api.views.auth_views import RegistroClienteView

urlpatterns = [
    path('noticias/', NoticiaListView.as_view(), name='noticias-list'),
    path('indicadores/', indicadores_banco_central, name='indicadores'),

    # JWT
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Ruta protegida
    path('cliente/dashboard/', ClienteDashboardView.as_view(), name='cliente-dashboard'),
    path('registro/', RegistroClienteView.as_view(), name='registro-cliente'),
]
