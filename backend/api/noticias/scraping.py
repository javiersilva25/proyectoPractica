import requests
from bs4 import BeautifulSoup

URL = "https://www.df.cl/"

def obtener_noticias():
    try:
        response = requests.get(URL)
        response.raise_for_status()
    except requests.RequestException:
        return []

    soup = BeautifulSoup(response.text, 'html.parser')

    noticias = []

    for link in soup.find_all('a'):
        titulo = link.get_text(strip=True)
        href = link.get('href')

        # Validar que el título y enlace sean válidos y relevantes
        if titulo and href and 'df.cl' in href:
            noticias.append({
                'titulo': titulo,
                'url': href
            })

        # Limitar la cantidad de noticias
        if len(noticias) >= 5:
            break

    return noticias
