# BeatMatch

## Reconocimiento y Sincronización de un video (consola)

Herramienta potente que sincroniza el audio de un video corto con el track musical final en alta calidad. Admite modo Automático (mediante reconocimiento de AudD) y modos Manuales apoyados en procesamiento avanzado de señales y matemáticas por correlación cruzada y FFT.

### Requisitos
- Python 3.10+
- ffmpeg instalado y disponible en PATH

### Instalación de dependencias
```bash
pip install -r requirements.txt
```

### Configuración de API key
Si vas a usar el reconocimiento automático (por defecto), debes usar tu API Token de AudD. Creá un archivo `.env` en la raíz del proyecto con tu token:
```
AUDD_API_TOKEN=tu_token
```
Podés obtener tu token en [audd.io](https://dashboard.audd.io/).

---

### MODO DE USO

**1. Modo Automático (Usa AudD):**
Reconoce la canción y sincroniza de acuerdo al timecode provisto por la API.
```bash
python main.py ruta/del/video.mp4
```

**2. Modo Manual de Búsqueda (Sin AudD, utiliza Correlación FFT):**
Evita el reconocimiento. Podes pasar el artista y canción exactos como texto, nosotros la descargamos y encontramos el desfasaje internamente.
```bash
python main.py ruta/del/video.mp4 --query "Artista - Tema"
```

**3. Modo Manual Local (Audio provisto, utiliza Correlación FFT):**
Ni siquiera necesitamos internet. Podes brindarle localmente ambos clips y armará la sincronización exacta.
```bash
python main.py ruta/del/video.mp4 --audio "ruta/de/la/cancion.mp3"
```

La app generará finalmente en el directorio del video un archivo optimizado llamado `video_beatmatch.mp4`.