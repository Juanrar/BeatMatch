"""Extraccion de audio desde un archivo de video."""

import os

from ffmpeg_utils import run_ffmpeg


def extract_audio(video_path: str, output_dir: str, duracion: int = 20) -> str:
    """Extrae un fragmento de audio del video para reconocimiento.

    Args:
        video_path: Ruta al archivo de video.
        output_dir: Directorio donde guardar el archivo de audio.
        duracion: Segundos de audio a extraer.

    Returns:
        Ruta al archivo de audio generado.
    """
    audio_path = os.path.join(output_dir, "sample.wav")

    run_ffmpeg([
        "-y",
        "-i", video_path,
        "-vn",
        "-ac", "1",
        "-ar", "44100",
        "-t", str(duracion),
        audio_path,
    ])

    return audio_path
