# /// script
# requires-python = ">=3.10"
# dependencies = ["faster-whisper>=1.1"]
# ///
"""Transcribe audios y videos en local con faster-whisper.

Acepta todo lo que lea ffmpeg: notas de voz de WhatsApp (.ogg/.opus), mp3, m4a, wav, aac, flac,
y videos (mp4, mkv, mov, webm, avi...), de los que solo se usa la pista de audio.

Uso:
  uv run transcribir.py                       # la nota de voz de WhatsApp mas reciente de Descargas
  uv run transcribir.py a.mp3 reunion.mp4     # archivos concretos
  uv run transcribir.py --ultimas 3           # las 3 notas de voz mas recientes
Opciones: --modelo (small|medium|large-v3, por defecto small), --idioma (es por defecto, "auto" para detectar),
          --marcas (marca de tiempo [mm:ss] por fragmento; util en videos y audios largos).
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
    # -vn descarta el video: de un mp4/mkv solo interesa la pista de audio.
    import numpy as np
    r = subprocess.run(
        ["ffmpeg", "-nostdin", "-loglevel", "error", "-i", str(f), "-vn", "-f", "s16le", "-ac", "1", "-ar", "16000", "-"],
        capture_output=True,
    )
    if r.returncode != 0 or not r.stdout:
        err = r.stderr.decode(errors="replace").strip()
        motivo = "no tiene pista de audio" if not err or "does not contain any stream" in err else err.splitlines()[0]
        sys.exit(f"No se pudo leer el audio de {f.name}: {motivo}")
    return np.frombuffer(r.stdout, np.int16).astype(np.float32) / 32768.0


def mmss(s: float) -> str:
    m, s = divmod(int(s), 60)
    return f"{m // 60}:{m % 60:02d}:{s:02d}" if m >= 60 else f"{m:02d}:{s:02d}"


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("archivos", nargs="*", type=Path)
    ap.add_argument("--ultimas", type=int, default=1)
    ap.add_argument("--modelo", default="small")
    ap.add_argument("--idioma", default="es")
    ap.add_argument("--marcas", action="store_true")
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
        segmentos, info = modelo.transcribe(pcm16k(f), language=idioma, vad_filter=True)
        if a.marcas:
            texto = "\n".join(f"[{mmss(s.start)}] {s.text.strip()}" for s in segmentos)
        else:
            texto = " ".join(s.text.strip() for s in segmentos)
        print(f"### {f.name} ({mmss(info.duration)}, idioma {info.language})\n{texto or '(sin voz detectada)'}\n")


if __name__ == "__main__":
    main()
