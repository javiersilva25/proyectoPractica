#!/usr/bin/env python

import os
import django

# Configura el entorno Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

# Importa y ejecuta el scraper
from api.noticias.scraper_df import scrape_df

scrape_df()
