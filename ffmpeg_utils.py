"""Utilidades compartidas para interactuar con ffmpeg."""

import glob
import os
import shutil
import subprocess


def find_ffmpeg() -> str:
    """Busca el ejecutable de ffmpeg en PATH y ubicaciones comunes de WinGet."""
    found = shutil.which("ffmpeg")
    if found:
        return found

    winget_pattern = os.path.join(
        os.environ.get("LOCALAPPDATA", ""),
        "Microsoft", "WinGet", "Packages", "Gyan.FFmpeg*", "**", "ffmpeg.exe",
    )
    matches = glob.glob(winget_pattern, recursive=True)
    if matches:
        return matches[0]

    return "ffmpeg"


def run_ffmpeg(args: list[str]) -> subprocess.CompletedProcess:
    """Ejecuta ffmpeg con los argumentos dados. Lanza RuntimeError si falla."""
    ffmpeg_bin = find_ffmpeg()
    cmd = [ffmpeg_bin] + args

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

    return completed
