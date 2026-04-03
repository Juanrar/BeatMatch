import os
import shutil
import tempfile

import numpy as np
import scipy.io.wavfile
import scipy.signal

from ffmpeg_utils import run_ffmpeg


def extract_mono_wav(input_path: str, output_wav: str) -> None:
    """Extrae todo el audio a 8000 Hz en Mono para analisis FFT."""
    args = [
        "-y",
        "-i", input_path,
        "-vn",
        "-ac", "1",
        "-ar", "8000",
        output_wav,
    ]
    run_ffmpeg(args)


def find_audio_offset(video_audio_path: str, song_audio_path: str) -> float:
    """Encuentra en que momento (offset) la cancion comienza respecto al video.

    Convierte ambos a WAV 8000Hz Mono temporalmente y usa Correlacion Cruzada
    con Fast Fourier Transform (FFT) para hallar el desfasaje exacto.

    Retorna float en segundos. Si es positivo, el video empieza adentro de
    la cancion (la cancion debe adelantarse). Si es negativo, el video empieza
    antes que la cancion (la cancion debe retrasarse).
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        wav_video = os.path.join(tmpdir, "video.wav")
        wav_song = os.path.join(tmpdir, "song.wav")

        print("Preparando analisis espectral (esto puede demorar unos segundos)...")
        extract_mono_wav(video_audio_path, wav_video)
        extract_mono_wav(song_audio_path, wav_song)

        rate1, data_video = scipy.io.wavfile.read(wav_video)
        rate2, data_song = scipy.io.wavfile.read(wav_song)

        if rate1 != rate2:
            raise RuntimeError("Diferencia de sample rate en la extraccion.")

        # Garantizar float32 para evitar overflow en multiplicaciones
        data_video = data_video.astype(np.float32)
        data_song = data_song.astype(np.float32)

        # scipy correlaciona: in1 y in2
        # Queremos buscar in1 (video, corto) adentro de in2 (cancion, largo)
        # El lag sera indexado donde in1 encastra en in2
        print("Alineando ondas por correlacion cruzada (FFT)...")
        correlation = scipy.signal.correlate(data_video, data_song, mode="full", method="fft")
        lags = scipy.signal.correlation_lags(data_video.size, data_song.size, mode="full")

        lag = lags[np.argmax(correlation)]
        offset_seconds = -lag / rate1

        return offset_seconds
