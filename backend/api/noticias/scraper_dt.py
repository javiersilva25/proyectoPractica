import requests
import html
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime
from api.models import Noticia

BASE_URL = "https://www.dt.gob.cl/portal/1627/"
FULL_URL = urljoin(BASE_URL, "w3-channel.html")


def parse_fecha(fecha_str: str) -> datetime | None:
    """Parsea fechas como '27 de junio de 2025' o '19-jun-2025' a objeto datetime."""
    formatos = [
        "%d de %B de %Y",  # español largo
        "%d-%b-%Y",        # corto con guiones
    ]
    meses = {
        "enero": "January", "febrero": "February", "marzo": "March",
        "abril": "April", "mayo": "May", "junio": "June",
        "julio": "July", "agosto": "August", "septiembre": "September",
        "octubre": "October", "noviembre": "November", "diciembre": "December",
    }

    for fmt in formatos:
        try:
            if "de" in fecha_str:
                for es, en in meses.items():
                    fecha_str = fecha_str.lower().replace(es, en)
            return datetime.strptime(fecha_str.strip(), fmt)
        except Exception:
            continue
    return None


def scrape_dt():
    print("🔎 Buscando noticias en el sitio de la Dirección del Trabajo...")

    try:
        resp = requests.get(FULL_URL, timeout=10)
        resp.raise_for_status()
    except Exception as e:
        print(f"❌ Error al acceder a {FULL_URL}: {e}")
        return

    soup = BeautifulSoup(resp.text, "html.parser")
    noticias_insertadas = 0

    # 🔹 Noticia destacada
    destacada = soup.select_one("#noticia-destacada .recuadro")
    if destacada:
        titulo = destacada.select_one("h3 a").text.strip()
        url = urljoin(FULL_URL, destacada.select_one("h3 a")["href"])
        fecha_raw = destacada.select_one("span.fecha").text.strip()
        fecha = parse_fecha(fecha_raw)

        print(f"📰 {fecha_raw} | {titulo} | {url}")

        _, creado = Noticia.objects.get_or_create(
            url=url,
            defaults={
                "titulo": titulo,
                "categoria": "laboral",
                "fuente": "Dirección del Trabajo",
                "fecha_publicacion": fecha,
            }
        )
        if creado:
            noticias_insertadas += 1

    # 🔹 Últimas noticias
    for recuadro in soup.select("#recuadros_articulo_17328 .recuadro"):
        titulo_elem = recuadro.select_one("p.abstract a")
        fecha_elem = recuadro.select_one("h6.fecha")

        if not titulo_elem or not fecha_elem:
            continue

        titulo = html.unescape(titulo_elem.text.strip())
        url = urljoin(FULL_URL, titulo_elem["href"])
        fecha_raw = fecha_elem.text.strip()
        fecha = parse_fecha(fecha_raw)

        print(f"📰 {fecha_raw} | {titulo} | {url}")

        _, creado = Noticia.objects.get_or_create(
            url=url,
            defaults={
                "titulo": titulo,
                "categoria": "laboral",
                "fuente": "Dirección del Trabajo",
                "fecha_publicacion": fecha,
            }
        )
        if creado:
            noticias_insertadas += 1

    print(f"\n✅ Se insertaron {noticias_insertadas} noticias desde dt.gob.cl")

if __name__ == "__main__":
    scrape_dt()
