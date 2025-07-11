from django.contrib import admin
from .models import DocumentoCliente
from .models import MensajeCliente

@admin.register(DocumentoCliente)
class DocumentoClienteAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'descripcion', 'archivo', 'fecha_subida')
    list_filter = ('fecha_subida',)
    search_fields = ('cliente__username', 'descripcion')

@admin.register(MensajeCliente)
class MensajeClienteAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'contenido', 'fecha', 'leido')
    list_filter = ('leido', 'fecha')
    search_fields = ('cliente__username', 'contenido')