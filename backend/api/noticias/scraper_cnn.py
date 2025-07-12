import requests
from bs4 import BeautifulSoup
from api.models import Noticia

def categorizar_cnn(url: str) -> str | None:
    if "mundo" in url:
        return "internacional"
    elif "politica" in url or "gobierno" in url or "elecciones" in url:
        return "politica"
    elif "economia" in url or "negocios" in url:
        return "economica"
    return None

def scrape_cnn():
    url = "https://cnnespanol.cnn.com/mundo"
    base_url = "https://cnnespanol.cnn.com"

    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
    except Exception as e:
        print(f"❌ Error al acceder a CNN: {e}")
        return

    soup = BeautifulSoup(resp.text, "html.parser")
    noticias_insertadas = 0

    print("🔎 Explorando artículos de CNN en Español...\n")

    # Noticias con estructura específica
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

        categoria = categorizar_cnn(enlace)
        if not categoria:
            continue

        print(f"➡️ {titulo} | {url_completo} | Categoría: {categoria}")

        _, creado = Noticia.objects.get_or_create(
            url=url_completo,
            defaults={
                "titulo": titulo,
                "categoria": categoria,
                "fuente": "CNN en Español",
            }
        )

        if creado:
            noticias_insertadas += 1

    print(f"\n✅ Se insertaron {noticias_insertadas} noticias desde CNN en Español\n")

if __name__ == "__main__":
    scrape_cnn()
