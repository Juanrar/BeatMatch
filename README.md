# BeatMatch

BeatMatch es una herramienta para el reconocimiento musical y la composición de videos sincronizados. Permite identificar la canción que suena en un video, descargar el audio completo desde YouTube y generar un nuevo archivo MP4 con el video original y la canción sincronizada.

## Requisitos

- Python 3.10+
- ffmpeg instalado y disponible en PATH
- Archivo `.env` con las siguientes variables:
  - `AUDD_API_TOKEN`: Token de la API de AudD
  - `ACR_ACCESS_KEY`: Clave de acceso para ACRCloud
  - `ACR_ACCESS_SECRET`: Secreto de acceso para ACRCloud
  - `ACR_REQURL`: URL del endpoint de ACRCloud

## Instalación

1. Clona este repositorio:
   ```bash
   git clone <URL_DEL_REPOSITORIO>
   ```
2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Asegúrate de tener `ffmpeg` instalado y configurado en tu PATH.

## Uso

Ejecuta el script principal con uno de los siguientes comandos:

### Reconocimiento automático
```bash
python main.py ruta/del/video.mp4
```

### Especificar una canción manualmente
```bash
python main.py ruta/del/video.mp4 --query "Artista - Canción"
```

### Usar un archivo de audio local
```bash
python main.py ruta/del/video.mp4 --audio "ruta/a/cancion.mp3"
```

## Notas

- Asegúrate de que el archivo de video sea válido y no esté corrupto.
- Si encuentras problemas con `ffmpeg`, verifica que esté correctamente instalado y configurado.

## Licencia

BeatMatch es un proyecto de código abierto bajo la licencia MIT.