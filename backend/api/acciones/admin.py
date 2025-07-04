# backend/acciones/admin.py
from django.contrib import admin
from .models import Accion

@admin.register(Accion)
class AccionAdmin(admin.ModelAdmin):
    list_display = ['simbolo', 'precio', 'cambio', 'porcentaje_cambio', 'fecha_actualizacion']
    list_filter = ['simbolo', 'fecha_actualizacion']
    search_fields = ['simbolo']
    readonly_fields = ['fecha_actualizacion']
    ordering = ['-fecha_actualizacion']