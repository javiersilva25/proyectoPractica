import requests
from bs4 import BeautifulSoup
import html
from api.models import Noticia

URL = "https://www.achs.cl/centro-de-noticias"

def scrape_achs():
    print("🔎 Buscando noticias en el sitio de la ACHS...")

    try:
        resp = requests.get(URL, timeout=10)
        resp.raise_for_status()
    except Exception as e:
        print(f"❌ Error al acceder a {URL}: {e}")
        return

    soup = BeautifulSoup(resp.text, "html.parser")
    noticias = soup.select("div.box-not")

    if not noticias:
        print("⚠️ No se encontraron noticias con el selector 'div.box-not'.")
        return

    noticias_insertadas = 0

    for box in noticias:
        h4 = box.select_one("h4")
        fecha_div = box.select_one("div.fecha")
        enlace_tag = box.select_one("a[href]")

        if not (h4 and fecha_div and enlace_tag):
            continue

        titulo = html.unescape(h4.get_text(strip=True))
        fecha = fecha_div.get_text(strip=True)
        enlace = enlace_tag["href"].strip()

        print(f"📰 {fecha} | {titulo} | {enlace}")

        _, creado = Noticia.objects.get_or_create(
            url=enlace,
            defaults={
                "titulo": titulo,
                "categoria": "laboral",
                "fuente": "ACHS",
            }
        )

        if creado:
            noticias_insertadas += 1

    print(f"\n✅ Se insertaron {noticias_insertadas} noticias desde achs.cl")

if __name__ == "__main__":
    scrape_achs()
