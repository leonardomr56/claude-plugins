# claude-plugins

Plugins de Claude Code de Leonardo Melo.

## Instalar

```
/plugin marketplace add leonardomr56/claude-plugins
/plugin install nota-de-voz@leonardomr56-plugins
```

## Plugins

### nota-de-voz

Transcribe notas de voz de WhatsApp (`.ogg`) en tu máquina y usa lo que dicen como base de una petición.

```
/nota-de-voz:nota-de-voz                          # la nota más reciente de Descargas
/nota-de-voz:nota-de-voz crea la tarea con esto
/nota-de-voz:nota-de-voz --ultimas 3 resúmelas
/nota-de-voz:nota-de-voz "C:\ruta\audio.ogg"
```

- Transcripción local con [faster-whisper](https://github.com/SYSTRAN/faster-whisper): el audio no sale de tu máquina y no hay costo por uso.
- Incluye el agente `transcriptor-voz` (modelo Haiku), que devuelve el texto literal, una versión limpia, la petición y los datos clave.
- Antes de hacer algo fuera de la sesión (crear tareas, enviar mensajes) pregunta, salvo que se lo pidas al invocarla.

**Requisitos:** [`uv`](https://docs.astral.sh/uv/) y [`ffmpeg`](https://ffmpeg.org/) en el PATH. La primera ejecución descarga el modelo `small` (~460 MB).

**Opciones del script:** `--modelo small|medium|large-v3` (por defecto `small`), `--idioma es|auto` (por defecto `es`).

## Licencia

MIT
