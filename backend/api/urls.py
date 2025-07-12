from django.urls import path, include
from .views import indicadores_banco_central

# Importar vistas de módulos internos
try:
    from .views.noticias import NoticiaListView
except ImportError:
    from .noticias.views import NoticiaListView

app_name = 'api'

urlpatterns = [
    # Noticias
    path('noticias/', NoticiaListView.as_view(), name='noticias-list'),
    
    # Indicadores
    path('indicadores/', indicadores_banco_central, name='indicadores'),
    
    # Acciones - incluir URLs del submódulo
    path('acciones/', include('api.acciones.urls')),
]