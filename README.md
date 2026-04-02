# BeatMatch

## Reconocimiento musical desde un video (consola)

### Requisitos
- Python 3.8+
- ffmpeg instalado y disponible en PATH

### Instalación de dependencias
```bash
pip install requests python-dotenv
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