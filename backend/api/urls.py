# api/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from api.views.cliente_dashboard import ClienteDashboardView
from api.views.dashboard_gerente import indicadores_gerente
from api.views.documento import DocumentoClienteViewSet
from api.views.mensaje import MensajeClienteViewSet
from api.views.perfil import get_perfil
from api.views.usuarios import listar_clientes
from api.views.auth_views import RegistroClienteView
from api.views import NoticiaListView, indicadores_banco_central
from api.views.contacto import (
    MensajeContactoCreateView,
    ListaMensajesContacto,
    ActualizarMensajeContacto,
)

# ViewSets
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
    path('registro/', RegistroClienteView.as_view(), name='registro-cliente'),
    path('perfil/', get_perfil, name='get-perfil'),
    path('cliente/dashboard/', ClienteDashboardView.as_view(), name='cliente-dashboard'),
    path('gerente/indicadores/', indicadores_gerente, name='indicadores-gerente'),
    path('usuarios/clientes/', listar_clientes, name='listar-clientes'),

    # Contacto (formulario del sitio)
    path('contacto/', MensajeContactoCreateView.as_view(), name='crear-contacto'),
    path('contacto/mensajes/', ListaMensajesContacto.as_view(), name='listar-contacto'),
    path('contacto/mensajes/<int:pk>/', ActualizarMensajeContacto.as_view(), name='actualizar-contacto'),

    # ViewSets
    path('', include(router.urls)),
]
