from django.db import models

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
