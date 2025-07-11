from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from api.views.cliente_dashboard import ClienteDashboardView
from api.views import NoticiaListView, indicadores_banco_central
from api.views.auth_views import RegistroClienteView
from api.views.documento import DocumentoClienteViewSet
from api.views.mensaje import MensajeClienteViewSet
from api.views.perfil import get_perfil  # 👈 NUEVO

# Router para los ViewSets
router = DefaultRouter()
router.register(r'documentos', DocumentoClienteViewSet, basename='documentos')
router.register(r'mensajes', MensajeClienteViewSet, basename='mensajes')

urlpatterns = [
    path('noticias/', NoticiaListView.as_view(), name='noticias-list'),
    path('indicadores/', indicadores_banco_central, name='indicadores'),

    # JWT
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Rutas protegidas
    path('cliente/dashboard/', ClienteDashboardView.as_view(), name='cliente-dashboard'),
    path('registro/', RegistroClienteView.as_view(), name='registro-cliente'),
    path('perfil/', get_perfil, name='get-perfil'),  # 👈 NUEVA RUTA

    # ViewSets
    path('', include(router.urls)),
]
