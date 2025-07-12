from django.urls import path, include
from .views import indicadores_banco_central
from .views.noticias import NoticiaListView

app_name = 'api'

urlpatterns = [
    # Noticias
    path('noticias/', NoticiaListView.as_view(), name='noticias-list'),
    
    # Indicadores
    path('indicadores/', indicadores_banco_central, name='indicadores'),
    
    # Acciones - incluir URLs del submódulo
    path('acciones/', include('api.acciones.urls')),
]