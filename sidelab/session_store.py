# Architected and built by codieverse+.
from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any

from sidelab.llm import PROVIDER_REGISTRY

_DEFAULT_SESSIONS_DIR = Path(__file__).resolve().parent.parent / "sessions"


def backend_label(backend: str) -> str:
    return PROVIDER_REGISTRY.get(backend, {}).get("label", backend)


def save_session(
    history: list[dict[str, Any]],
    pasien: dict[str, Any],
    session_id: str,
    *,
    backend: str = "",
    model: str = "",
    sessions_dir: Path | str | None = None,
) -> Path:
    target_dir = Path(sessions_dir) if sessions_dir is not None else _DEFAULT_SESSIONS_DIR
    target_dir.mkdir(parents=True, exist_ok=True)

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = target_dir / f"sidelab_{ts}_{session_id}.txt"
    with filename.open("w", encoding="utf-8") as f:
        f.write(f"SIDELAB Session {session_id}\n")
        f.write(f"Tanggal: {datetime.now().strftime('%d %B %Y %H:%M')}\n")
        if backend:
            f.write(f"Backend: {backend_label(backend)}\n")
        if model:
            f.write(f"Model: {model}\n")
        if pasien and pasien.get("nama"):
            f.write(
                "Pasien: " + " | ".join(f"{k}: {v}" for k, v in pasien.items()) + "\n"
            )
        f.write("\n" + "=" * 60 + "\n\n")
        for msg in history:
            role = "DOKTER" if msg["role"] == "user" else "SIDELAB"
            f.write(f"{role}:\n{msg['content']}\n\n")
    return filename
