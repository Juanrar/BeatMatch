"""Reconocimiento de canciones usando la API de AudD."""

import json
from dataclasses import dataclass

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


def _timecode_to_seconds(timecode: str) -> int:
    """Convierte un timecode 'MM:SS' o 'HH:MM:SS' a segundos."""
    if not timecode:
        return 0

    partes = timecode.split(":")
    if len(partes) == 2:
        minutos, segundos = int(partes[0]), int(partes[1])
        return minutos * 60 + segundos
    if len(partes) == 3:
        horas, minutos, segundos = int(partes[0]), int(partes[1]), int(partes[2])
        return horas * 3600 + minutos * 60 + segundos
    return 0


def recognize_song(audio_path: str, token: str) -> SongMatch:
    """Envia audio a AudD y retorna los datos de la cancion reconocida.

    Raises:
        LookupError: Si no se reconoce la cancion.
        RuntimeError: Si hay un error de red o respuesta invalida.
    """
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

    timecode_raw = result.get("timecode", "")

    return SongMatch(
        title=result.get("title", "Desconocido"),
        artist=result.get("artist", "Desconocido"),
        album=result.get("album", ""),
        timecode_raw=timecode_raw,
        timecode_seconds=_timecode_to_seconds(timecode_raw),
        song_link=result.get("song_link", ""),
    )
