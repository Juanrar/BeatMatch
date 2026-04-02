# BeatMatch

## Reconocimiento musical y composición de video sincronizado

Reconoce la canción que suena en un video, descarga el audio completo desde YouTube, y genera un nuevo MP4 con el video original y la canción sincronizada.

### Requisitos
- Python 3.10+
- ffmpeg instalado y disponible en PATH

### Instalación de dependencias
```bash
pip install -r requirements.txt
```

### Configuración de API key (AudD)
Creá un archivo `.env` en la raíz del proyecto con tu token:
```
AUDD_API_TOKEN=tu_token
```
Podés obtener tu token en [audd.io](https://dashboard.audd.io/).

### Uso
```bash
python main.py ruta/del/video.mp4
```

El script:
1. Extrae un fragmento de audio del video
2. Reconoce la canción usando la API de AudD
3. Descarga la canción completa desde YouTube
4. Genera `video_beatmatch.mp4` con el audio sincronizado