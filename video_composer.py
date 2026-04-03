"""Composicion de video con audio sincronizado usando ffmpeg."""

from ffmpeg_utils import run_ffmpeg


def compose_video(
    video_path: str,
    audio_path: str,
    offset_seconds: float,
    output_path: str,
) -> None:
    """Genera un MP4 combinando el video original con el audio sincronizado.

    Args:
        video_path: Ruta al video original.
        audio_path: Ruta al audio completo.
        offset_seconds: Offset calculado. Si es > 0 la canción empieza antes.
        output_path: Ruta del archivo final.
    """
    args = ["-y", "-i", video_path]

    if offset_seconds >= 0:
        # La canción debe empezar adelantada
        args.extend(["-ss", str(offset_seconds), "-i", audio_path])
    else:
        # El video empieza antes que la canción (la canción debe retrasarse)
        args.extend(["-itsoffset", str(abs(offset_seconds)), "-i", audio_path])

    args.extend([
        "-map", "0:v",
        "-map", "1:a",
        "-c:v", "copy",
        "-c:a", "aac",
        "-shortest",
        output_path,
    ])

    print("Componiendo video con audio sincronizado...")
    run_ffmpeg(args)
