from django.core.management.base import BaseCommand
from api.models import Noticia
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Limpia noticias antiguas'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dias',
            type=int,
            default=30,
            help='Eliminar noticias más antiguas que X días (default: 30)',
        )

    def handle(self, *args, **options):
        dias = options['dias']
        fecha_limite = datetime.now() - timedelta(days=dias)
        
        noticias_antiguas = Noticia.objects.filter(fecha_scraping__lt=fecha_limite)
        count = noticias_antiguas.count()
        
        if count > 0:
            noticias_antiguas.delete()
            self.stdout.write(
                self.style.SUCCESS(f'🗑️ Se eliminaron {count} noticias antiguas')
            )
        else:
            self.stdout.write('ℹ️ No hay noticias antiguas para eliminar')