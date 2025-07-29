#!/usr/bin/env python
import os
import django
import re
import html
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime

# Configurar Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

from api.models import Noticia

def categorizar_enlace(url: str) -> str | None:
    """Categoriza una URL según palabras clave"""
    url_lower = url.lower()
    if any(palabra in url_lower for palabra in ["mundo", "internacional", "global"]):
        return "internacional"
    elif any(palabra in url_lower for palabra in ["politica", "gobierno", "elecciones"]):
        return "politica"
    elif any(palabra in url_lower for palabra in ["economia", "negocios", "financiero", "mercado"]):
        return "economica"
    elif any(palabra in url_lower for palabra in ["tributaria", "impuesto", "sii"]):
        return "tributaria"
    elif any(palabra in url_lower for palabra in ["laboral", "trabajo", "sindical"]):
        return "laboral"
    return "economica"  # Categoría por defecto

def scrape_sii():
    """Scraper del SII"""
    print("🔎 Scrapeando SII...")
    BASE_URL = "https://www.sii.cl/noticias/2025/"
    FULL_URL = BASE_URL + "index.html"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        resp = requests.get(FULL_URL, headers=headers, timeout=15)
        resp.raise_for_status()
    except Exception as e:
        print(f"❌ Error SII: {e}")
        return 0
    
    match = re.search(r"arrayIndice\s*=\s*(\[[^\]]+\])", resp.text, re.DOTALL)
    if not match:
        print("❌ No se encontró array de noticias SII")
        return 0
    
    items = re.findall(r"\['(.*?)',\s*'(.*?)',\s*'(.*?)',\s*'(.*?)'\]", match.group(1))
    insertadas = 0
    
    for id_noticia, fecha, titulo_html, img in items:
        url = urljoin(BASE_URL, f"{id_noticia}.htm")
        titulo = html.unescape(titulo_html).strip()
        
        try:
            fecha_obj = datetime.strptime(fecha.strip(), "%d-%m-%Y").date()
        except:
            try:
                fecha_obj = datetime.strptime(fecha.strip(), "%d/%m/%Y").date()
            except:
                fecha_obj = None
        
        _, creado = Noticia.objects.get_or_create(
            url=url,
            defaults={
                "titulo": titulo,
                "categoria": "tributaria",
                "fuente": "SII",
                "fecha_publicacion": fecha_obj,
            }
        )
        if creado:
            insertadas += 1
    
    print(f"✅ SII: {insertadas} noticias insertadas")
    return insertadas

def scrape_achs():
    """Scraper de ACHS"""
    print("🔎 Scrapeando ACHS...")
    URL = "https://www.achs.cl/centro-de-noticias"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        resp = requests.get(URL, headers=headers, timeout=15)
        resp.raise_for_status()
    except Exception as e:
        print(f"❌ Error ACHS: {e}")
        return 0
    
    soup = BeautifulSoup(resp.text, "html.parser")
    noticias = soup.select("div.box-not")
    insertadas = 0
    
    for box in noticias:
        try:
            h4 = box.select_one("h4")
            enlace_tag = box.select_one("a[href]")
            
            if not (h4 and enlace_tag):
                continue
            
            titulo = html.unescape(h4.get_text(strip=True))
            enlace = enlace_tag["href"].strip()
            
            _, creado = Noticia.objects.get_or_create(
                url=enlace,
                defaults={
                    "titulo": titulo,
                    "categoria": "laboral",
                    "fuente": "ACHS",
                }
            )
            if creado:
                insertadas += 1
        except Exception as e:
            continue
    
    print(f"✅ ACHS: {insertadas} noticias insertadas")
    return insertadas

