import requests
from bs4 import BeautifulSoup
import time
import sys

BASE_URL = "https://www.letras.com"
HEADERS = {'User-Agent': 'Mozilla/5.0'}

def get_song_links(artist_slug):
    artist_url = f"{BASE_URL}/{artist_slug}/"
    print(f"Obteniendo lista de canciones de {artist_slug}...")
    response = requests.get(artist_url, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = []
    for li in soup.select('li.songList-table-row.--song'):
        a_tag = li.find('a')
        title = a_tag.get_text(strip=True)
        href = a_tag.get('href')
        if href and href.startswith(f"/{artist_slug}/"):
            links.append((title, BASE_URL + href))
    return links

def get_song_lyrics(url):
    try:
        response = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(response.text, 'html.parser')
        letra_div = soup.find('div', class_='lyric-original') or soup.find('div', class_='cnt-letra')
        if letra_div:
            return letra_div.get_text(separator='\n', strip=True)
        return "Letra no disponible"
    except Exception as e:
        print(f"❌ Error obteniendo letra: {e}")
        return "Error al obtener letra"

def save_to_file(songs, artist_slug):
    filename = f"letras-{artist_slug}.txt"
    print(f"Guardando letras en {filename}...")
    with open(filename, 'w', encoding='utf-8') as f:
        for title, lyrics in songs:
            f.write(f"{title}\n")
            f.write(f"{lyrics}\n")
            f.write("\n" + "-"*60 + "\n\n")

def main(artist_slug):
    songs_data = []
    links = get_song_links(artist_slug)
    print(f"Se encontraron {len(links)} canciones.")
    for i, (title, url) in enumerate(links, 1):
        print(f"[{i}/{len(links)}] Descargando: {title}")
        lyrics = get_song_lyrics(url)
        songs_data.append((title, lyrics))
        save_to_file(songs_data, artist_slug)
        time.sleep(1)
    save_to_file(songs_data, artist_slug)
    print("✅ Proceso completado.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❗Uso: python script.py nombre-del-artista (por ejemplo: carlos-varela)")
    else:
        artist_slug = sys.argv[1].strip('/')
        main(artist_slug)
