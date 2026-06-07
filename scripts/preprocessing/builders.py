from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from adapters import build_real_frame
from frame import SurvivalFrame
from logging_utils import log


def _synthetic_frame(dataset: str, censoring_rate: float, cfg: dict[str, Any]) -> SurvivalFrame:
    data_cfg = cfg.get("data_build", {})
    seq_len = int(data_cfg.get("sequence_length", 20))
    debug = bool(cfg.get("debug_small_run", False))
    n_units = 10 if debug else 48
    rng = np.random.default_rng(abs(hash((dataset, censoring_rate))) % (2**32))
    rows = []
    for unit in range(n_units):
        total_time = int(rng.integers(seq_len + 6, seq_len + 24))
        is_censored = rng.random() < censoring_rate
        censor_time = int(rng.integers(seq_len + 2, total_time)) if is_censored else total_time
        for anchor in range(max(3, censor_time - seq_len)):
            horizon = censor_time - anchor
            event = 0 if is_censored else 1
            rows.append((f"{dataset}_{unit}", anchor, horizon, event))
    n = len(rows)
    d_seq = 5
    p_static = 3
    x_seq = np.zeros((n, seq_len, d_seq), dtype=np.float32)
    seq_mask = np.ones((n, seq_len), dtype=np.float32)
    missing_mask = np.ones((n, seq_len, d_seq), dtype=np.float32)
    delta_t = np.tile(np.arange(seq_len, dtype=np.float32), (n, 1))
    x_static = np.zeros((n, p_static), dtype=np.float32)
    duration = np.zeros(n, dtype=np.float32)
    event = np.zeros(n, dtype=np.int64)
    event_type = np.zeros(n, dtype=np.int64)
    unit_id = np.empty(n, dtype=object)
    anchor_time = np.zeros(n, dtype=np.float32)
    for i, (unit, anchor, dur, ev) in enumerate(rows):
        trend = (anchor + np.arange(seq_len)) / max(anchor + dur, 1)
        noise = rng.normal(0, 0.06, size=(seq_len, d_seq))
        x_seq[i] = (trend[:, None] * np.linspace(0.7, 1.3, d_seq)[None, :] + noise).astype(np.float32)
        x_static[i] = np.array([len(unit), anchor % 7, censoring_rate], dtype=np.float32)
        duration[i] = max(float(dur), 1.0)
        event[i] = int(ev)
        event_type[i] = int(ev)
        unit_id[i] = unit
        anchor_time[i] = float(anchor)
    return SurvivalFrame(
        x_seq=x_seq,
        x_static=x_static,
        seq_mask=seq_mask,
        missing_mask=missing_mask,
        delta_t=delta_t,
        duration=duration,
        event=event,
        event_type=event_type,
        unit_id=unit_id,
        anchor_time=anchor_time,
        dataset_name=dataset,
        feature_names_seq=[f"sensor_{i}" for i in range(d_seq)],
        feature_names_static=["unit_name_length", "anchor_mod7", "admin_censoring_rate"],
        meta_json={
            "dataset": dataset,
            "censoring_rate": censoring_rate,
            "source": "synthetic_smoke_fallback",
            "note": "C-MAPSS censoring is simulated administrative censoring, not natural censoring.",
        },
    )


def build_survival_frame(
    dataset: str,
    censoring_rate: float,
    cfg: dict[str, Any],
    project_root: str | Path,
    force_rebuild: bool = False,
) -> tuple[SurvivalFrame, Path]:
    root = Path(project_root)
    tag = f"{dataset}_{censoring_rate:g}".replace(".", "p")
    out_path = root / "data" / "frames" / f"{tag}_frame.npz"
    if out_path.exists() and not force_rebuild:
        cached = SurvivalFrame.load_npz(out_path)
        synthetic_cached = bool(cached.meta_json.get("synthetic_fallback", False)) or cached.meta_json.get("source") == "synthetic_smoke_fallback"
        allow_synthetic = bool(cfg.get("data_build", {}).get("allow_synthetic_fallback", False))
        if not synthetic_cached or allow_synthetic:
            log("RESUME", f"loading cached frame {out_path}")
            return cached, out_path
        log("DATA", f"discarding synthetic cache for real build: {out_path}")

    log("DATA", f"Building frame for {dataset} censoring={censoring_rate}")
    allow_synthetic = bool(cfg.get("data_build", {}).get("allow_synthetic_fallback", False))
    try:
        result = build_real_frame(dataset, censoring_rate, cfg, root)
        frame = result.frame
        log("DATA", f"real adapter source={result.source_path}")
    except Exception as exc:
        if not allow_synthetic:
            raise RuntimeError(
                f"Real adapter failed for dataset={dataset}; synthetic fallback is disabled. Cause: {exc}"
            ) from exc
        log("DATA", f"real adapter failed; using explicit synthetic fallback because allow_synthetic_fallback=true: {exc}")
        frame = _synthetic_frame(dataset, censoring_rate, cfg)
    frame.save_npz(out_path)
    log("SAVE", f"frame saved to {out_path}")
    return frame, out_path


def audit_rows_to_table(rows: list[dict[str, Any]]) -> pd.DataFrame:
    keep = [
        "dataset",
        "censoring_rate",
        "n_rows",
        "n_units",
        "event_rate",
        "censoring_rate_actual",
        "duration_median",
        "padding_rate",
        "missingness_rate",
        "source_type",
        "synthetic_fallback",
        "short_sequence_fraction",
        "status",
    ]
    return pd.DataFrame([{key: row.get(key) for key in keep} for row in rows])
