import os
import time
import json
import base64
import hashlib
import hmac
from urllib.parse import urlparse
from dataclasses import dataclass
from dotenv import load_dotenv

import requests


@dataclass
class SongMatch:
    """Resultado del reconocimiento de una cancion."""

    title: str
    artist: str
    album: str
    timecode_raw: str
    timecode_seconds: int
    song_link: str


def _ms_to_timecode(ms: int) -> str:
    """Convierte milisegundos a un formato 'MM:SS'."""
    if not ms:
        return "00:00"
    
    segundos_totales = ms // 1000
    minutos = segundos_totales // 60
    segundos = segundos_totales % 60
    return f"{minutos:02d}:{segundos:02d}"


# Cargar variables de entorno desde el archivo .env
load_dotenv()

def recognize_song(audio_path: str) -> SongMatch:
    """Envia audio a ACRCloud y retorna los datos de la cancion reconocida.

    Raises:
        LookupError: Si no se reconoce la cancion o hay error del servicio.
        RuntimeError: Si hay un error de red, respuesta invalida o al leer archivo.
    """
    # Cargar credenciales desde variables de entorno
    access_key = os.getenv("ACR_ACCESS_KEY")
    access_secret = os.getenv("ACR_ACCESS_SECRET")
    requrl = os.getenv("ACR_REQURL")

    if not access_key or not access_secret or not requrl:
        raise RuntimeError("Faltan las credenciales de ACRCloud en las variables de entorno.")

    # 1. Configuración para la firma de ACRCloud (Signature)
    http_method = "POST"
    http_uri = urlparse(requrl).path # Extrae la ruta (por lo general /v1/identify)
    
    data_type = "audio"
    signature_version = "1"
    timestamp = str(int(time.time()))

    # Crear el string para firmar
    string_to_sign = f"{http_method}\n{http_uri}\n{access_key}\n{data_type}\n{signature_version}\n{timestamp}"
    
    # Generar firma HMAC-SHA1
    sign = base64.b64encode(
        hmac.new(
            access_secret.encode('ascii'), 
            string_to_sign.encode('ascii'), 
            digestmod=hashlib.sha1
        ).digest()
    ).decode('ascii')

    # 2. Preparar los datos y archivos para la petición
    try:
        file_size = os.path.getsize(audio_path)
        with open(audio_path, "rb") as audio_file:
            data = {
                'access_key': access_key,
                'sample_bytes': file_size,
                'timestamp': timestamp,
                'signature': sign,
                'data_type': data_type,
                'signature_version': signature_version
            }
            files = {'sample': audio_file}

            response = requests.post(requrl, data=data, files=files, timeout=60)
        response.raise_for_status()
    except requests.RequestException as exc:
        raise RuntimeError(f"Error consultando API de reconocimiento: {exc}")
    except OSError as exc:
        raise RuntimeError(f"Error accediendo al archivo de audio: {exc}")

    # 3. Analizar respuesta JSON
    try:
        payload = response.json()
    except json.JSONDecodeError:
        raise RuntimeError("La API devolvio una respuesta invalida")

    status = payload.get("status", {})
    if status.get("code") != 0:
        raise LookupError(f"Cancion no reconocida. ACRCloud Status: {status.get('msg')}")

    metadata = payload.get("metadata", {})
    music_list = metadata.get("music", [])

    if not music_list:
        raise LookupError("Cancion no reconocida")

    # Tomar la primera coincidencia
    match = music_list[0]

    # Extraer y formatear artistas
    artists_data = match.get("artists", [])
    artist_names = ", ".join(a.get("name", "") for a in artists_data) if artists_data else "Desconocido"

    # Procesar tiempos
    play_offset_ms = match.get("play_offset_ms", 0)
    timecode_seconds = play_offset_ms // 1000
    timecode_raw = _ms_to_timecode(play_offset_ms)

    # Buscar un enlace válido (ACRCloud anida esto en external_metadata)
    song_link = ""
    external_meta = match.get("external_metadata", {})
    if "spotify" in external_meta and "track" in external_meta["spotify"]:
        track_id = external_meta["spotify"]["track"].get("id")
        if track_id:
            song_link = f"https://open.spotify.com/track/{track_id}"
    elif "youtube" in external_meta:
        yt_id = external_meta["youtube"].get("vid")
        if yt_id:
            song_link = f"https://www.youtube.com/watch?v={yt_id}"

    return SongMatch(
        title=match.get("title", "Desconocido"),
        artist=artist_names,
        album=match.get("album", {}).get("name", ""),
        timecode_raw=timecode_raw,
        timecode_seconds=timecode_seconds,
        song_link=song_link,
    )