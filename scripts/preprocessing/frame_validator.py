from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from frame import SurvivalFrame
from io_utils import write_json
from logging_utils import log


FORBIDDEN_FEATURE_TOKENS = {
    "unit_id",
    "unit_number",
    "engine_id",
    "machine_id",
    "episode_id",
    "failure_time",
    "failure_datetime",
    "time_to_event",
    "remaining_useful_life",
    "rul",
    "rul_true",
    "rul_true",
    "duration",
    "event",
    "event_type",
    "censor_time",
}


def _fail(errors: list[str], message: str) -> None:
    errors.append(message)


def validate_frame(
    frame: SurvivalFrame,
    horizons: list[float],
    splits: dict[str, list[str]] | None = None,
    allow_short_sequences: bool = False,
) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    n, seq_len, d_seq = frame.x_seq.shape
    if frame.seq_mask.shape != (n, seq_len):
        _fail(errors, "seq_mask shape is incompatible with x_seq")
    if frame.missing_mask.shape != (n, seq_len, d_seq):
        _fail(errors, "missing_mask shape is incompatible with x_seq")
    if frame.delta_t.shape != (n, seq_len):
        _fail(errors, "delta_t shape is incompatible with x_seq")
    for name in ["duration", "event", "event_type", "unit_id", "anchor_time"]:
        if len(getattr(frame, name)) != n:
            _fail(errors, f"{name} length does not match N")
    if np.any(frame.duration <= 0):
        _fail(errors, "duration must be positive for all rows")
    if not np.all(np.isin(frame.event, [0, 1])):
        _fail(errors, "event must be in {0,1}")
    if np.any((frame.event == 0) & (frame.event_type != 0)):
        _fail(errors, "event_type must be 0 when event is censored")
    if np.any((frame.event == 1) & (frame.event_type < 1)):
        _fail(errors, "event_type must be >=1 when event is observed")
    for name, arr in [("x_seq", frame.x_seq), ("x_static", frame.x_static), ("delta_t", frame.delta_t)]:
        if not np.all(np.isfinite(arr)):
            _fail(errors, f"{name} contains NaN or Inf")
    if np.any(frame.delta_t < 0):
        _fail(errors, "delta_t must be non-negative")
    if list(horizons) != sorted(horizons) or any(float(h) <= 0 for h in horizons):
        _fail(errors, "risk horizons must be positive and sorted")
    feature_names = [*frame.feature_names_seq, *frame.feature_names_static]
    bad_features = [
        name for name in feature_names
        if any(token in name.lower() for token in FORBIDDEN_FEATURE_TOKENS)
    ]
    if bad_features:
        _fail(errors, f"leakage-prone feature names: {bad_features}")
    duplicated = pd.DataFrame({"unit_id": frame.unit_id.astype(str), "anchor_time": frame.anchor_time}).duplicated().sum()
    valid_steps = frame.seq_mask.sum(axis=1)
    padding_rate = float(1.0 - frame.seq_mask.mean())
    missingness_rate = float(1.0 - frame.missing_mask.mean())
    short_fraction = float(np.mean(valid_steps < 3))
    if short_fraction > 0:
        warnings.append(f"{short_fraction:.3f} rows have fewer than three valid timesteps")
    if padding_rate > 0.75 and not allow_short_sequences:
        _fail(errors, "padding rate is too high; set allow_short_sequences=true only for stress datasets")
    split_overlap = {}
    if splits:
        seen: dict[str, str] = {}
        for split_name, units in splits.items():
            for unit in units:
                if unit in seen:
                    split_overlap.setdefault(unit, []).extend([seen[unit], split_name])
                seen[unit] = split_name
        if split_overlap:
            _fail(errors, f"unit leakage across splits: {split_overlap}")
    audit = {
        "dataset": frame.dataset_name,
        "n_rows": int(n),
        "n_units": int(len(np.unique(frame.unit_id.astype(str)))),
        "n_seq_features": int(d_seq),
        "n_static_features": int(frame.x_static.shape[1]),
        "event_rate": float(np.mean(frame.event)),
        "censoring_rate_actual": float(1.0 - np.mean(frame.event)),
        "duration_min": float(np.min(frame.duration)),
        "duration_median": float(np.median(frame.duration)),
        "duration_max": float(np.max(frame.duration)),
        "valid_timestep_min": float(np.min(valid_steps)),
        "valid_timestep_median": float(np.median(valid_steps)),
        "valid_timestep_max": float(np.max(valid_steps)),
        "short_sequence_fraction": short_fraction,
        "padding_rate": padding_rate,
        "missingness_rate": missingness_rate,
        "duplicated_unit_anchor_rows": int(duplicated),
        "warnings": warnings,
        "errors": errors,
        "status": "passed" if not errors else "failed",
        "source_type": frame.meta_json.get("source_type", ""),
        "source": frame.meta_json.get("source", ""),
        "synthetic_fallback": bool(frame.meta_json.get("synthetic_fallback", False)),
        "notes": frame.meta_json,
    }
    return audit


def export_audit(audit: dict[str, Any], json_path: str | Path, csv_path: str | Path) -> None:
    write_json(json_path, audit)
    pd.DataFrame([audit]).to_csv(csv_path, index=False)
    log("AUDIT", f"{audit['status'].upper()} {audit['dataset']}")
