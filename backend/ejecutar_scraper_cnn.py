#!/usr/bin/env python

import os
import sys
import django

# 🔧 Establece el directorio base del proyecto (ajústalo si es necesario)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

# Configura el entorno Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

# Importa y ejecuta el scraper
from api.noticias.scraper_cnn import scrape_cnn

scrape_cnn()
