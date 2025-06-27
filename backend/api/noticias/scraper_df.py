import requests
from bs4 import BeautifulSoup
from api.models import Noticia

def categorizar_enlace(url: str) -> str | None:
    if "internacional" in url:
        return "internacional"
    elif "politica" in url or "nacional" in url:
        return "politica"
    elif any(x in url for x in ["economica", "negocios", "empresas", "mercados"]):
        return "economica"
    else:
        return None

def scrape_df():
    url = "https://www.df.cl/"
    resp = requests.get(url, timeout=10)
    soup = BeautifulSoup(resp.text, "html.parser")

    enlaces = soup.find_all("a", href=True)
    noticias_insertadas = 0

    print("🔎 Explorando enlaces del home de df.cl...\n")

    for a in enlaces:
        titulo = a.get_text(strip=True)
        enlace = a["href"]

        if not titulo or not enlace.startswith("https://"):
            continue

        categoria = categorizar_enlace(enlace)
        if not categoria:
            continue

        print(f"➡️ {titulo} | {enlace} | Categoría: {categoria}")

        Noticia.objects.get_or_create(
            url=enlace,
            defaults={
                "titulo": titulo,
                "categoria": categoria,
                "fuente": "Diario Financiero",
            }
        )
        noticias_insertadas += 1

    print(f"\n✅ Se insertaron {noticias_insertadas} noticias desde df.cl")
