#!/usr/bin/env python3
"""
BeatMatch — Reconocimiento musical y composición de video sincronizado.

Reconoce la canción que suena en un video, descarga el audio completo
desde YouTube, y genera un nuevo MP4 con el video original y la canción
sincronizada.

Requisitos:
- Python 3.10+
- ffmpeg instalado y disponible en PATH
- Token de AudD en archivo .env

Instalación:
    pip install -r requirements.txt

Uso:
    python main.py ruta/del/video.mp4
"""

import os
import sys
import tempfile

from dotenv import load_dotenv

from audio_extractor import extract_audio
from song_recognizer import recognize_song
from song_downloader import download_song
from video_composer import compose_video

load_dotenv()


def _build_output_path(video_path: str) -> str:
    """Genera el nombre del archivo de salida: video_beatmatch.mp4."""
    base, ext = os.path.splitext(video_path)
    return f"{base}_beatmatch{ext}"


def main() -> int:
    if len(sys.argv) != 2:
        print("Uso: python main.py ruta/del/video.mp4")
        return 1

    video_path = sys.argv[1]

    if not os.path.isfile(video_path):
        print("Error: el archivo de video no existe")
        return 1

    token = os.getenv("AUDD_API_TOKEN")
    if not token:
        print("Error: falta la variable de entorno AUDD_API_TOKEN")
        return 1

    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            # 1. Extraer audio y reconocer canción
            print("Extrayendo audio del video...")
            audio_sample = extract_audio(video_path, tmpdir)

            print("Reconociendo canción...")
            match = recognize_song(audio_sample, token)

            print(f"Canción: {match.artist} - {match.title}")
            print(f"Álbum: {match.album}")
            print(f"Timecode: {match.timecode_raw} ({match.timecode_seconds}s)")

            # 2. Descargar canción completa desde YouTube
            song_path = download_song(match.artist, match.title, tmpdir)
            print("Descarga completada.")

            # 3. Componer video con audio sincronizado
            output_path = _build_output_path(video_path)
            compose_video(video_path, song_path, match.timecode_seconds, output_path)

        print(f"Video generado: {output_path}")
        return 0

    except LookupError as exc:
        print(f"Error: {exc}")
        return 1
    except RuntimeError as exc:
        print(f"Error: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
