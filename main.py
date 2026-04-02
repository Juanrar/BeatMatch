#!/usr/bin/env python3
"""
Reconocimiento musical desde un video (consola).

Requisitos:
- Python 3.8+
- ffmpeg instalado y disponible en PATH
- requests

Instalacion de dependencias:
- pip install requests

Configuracion de API key (AudD):
- Define la variable de entorno AUDD_API_TOKEN
  - PowerShell: $env:AUDD_API_TOKEN="tu_token"
  - CMD: set AUDD_API_TOKEN=tu_token

Uso:
- python main.py ruta/del/video.mp4
"""

import json
import os
import subprocess
import sys
import tempfile

import requests
from dotenv import load_dotenv

load_dotenv()


def _buscar_ffmpeg() -> str:
    """Busca ffmpeg en PATH y en ubicaciones comunes de WinGet."""
    import shutil
    import glob

    found = shutil.which("ffmpeg")
    if found:
        return found

    # Buscar en instalaciones de WinGet
    winget_pattern = os.path.join(
        os.environ.get("LOCALAPPDATA", ""),
        "Microsoft", "WinGet", "Packages", "Gyan.FFmpeg*", "**", "ffmpeg.exe",
    )
    matches = glob.glob(winget_pattern, recursive=True)
    if matches:
        return matches[0]

    return "ffmpeg"


def extraer_audio(video_path: str, audio_path: str) -> None:
    ffmpeg_bin = _buscar_ffmpeg()
    cmd = [
        ffmpeg_bin,
        "-y",
        "-i",
        video_path,
        "-vn",
        "-ac",
        "1",
        "-ar",
        "44100",
        "-t",
        "20",
        audio_path,
    ]

    try:
        completed = subprocess.run(
            cmd,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
    except FileNotFoundError:
        raise RuntimeError("ffmpeg no esta instalado o no esta en PATH")
    except subprocess.CalledProcessError as exc:
        stderr = (exc.stderr or "").strip()
        raise RuntimeError(f"Error en ffmpeg: {stderr}")

    if completed.returncode != 0:
        raise RuntimeError("Error desconocido en ffmpeg")


def reconocer_cancion(audio_path: str, token: str) -> dict:
    url = "https://api.audd.io/"

    try:
        with open(audio_path, "rb") as audio_file:
            response = requests.post(
                url,
                data={"api_token": token},
                files={"file": audio_file},
                timeout=60,
            )
        response.raise_for_status()
    except requests.RequestException as exc:
        raise RuntimeError(f"Error consultando API de reconocimiento: {exc}")

    try:
        payload = response.json()
    except json.JSONDecodeError:
        raise RuntimeError("La API devolvio una respuesta invalida")

    result = payload.get("result")
    if not result:
        raise LookupError("Cancion no reconocida")

    return result


def formatear_tiempo(timecode: str) -> str:
    if not timecode:
        return "No disponible"

    partes = timecode.split(":")
    if len(partes) == 2:
        minutos, segundos = partes
        return f"{minutos}:{segundos}"
    if len(partes) == 3:
        _, minutos, segundos = partes
        return f"{minutos}:{segundos}"
    return timecode


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
            audio_path = os.path.join(tmpdir, "audio.wav")
            extraer_audio(video_path, audio_path)
            result = reconocer_cancion(audio_path, token)

        song = result.get("title") or "Desconocido"
        artist = result.get("artist") or "Desconocido"
        confidence = result.get("score") or result.get("confidence") or "No disponible"
        timecode = formatear_tiempo(result.get("timecode") or "")

        print(f"Cancion: {song}")
        print(f"Artista: {artist}")
        print(f"Confianza: {confidence}")
        print(f"Minuto del tema: {timecode}")
        return 0

    except LookupError as exc:
        print(f"Error: {exc}")
        return 1
    except RuntimeError as exc:
        print(f"Error: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
