# 🎵 Letras Scraper
Este script en Python permite extraer automáticamente la lista de canciones y sus letras desde [letras.com](https://www.letras.com/) para un artista cubano o de cualquier otra región, guardándolas en un archivo de texto plano.

## 📦 Requisitos
- Python 3.7 o superior

### Librerías:
- requests
- beautifulsoup4

## 🚀 Uso
Desde la terminal, ejecuta el script con el nombre del artista (slug de URL):

```py
python script.py nombre-del-artista
```
Por ejemplo:

```
python script.py carlos-varela
python script.py silvio-rodriguez
```
Esto generará un archivo llamado letras-nombre-del-artista.txt con las letras de todas las canciones disponibles para ese artista.

## 💡 ¿Cómo saber el nombre-del-artista?
Debes usar el segmento de la URL del artista en letras.com.
Por ejemplo:
https://www.letras.com/**carlos-varela**/
→ el slug sería carlos-varela.
