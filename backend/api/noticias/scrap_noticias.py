import re
import html
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime
from api.models import Noticia

# ------------------------ SII ------------------------
def scrape_sii():
    print("\U0001F50E Buscando noticias en el sitio del SII...")
    BASE_URL = "https://www.sii.cl/noticias/2025/"
    FULL_URL = BASE_URL + "index.html"

    try:
        resp = requests.get(FULL_URL, timeout=10)
        resp.raise_for_status()
    except Exception as e:
        print(f"\u274c Error al acceder a {FULL_URL}: {e}")
        return

    match = re.search(r"arrayIndice\s*=\s*(\[[^\]]+\])", resp.text, re.DOTALL)
    if not match:
        print("\u274c No se encontr\u00f3 el array de noticias en el HTML.")
        return

    array_js = match.group(1)
    items = re.findall(r"\['(.*?)',\s*'(.*?)',\s*'(.*?)',\s*'(.*?)'\]", array_js)
    if not items:
        print("\u26a0\ufe0f No se encontraron noticias en el array.")
        return

    noticias_insertadas = 0

    for id_noticia, fecha, titulo_html, img in items:
        url = urljoin(BASE_URL, f"{id_noticia}.htm")
        titulo = html.unescape(titulo_html).strip()
        try:
            fecha_obj = datetime.strptime(fecha.strip(), "%d/%m/%Y")
        except:
            fecha_obj = None

        print(f"\U0001F4F0 {fecha} | {titulo} | {url}")

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
            noticias_insertadas += 1

    print(f"\n\u2705 Se insertaron {noticias_insertadas} noticias desde sii.cl")


# ------------------------ CNN ------------------------
def scrape_cnn():
    url = "https://cnnespanol.cnn.com/mundo"
    base_url = "https://cnnespanol.cnn.com"

    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
    except Exception as e:
        print(f"\u274c Error al acceder a CNN: {e}")
        return

    soup = BeautifulSoup(resp.text, "html.parser")
    noticias_insertadas = 0
    print("\U0001F50E Explorando art\u00edculos de CNN en Espa\u00f1ol...\n")

    articulos = soup.select("a.container__link--type-article")
    for a in articulos:
        enlace = a.get("href")
        if not enlace or not enlace.startswith("/202"):
            continue

        titulo_tag = a.select_one(".container__headline-text")
        if not titulo_tag:
            continue

        titulo = titulo_tag.get_text(strip=True)
        url_completo = base_url + enlace
        categoria = categorizar_enlace(enlace)
        if not categoria:
            continue

        try:
            detalle = requests.get(url_completo, timeout=10)
            detalle.raise_for_status()
            soup_detalle = BeautifulSoup(detalle.text, "html.parser")
            fecha_elem = soup_detalle.select_one("meta[property='article:published_time']")
            fecha_raw = fecha_elem['content'] if fecha_elem else None
            fecha_obj = datetime.fromisoformat(fecha_raw[:-1]) if fecha_raw else None
        except:
            fecha_obj = None

        print(f"\u27a1\ufe0f {titulo} | {url_completo} | Categor\u00eda: {categoria}")

        _, creado = Noticia.objects.get_or_create(
            url=url_completo,
            defaults={
                "titulo": titulo,
                "categoria": categoria,
                "fuente": "CNN en Español",
                "fecha_publicacion": fecha_obj,
            }
        )
        if creado:
            noticias_insertadas += 1

    print(f"\n\u2705 Se insertaron {noticias_insertadas} noticias desde CNN en Espa\u00f1ol\n")


# ------------------------ Diario Financiero ------------------------
def scrape_df():
    url = "https://www.df.cl/"
    resp = requests.get(url, timeout=10)
    soup = BeautifulSoup(resp.text, "html.parser")

    enlaces = soup.find_all("a", href=True)
    noticias_insertadas = 0

    print("\U0001F50E Explorando enlaces del home de df.cl...\n")

    for a in enlaces:
        titulo = a.get_text(strip=True)
        enlace = a["href"]

        if not titulo or not enlace.startswith("https://"):
            continue

        categoria = categorizar_enlace(enlace)
        if not categoria:
            continue

        print(f"\u27a1\ufe0f {titulo} | {enlace} | Categor\u00eda: {categoria}")

        Noticia.objects.get_or_create(
            url=enlace,
            defaults={
                "titulo": titulo,
                "categoria": categoria,
                "fuente": "Diario Financiero",
                # fecha_publicacion: No disponible fácilmente
            }
        )
        noticias_insertadas += 1

    print(f"\n\u2705 Se insertaron {noticias_insertadas} noticias desde df.cl")


# ------------------------ Dirección del Trabajo ------------------------
def parse_fecha(fecha_str: str) -> datetime | None:
    formatos = ["%d de %B de %Y", "%d-%b-%Y"]
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
    print("\U0001F50E Buscando noticias en el sitio de la Dirección del Trabajo...")
    BASE_URL = "https://www.dt.gob.cl/portal/1627/"
    FULL_URL = urljoin(BASE_URL, "w3-channel.html")

    try:
        resp = requests.get(FULL_URL, timeout=10)
        resp.raise_for_status()
    except Exception as e:
        print(f"\u274c Error al acceder a {FULL_URL}: {e}")
        return

    soup = BeautifulSoup(resp.text, "html.parser")
    noticias_insertadas = 0

    # Noticia destacada
    destacada = soup.select_one("#noticia-destacada .recuadro")
    if destacada:
        titulo = destacada.select_one("h3 a").text.strip()
        url = urljoin(FULL_URL, destacada.select_one("h3 a")["href"])
        fecha_raw = destacada.select_one("span.fecha").text.strip()
        fecha = parse_fecha(fecha_raw)

        print(f"\U0001F4F0 {fecha_raw} | {titulo} | {url}")

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

    # Últimas noticias
    for recuadro in soup.select("#recuadros_articulo_17328 .recuadro"):
        titulo_elem = recuadro.select_one("p.abstract a")
        fecha_elem = recuadro.select_one("h6.fecha")

        if not titulo_elem or not fecha_elem:
            continue

        titulo = html.unescape(titulo_elem.text.strip())
        url = urljoin(FULL_URL, titulo_elem["href"])
        fecha_raw = fecha_elem.text.strip()
        fecha = parse_fecha(fecha_raw)

        print(f"\U0001F4F0 {fecha_raw} | {titulo} | {url}")

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

    print(f"\n\u2705 Se insertaron {noticias_insertadas} noticias desde dt.gob.cl")