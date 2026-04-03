#!/usr/bin/env python3
"""
BeatMatch — Reconocimiento musical y composición de video sincronizado.

Reconoce la canción que suena en un video, descarga el audio completo
desde YouTube, y genera un nuevo MP4 con el video original y la canción
sincronizada.

Requisitos:
- Python 3.10+
- ffmpeg instalado y disponible en PATH
- Token de AudD en archivo .env (si se usa detección automática)

Instalación:
    pip install -r requirements.txt

Uso:
    python main.py ruta/del/video.mp4
    python main.py ruta/del/video.mp4 --query "Artista - Cancion"
    python main.py ruta/del/video.mp4 --audio "ruta/a/cancion.mp3"
"""

import argparse
import os
import sys
import tempfile

from dotenv import load_dotenv

from audio_extractor import extract_audio
from song_recognizer import recognize_song
from song_downloader import download_song
from video_composer import compose_video
from audio_aligner import find_audio_offset

load_dotenv()


def _build_output_path(video_path: str) -> str:
    """Genera el nombre del archivo de salida: video_beatmatch.mp4."""
    base, ext = os.path.splitext(video_path)
    return f"{base}_beatmatch{ext}"


def main() -> int:
    parser = argparse.ArgumentParser(description="Sincroniza videos con audios de alta calidad.")
    parser.add_argument("video", help="Ruta al archivo de video original.")
    parser.add_argument("--query", "-q", help="Descargar esta cancion (Ej: 'Artista - Cancion'). Saltea AudD y usa analisis por FFT.")
    parser.add_argument("--audio", "-a", help="Usar este archivo de audio local. Saltea AudD, YT-DLP y usa analisis por FFT.")
    
    args = parser.parse_args()
    video_path = args.video

    if not os.path.isfile(video_path):
        print(f"Error: el archivo de video '{video_path}' no existe")
        return 1

    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            song_path = None
            offset = 0.0

            if args.audio:
                # 1. El usuario pasó una pista local de audio
                if not os.path.isfile(args.audio):
                    print(f"Error: El archivo de audio '{args.audio}' no existe.")
                    return 1
                print(f"Modo manual: Usando archivo local '{args.audio}'")
                song_path = args.audio
                offset = find_audio_offset(video_path, song_path)
                print(f"Offset detectado matemáticamente: {offset:.3f} segundos")

            elif args.query:
                # 2. El usuario pidio una cancion especifica, no AudD
                print(f"Modo manual: Buscando la cancion '{args.query}' en YouTube...")
                # Enviamos el query entero como title
                song_path = download_song("", args.query, tmpdir)
                print("Descarga completada. Analizando audio...")
                offset = find_audio_offset(video_path, song_path)
                print(f"Offset detectado matemáticamente: {offset:.3f} segundos")

            else:
                # 3. Flujo actual: uso de AudD para reconocer audio automaticamente
                token = os.getenv("AUDD_API_TOKEN")
                if not token:
                    print("Error: falta la variable de entorno AUDD_API_TOKEN para usar reconocimiento automatico.")
                    print("Podes usar la herramienta sin API Token mediante --query o --audio.")
                    return 1
                
                print("Extrayendo audio del video para AudD...")
                audio_sample = extract_audio(video_path, tmpdir)

                print("Reconociendo canción...")
                match = recognize_song(audio_sample, token)
                print(f"Canción: {match.artist} - {match.title}")
                print(f"Álbum: {match.album}")
                print(f"Timecode AudD: {match.timecode_raw} ({match.timecode_seconds}s)")

                print(f"Buscando en YouTube la cancion reconocida...")
                song_path = download_song(match.artist, match.title, tmpdir)
                print("Descarga completada. Analizando audio...")
                offset = find_audio_offset(video_path, song_path)
                print(f"Offset detectado matemáticamente: {offset:.3f} segundos")

            # Componer video
            output_path = _build_output_path(video_path)
            compose_video(video_path, song_path, offset, output_path)

        print(f"\n¡Video generado exitosamente!\nRuta local: {output_path}")
        return 0

    except LookupError as exc:
        print(f"Error: {exc}")
        return 1
    except RuntimeError as exc:
        print(f"Error: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
