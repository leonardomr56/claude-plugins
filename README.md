# claude-plugins

Plugins de Claude Code de Leonardo Melo.

## Instalar

```
/plugin marketplace add leonardomr56/claude-plugins
/plugin install nota-de-voz@leonardomr56-plugins
```

## Plugins

### nota-de-voz

Transcribe en tu máquina notas de voz de WhatsApp, audios y videos, y usa lo que dicen como base de una petición.

Formatos: todo lo que lea ffmpeg, por ejemplo `ogg`, `opus`, `mp3`, `m4a`, `wav`, `aac`, `flac` y videos `mp4`, `mkv`, `mov`, `webm`, `avi` (de los videos solo se usa el audio).

```
/nota-de-voz:nota-de-voz                          # la nota de voz más reciente de Descargas
/nota-de-voz:nota-de-voz crea la tarea con esto
/nota-de-voz:nota-de-voz --ultimas 3 resúmelas
/nota-de-voz:nota-de-voz "C:\ruta\reunion.mp4" saca los acuerdos
```

- Transcripción local con [faster-whisper](https://github.com/SYSTRAN/faster-whisper): el audio no sale de tu máquina y no hay costo por uso.
- Incluye el agente `transcriptor-voz` (modelo Haiku), que devuelve el texto literal, una versión limpia, la petición y los datos clave.
- Antes de hacer algo fuera de la sesión (crear tareas, enviar mensajes) pregunta, salvo que se lo pidas al invocarla.

**Requisitos:** [`uv`](https://docs.astral.sh/uv/) y [`ffmpeg`](https://ffmpeg.org/) en el PATH. La primera ejecución descarga el modelo `small` (~460 MB).

**Opciones del script:** `--modelo small|medium|large-v3` (por defecto `small`), `--idioma es|auto` (por defecto `es`), `--marcas` (marca de tiempo `[mm:ss]` por fragmento, útil en videos y audios largos).

**Velocidad orientativa** (CPU, modelo `small`): unos 20 s por minuto de audio; un video de 1 hora tarda unos 20 minutos.

## Licencia

MIT
