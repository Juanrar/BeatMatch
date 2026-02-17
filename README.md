# BeatMatch

## Reconocimiento musical desde un video (consola)

### Requisitos
- Python 3.8+
- ffmpeg instalado y disponible en PATH
- requests

### Instalación de dependencias
```bash
pip install requests
```

### Configuración de API key (AudD)
Define la variable de entorno `AUDD_API_TOKEN`:
- **PowerShell**: `$env:AUDD_API_TOKEN="tu_token"`
- **CMD**: `set AUDD_API_TOKEN=tu_token`

### Uso
```bash
python main.py ruta/del/video.mp4
```