from django.core.management.base import BaseCommand
from api.noticias.scraper_sii import scrape_sii
from api.noticias.scraper_achs import scrape_achs
from api.noticias.scraper_cnn import scrape_cnn
from api.noticias.scraper_dt import scrape_dt

class Command(BaseCommand):
    help = 'Ejecuta los scrapers de noticias'

    def add_arguments(self, parser):
        parser.add_argument(
            '--scraper',
            type=str,
            help='Especifica qué scraper ejecutar: sii, achs, cnn, dt, all',
            default='all'
        )

    def handle(self, *args, **options):
        scraper = options['scraper'].lower()
        
        if scraper == 'sii' or scraper == 'all':
            self.stdout.write('🔄 Ejecutando scraper SII...')
            try:
                scrape_sii()
                self.stdout.write(self.style.SUCCESS('✅ Scraper SII completado'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'❌ Error en scraper SII: {e}'))
        
        if scraper == 'achs' or scraper == 'all':
            self.stdout.write('🔄 Ejecutando scraper ACHS...')
            try:
                scrape_achs()
                self.stdout.write(self.style.SUCCESS('✅ Scraper ACHS completado'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'❌ Error en scraper ACHS: {e}'))
        
        if scraper == 'cnn' or scraper == 'all':
            self.stdout.write('🔄 Ejecutando scraper CNN...')
            try:
                scrape_cnn()
                self.stdout.write(self.style.SUCCESS('✅ Scraper CNN completado'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'❌ Error en scraper CNN: {e}'))
        
        if scraper == 'dt' or scraper == 'all':
            self.stdout.write('🔄 Ejecutando scraper DT...')
            try:
                scrape_dt()
                self.stdout.write(self.style.SUCCESS('✅ Scraper DT completado'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'❌ Error en scraper DT: {e}'))
        
        self.stdout.write(self.style.SUCCESS('🎉 Proceso de scraping completado'))