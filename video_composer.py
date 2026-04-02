"""Composicion de video con audio sincronizado usando ffmpeg."""

from ffmpeg_utils import run_ffmpeg


def compose_video(
    video_path: str,
    audio_path: str,
    offset_seconds: int,
    output_path: str,
) -> None:
    """Genera un MP4 combinando el video original con el audio sincronizado.

    El offset_seconds indica en que segundo de la cancion empieza el video.
    FFmpeg corta el audio desde ese punto y lo combina con el video sin
    re-encodear la pista de video.

    Args:
        video_path: Ruta al video original.
        audio_path: Ruta al audio de la cancion completa.
        offset_seconds: Segundo de la cancion donde comienza el video.
        output_path: Ruta del archivo MP4 de salida.
    """
    args = [
        "-y",
        "-i", video_path,
        "-ss", str(offset_seconds),
        "-i", audio_path,
        "-map", "0:v",
        "-map", "1:a",
        "-c:v", "copy",
        "-c:a", "aac",
        "-shortest",
        output_path,
    ]

    print("Componiendo video con audio sincronizado...")
    run_ffmpeg(args)
