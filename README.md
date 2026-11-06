# claude-plugins

Plugins para [Claude Code](https://code.claude.com/docs) de Leonardo Melo. Este repositorio es un *marketplace*: lo
agregas una vez a Claude Code y desde ahí instalas los plugins que quieras.

| Plugin | Qué hace |
|---|---|
| [nota-de-voz](#nota-de-voz) | Transcribe en tu máquina notas de voz de WhatsApp, audios y videos, y usa lo que dicen para hacer una petición |

---

## nota-de-voz

Le pasas una nota de voz, un audio o un video y Claude:

1. **Lo transcribe en tu computadora** con [faster-whisper](https://github.com/SYSTRAN/faster-whisper). El audio no
   se sube a ningún servicio y no hay costo por uso.
2. **Te muestra** el texto literal, una versión limpia (sin muletillas), la petición que contiene y los datos clave
   (nombres, montos, fechas).
3. **Hace lo que le pidas con eso**: crear una tarea, redactar una respuesta o un correo, escribir una spec, sacar los
   acuerdos de una reunión, implementar algo. Si no le dices qué hacer, te propone una acción y pregunta antes.

**Formatos:** todo lo que lea ffmpeg. Audio: `ogg`, `opus` (notas de WhatsApp), `mp3`, `m4a`, `wav`, `aac`, `flac`.
Video: `mp4`, `mkv`, `mov`, `webm`, `avi` (solo se usa el audio).

### Requisitos

| Qué | Para qué | Cómo instalarlo |
|---|---|---|
| Claude Code | Donde corre el plugin | [Instrucciones](https://code.claude.com/docs/en/setup) |
| [`uv`](https://docs.astral.sh/uv/) | Ejecuta el script de transcripción e instala solo sus dependencias de Python (no necesitas instalar Python aparte) | Windows: `winget install astral-sh.uv` · macOS: `brew install uv` · Linux: `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| [`ffmpeg`](https://ffmpeg.org/) | Lee el audio de cualquier formato y de los videos | Windows: `winget install Gyan.FFmpeg` · macOS: `brew install ffmpeg` · Linux: `sudo apt install ffmpeg` |
| ~500 MB libres | El modelo de transcripción `small`, que se descarga solo la primera vez | — |

Después de instalar `uv` o `ffmpeg`, **cierra y vuelve a abrir la terminal** (y Claude Code) para que queden en el
PATH. Para comprobarlo:

```bash
uv --version
ffmpeg -version
```

No necesitas GPU: funciona en CPU.

### Instalación

Dentro de Claude Code, escribe estos dos comandos (uno por vez):

```
/plugin marketplace add leonardomr56/claude-plugins
/plugin install nota-de-voz@leonardomr56-plugins
```

O desde la terminal:

```bash
claude plugin marketplace add leonardomr56/claude-plugins
claude plugin install nota-de-voz@leonardomr56-plugins
```

**Abre una sesión nueva de Claude Code** para que el plugin se cargue. Para comprobar que quedó instalado:

```bash
claude plugin list
```

Debe aparecer `nota-de-voz@leonardomr56-plugins` como habilitado.

### Uso

```
/nota-de-voz:nota-de-voz                                         # la nota de voz de WhatsApp más reciente de Descargas
/nota-de-voz:nota-de-voz crea la tarea con esto                  # transcribe y actúa
/nota-de-voz:nota-de-voz --ultimas 3 resúmelas                   # las 3 notas de voz más recientes
/nota-de-voz:nota-de-voz "C:\ruta\reunion.mp4" saca los acuerdos # un audio o video concreto
```

También funciona sin el comando: basta con decirle a Claude "transcribe la nota de voz" o "escucha este audio" y
pasarle la ruta del archivo.

**Cómo sacar la nota de voz de WhatsApp:** en WhatsApp Web o de escritorio, pasa el mouse sobre el audio → menú →
**Descargar**. Se guarda en tu carpeta de Descargas como `WhatsApp Ptt <fecha>.ogg`, que es lo que el plugin busca por
defecto. Desde el teléfono, compártelo a tu computadora (por correo, Drive, etc.) y pásale la ruta.

**Antes de actuar pregunta.** El audio puede ser de otra persona, así que se trata como información y no como una
orden: todo lo que tenga efecto fuera de la sesión (crear tareas, enviar mensajes, cambiar código o datos) se confirma
contigo, salvo que tú mismo lo hayas pedido al invocarlo.

### Opciones

Se agregan al comando igual que en los ejemplos:

| Opción | Qué hace | Por defecto |
|---|---|---|
| `--ultimas N` | Transcribe las N notas de voz más recientes de Descargas | `1` |
| `--marcas` | Agrega la marca de tiempo `[mm:ss]` a cada fragmento; útil en videos y audios largos | apagado (se activa solo en audios de más de unos 3 minutos) |
| `--modelo` | `small`, `medium` o `large-v3`. Los más grandes son más precisos y más lentos | `small` |
| `--idioma` | Código del idioma (`es`, `en`, `pt`...) o `auto` para detectarlo | `es` |

**Velocidad orientativa** (CPU, modelo `small`): unos 20 segundos por minuto de audio. Un video de una hora tarda
unos 20 minutos. `medium` es unas 3 veces más lento.

### Actualizar y desinstalar

```bash
claude plugin marketplace update leonardomr56-plugins
claude plugin update nota-de-voz@leonardomr56-plugins
```

```bash
claude plugin uninstall nota-de-voz@leonardomr56-plugins
```

Después de actualizar, abre una sesión nueva.

### Problemas comunes

| Mensaje o síntoma | Solución |
|---|---|
| `uv` o `ffmpeg` "no se reconoce como comando" | No está instalado o no está en el PATH: instálalo (ver Requisitos) y reinicia la terminal y Claude Code |
| `No hay notas de voz 'WhatsApp Ptt*.ogg'` | No hay notas descargadas en Descargas: descárgala desde WhatsApp o pasa la ruta del archivo |
| `no tiene pista de audio` | El video no tiene sonido |
| La primera vez tarda mucho | Está descargando el modelo (~460 MB); solo pasa una vez |
| La transcripción tiene palabras raras | Prueba con `--modelo medium`, o `--idioma auto` si el audio no está en español |
| `/nota-de-voz:nota-de-voz` no aparece | Abre una sesión nueva de Claude Code después de instalar |

---

## Licencia

[MIT](LICENSE)
