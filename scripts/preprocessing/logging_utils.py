from __future__ import annotations

from io_utils import now_utc


def log(stage: str, message: str) -> None:
    print(f"[{stage}] {now_utc()} {message}", flush=True)
