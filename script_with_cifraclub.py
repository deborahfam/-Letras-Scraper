import re
import sys
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

LETRAS_BASE = "https://www.letras.com"
HEADERS = {"User-Agent": "Mozilla/5.0"}

def get_song_links(artist_slug: str) -> list[tuple[str, str]]:
    print(f"⏳ Obteniendo lista de canciones de {artist_slug} …")
    url = f"{LETRAS_BASE}/{artist_slug}/"
    soup = BeautifulSoup(requests.get(url, headers=HEADERS).text, "html.parser")

    links: list[tuple[str, str]] = []
    for li in soup.select("li.songList-table-row.--song"):
        a_tag = li.find("a")
        if not a_tag:
            continue

        title = a_tag.get_text(strip=True)
        href = a_tag.get("href", "")

        if "cifraclub.com" not in href:
            continue

        full_url = href if bool(urlparse(href).netloc) else urljoin(LETRAS_BASE, href)
        links.append((title, full_url))

    print(f"✅ Encontradas {len(links)} canciones enlazadas a CifraClub.")
    return links

_CHORD_RE = re.compile(r"^[A-G][#b]?m?(aj7|sus\d|dim|\d+)?$")

def clean_pre(pre_tag: BeautifulSoup) -> str:
    for b in pre_tag.find_all("b"):
        b.decompose()

    raw_lines = (line.strip() for line in pre_tag.get_text("\n").splitlines())
    lyrics_lines = [
        ln for ln in raw_lines
        if ln and not _CHORD_RE.fullmatch(ln)
    ]
    return "\n".join(lyrics_lines)

def get_song_lyrics(url: str) -> str:
    """
    Descarga la página de CifraClub y devuelve sólo la letra (sin acordes).
    """
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        pre_tag = soup.select_one("div.cifra_cnt pre")
        if not pre_tag:
            return "Letra no encontrada (⛔ estructura inesperada)"

        return clean_pre(pre_tag)

    except Exception as err:
        return f"Error al obtener letra ({err})"

def save_to_file(songs: list[tuple[str, str]], artist_slug: str) -> None:
    filename = f"letras-{artist_slug}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        for title, lyrics in songs:
            f.write(title + "\n")
            f.write(lyrics + "\n")
            f.write("\n" + "-" * 60 + "\n\n")
    print(f"💾 Letras guardadas en {filename}")

def main(artist_slug: str) -> None:
    songs: list[tuple[str, str]] = []
    links = get_song_links(artist_slug)

    for idx, (title, url) in enumerate(links, 1):
        print(f"[{idx}/{len(links)}] ⤵️  Descargando «{title}»")
        lyrics = get_song_lyrics(url)
        songs.append((title, lyrics))
        save_to_file(songs, artist_slug)
        time.sleep(1)

    print("🏁 Proceso completado.")

# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❗ Uso: python script.py nombre-del-artista (p. ej.: duo-los-compadres)")
        sys.exit(1)

    main(sys.argv[1].strip("/"))
