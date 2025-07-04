# backend/acciones/models.py
from django.db import models
from django.utils import timezone

class Accion(models.Model):
    simbolo = models.CharField(max_length=10)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    cambio = models.DecimalField(max_digits=10, decimal_places=2)
    porcentaje_cambio = models.CharField(max_length=20)
    fecha_actualizacion = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-fecha_actualizacion']
        verbose_name = 'Acción'
        verbose_name_plural = 'Acciones'
    
    def __str__(self):
        return f"{self.simbolo} - ${self.precio}"