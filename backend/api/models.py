from django.db import models
from django.conf import settings


class Noticia(models.Model):
    CATEGORIAS = [
        ('nacional', 'Nacional'),
        ('internacional', 'Internacional'),
        ('tributaria', 'Tributaria (SII)'),
        ('bcentral', 'Banco Central'),
        ('achs', 'ACHS'),
        ('dtrabajo', 'Dirección del Trabajo'),
        ('politica', 'Política'),
        ('tecnologia', 'Tecnología'),
        ('economica', 'Económica'),
        ('negocios', 'Negocios'),
        ('empresas', 'Empresas'),
        ('mercados', 'Mercados'),
        ('otros', 'Otros'),
        ('laboral', 'Laboral'),
    ]

    titulo = models.CharField(max_length=255)
    url = models.URLField(unique=True)
    categoria = models.CharField(max_length=50, choices=CATEGORIAS)
    fuente = models.CharField(max_length=100)
    fecha_publicacion = models.DateField(null=True, blank=True)
    fecha_scraping = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.categoria}] {self.titulo}"


class DocumentoCliente(models.Model):
    cliente = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='documentos')
    descripcion = models.CharField(max_length=255)
    archivo = models.FileField(upload_to='documentos_clientes/')
    fecha_subida = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Documento de {self.cliente.username} - {self.descripcion}"


class DocumentoLeido(models.Model):
    documento = models.ForeignKey(DocumentoCliente, on_delete=models.CASCADE, related_name='lecturas')
    cliente = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    revisado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('documento', 'cliente')


class MensajeCliente(models.Model):
    cliente = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    contenido = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    leido = models.BooleanField(default=False)
