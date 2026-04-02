"""Descarga de canciones completas desde YouTube usando yt-dlp."""

import os

import yt_dlp

from ffmpeg_utils import find_ffmpeg


def download_song(artist: str, title: str, output_dir: str) -> str:
    """Busca y descarga la cancion completa desde YouTube.

    Args:
        artist: Nombre del artista.
        title: Titulo de la cancion.
        output_dir: Directorio donde guardar el archivo descargado.

    Returns:
        Ruta al archivo de audio descargado.

    Raises:
        RuntimeError: Si no se pudo descargar la cancion.
    """
    query = f"{artist} - {title}"
    output_template = os.path.join(output_dir, "song.%(ext)s")

    ffmpeg_path = find_ffmpeg()
    ffmpeg_dir = os.path.dirname(ffmpeg_path) if os.path.isfile(ffmpeg_path) else None

    ydl_opts = {
        "format": "bestaudio/best",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "m4a",
            "preferredquality": "192",
        }],
        "default_search": "ytsearch1",
        "outtmpl": output_template,
        "quiet": True,
        "no_warnings": True,
    }

    if ffmpeg_dir:
        ydl_opts["ffmpeg_location"] = ffmpeg_dir

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"Buscando en YouTube: {query}...")
            ydl.download([query])
    except Exception as exc:
        raise RuntimeError(f"Error descargando cancion: {exc}")

    expected_path = os.path.join(output_dir, "song.m4a")
    if not os.path.isfile(expected_path):
        # Buscar cualquier archivo song.* generado
        for f in os.listdir(output_dir):
            if f.startswith("song.") and f != "song.wav":
                return os.path.join(output_dir, f)
        raise RuntimeError("No se encontro el archivo de audio descargado")

    return expected_path