def scrape_cnn():
    """Scraper de CNN Español"""
    print("🔎 Scrapeando CNN...")
    url = "https://cnnespanol.cnn.com/mundo"
    base_url = "https://cnnespanol.cnn.com"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        resp = requests.get(url, headers=headers, timeout=15)
        resp.raise_for_status()
    except Exception as e:
        print(f"❌ Error CNN: {e}")
        return 0
    
    soup = BeautifulSoup(resp.text, "html.parser")
    insertadas = 0
    
    # Buscar diferentes selectores de artículos
    selectores = [
        "a.container__link--type-article",
        "a[href*='/2025/']",
        ".cd__headline a"
    ]
    
    articulos = []
    for selector in selectores:
        articulos.extend(soup.select(selector))
    
    for a in articulos[:30]:  # Limitar a 30 artículos
        try:
            enlace = a.get("href")
            if not enlace or not enlace.startswith("/202"):
                continue
            
            # Buscar título en diferentes elementos
            titulo_elem = (a.select_one(".container__headline-text") or 
                          a.select_one(".cd__headline-text") or 
                          a)
            
            if not titulo_elem:
                continue
            
            titulo = titulo_elem.get_text(strip=True)
            if not titulo or len(titulo) < 10:
                continue
            
            url_completo = base_url + enlace
            categoria = categorizar_enlace(enlace)
            
            _, creado = Noticia.objects.get_or_create(
                url=url_completo,
                defaults={
                    "titulo": titulo,
                    "categoria": categoria,
                    "fuente": "CNN Español",
                }
            )
            if creado:
                insertadas += 1
        except Exception as e:
            continue
    
    print(f"✅ CNN: {insertadas} noticias insertadas")
    return insertadas

def scrape_dt():
    """Scraper Dirección del Trabajo"""
    print("🔎 Scrapeando Dirección del Trabajo...")
    BASE_URL = "https://www.dt.gob.cl/portal/1627/"
    FULL_URL = urljoin(BASE_URL, "w3-channel.html")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        resp = requests.get(FULL_URL, headers=headers, timeout=15)
        resp.raise_for_status()
    except Exception as e:
        print(f"❌ Error DT: {e}")
        return 0
    
    soup = BeautifulSoup(resp.text, "html.parser")
    insertadas = 0
    
    # Buscar noticias en diferentes secciones
    selectores_noticias = [
        "#noticia-destacada .recuadro",
        "#recuadros_articulo_17328 .recuadro",
        ".recuadro"
    ]
    
    for selector in selectores_noticias:
        for recuadro in soup.select(selector):
            try:
                # Buscar título y enlace
                titulo_elem = (recuadro.select_one("h3 a") or 
                              recuadro.select_one("p.abstract a") or
                              recuadro.select_one("a"))
                
                if not titulo_elem:
                    continue
                
                titulo = html.unescape(titulo_elem.text.strip())
                if not titulo or len(titulo) < 10:
                    continue
                
                url_relativa = titulo_elem.get("href")
                if not url_relativa:
                    continue
                
                url = urljoin(FULL_URL, url_relativa)
                
                _, creado = Noticia.objects.get_or_create(
                    url=url,
                    defaults={
                        "titulo": titulo,
                        "categoria": "laboral",
                        "fuente": "Dirección del Trabajo",
                    }
                )
                if creado:
                    insertadas += 1
            except Exception as e:
                continue
    
    print(f"✅ DT: {insertadas} noticias insertadas")
    return insertadas

def ejecutar_scraping_completo():
    """Ejecuta todos los scrapers"""
    print("🚀 INICIANDO SCRAPING COMPLETO")
    print("=" * 50)
    
    total_inicial = Noticia.objects.count()
    
    # Ejecutar todos los scrapers
    sii_count = scrape_sii()
    achs_count = scrape_achs()
    cnn_count = scrape_cnn()
    dt_count = scrape_dt()
    
    total_final = Noticia.objects.count()
    nuevas = total_final - total_inicial
    
    print("=" * 50)
    print("🎉 RESUMEN DE SCRAPING:")
    print(f"📊 SII: {sii_count} noticias")
    print(f"📊 ACHS: {achs_count} noticias")
    print(f"📊 CNN: {cnn_count} noticias")
    print(f"📊 DT: {dt_count} noticias")
    print(f"📊 TOTAL NUEVAS: {nuevas} noticias")
    print(f"📊 TOTAL EN BD: {total_final} noticias")
    
    # Mostrar por categoría
    print("\n📋 POR CATEGORÍA:")
    categorias = Noticia.objects.values('categoria').distinct()
    for cat in categorias:
        count = Noticia.objects.filter(categoria=cat['categoria']).count()
        print(f"   - {cat['categoria']}: {count} noticias")
    
    print("✅ SCRAPING COMPLETADO")

if __name__ == "__main__":
    ejecutar_scraping_completo()