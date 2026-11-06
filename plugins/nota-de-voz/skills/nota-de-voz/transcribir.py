# /// script
# requires-python = ">=3.10"
# dependencies = ["faster-whisper>=1.1"]
# ///
"""Transcribe notas de voz (.ogg de WhatsApp u otro audio) en local con faster-whisper.

Uso:
  uv run transcribir.py                 # la nota de voz mas reciente de Descargas
  uv run transcribir.py a.ogg b.ogg     # archivos concretos
  uv run transcribir.py --ultimas 3     # las 3 mas recientes
Opciones: --modelo (small|medium|large-v3, por defecto small), --idioma (es por defecto, "auto" para detectar).
"""
import argparse
import subprocess
import sys
from pathlib import Path

DESCARGAS = Path.home() / "Downloads"


def recientes(n: int) -> list[Path]:
    notas = sorted(DESCARGAS.glob("WhatsApp Ptt*.ogg"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not notas:
        sys.exit(f"No hay notas de voz 'WhatsApp Ptt*.ogg' en {DESCARGAS}")
    return list(reversed(notas[:n]))  # en orden cronologico


def pcm16k(f: Path):
    # Decodifica con el ffmpeg del sistema: el PyAV que trae faster-whisper choca con av 15+.
    import numpy as np
    crudo = subprocess.run(
        ["ffmpeg", "-nostdin", "-loglevel", "error", "-i", str(f), "-f", "s16le", "-ac", "1", "-ar", "16000", "-"],
        capture_output=True, check=True,
    ).stdout
    return np.frombuffer(crudo, np.int16).astype(np.float32) / 32768.0


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("archivos", nargs="*", type=Path)
    ap.add_argument("--ultimas", type=int, default=1)
    ap.add_argument("--modelo", default="small")
    ap.add_argument("--idioma", default="es")
    a = ap.parse_args()

    archivos = a.archivos or recientes(a.ultimas)
    for f in archivos:
        if not f.is_file():
            sys.exit(f"No existe: {f}")

    from faster_whisper import WhisperModel  # import tardio: los errores de ruta salen antes de cargar el modelo

    # ponytail: CPU int8 fijo; si aparece una GPU NVIDIA, device="cuda" lo acelera mucho
    modelo = WhisperModel(a.modelo, device="cpu", compute_type="int8")
    idioma = None if a.idioma == "auto" else a.idioma
    for f in archivos:
        segmentos, info = modelo.transcribe(pcm16k(f),language=idioma, vad_filter=True)
        texto = " ".join(s.text.strip() for s in segmentos)
        print(f"### {f.name} ({info.duration:.0f} s, idioma {info.language})\n{texto}\n")


if __name__ == "__main__":
    main()
