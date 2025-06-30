import re
import requests
import html
from api.models import Noticia
from urllib.parse import urljoin

BASE_URL = "https://www.sii.cl/noticias/2025/"
FULL_URL = BASE_URL + "index.html"

def scrape_sii():
    print("🔎 Buscando noticias en el sitio del SII...")

    try:
        resp = requests.get(FULL_URL, timeout=10)
        resp.raise_for_status()
    except Exception as e:
        print(f"❌ Error al acceder a {FULL_URL}: {e}")
        return

    # Buscar el bloque de arrayIndice en el script JS
    match = re.search(r"arrayIndice\s*=\s*(\[[^\]]+\])", resp.text, re.DOTALL)
    if not match:
        print("❌ No se encontró el array de noticias en el HTML.")
        return

    array_js = match.group(1)

    # Extraer entradas del array: ['id', 'fecha', 'titulo', 'imagen']
    items = re.findall(r"\['(.*?)',\s*'(.*?)',\s*'(.*?)',\s*'(.*?)'\]", array_js)
    if not items:
        print("⚠️ No se encontraron noticias en el array.")
        return

    noticias_insertadas = 0

    for id_noticia, fecha, titulo_html, img in items:
        url = urljoin(BASE_URL, f"{id_noticia}.htm")
        titulo = html.unescape(titulo_html).strip()

        print(f"📰 {fecha} | {titulo} | {url}")

        # Insertar noticia si no existe
        _, creado = Noticia.objects.get_or_create(
            url=url,
            defaults={
                "titulo": titulo,
                "categoria": "tributaria",
                "fuente": "SII",
            }
        )

        if creado:
            noticias_insertadas += 1

    print(f"\n✅ Se insertaron {noticias_insertadas} noticias desde sii.cl")
