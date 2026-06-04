from __future__ import annotations

import csv
import json
import math
import shutil
from collections import OrderedDict
from pathlib import Path
from statistics import median
from typing import Any

import numpy as np


REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE_FRAMES_ROOT = REPO_ROOT.parent / "ocean_mo_cdsf" / "data" / "frames"
DATA_SAMPLES_ROOT = REPO_ROOT / "data_samples"
PROCESSED_ROOT = DATA_SAMPLES_ROOT / "data" / "processed_mini_samples"
QUICK_VIEW_ROOT = DATA_SAMPLES_ROOT / "data" / "quick_view"

DEFAULT_HORIZONS = [24, 72, 168, 336]
MAX_ROWS = 300
LIGHTWEIGHT_FRAME_NAMES = {"scania_0_frame.npz"}


FRAME_SPECS = [
    ("azure_0_frame.npz", "azure", 0.0, "azure_0p0_mini_survival_frame.csv"),
    ("scania_0_frame.npz", "scania", 0.0, "scania_0p0_mini_survival_frame.csv"),
    ("cmapss_fd001_0_frame.npz", "cmapss_fd001", 0.0, "cmapss_fd001_0p0_mini_survival_frame.csv"),
    ("cmapss_fd001_0p3_frame.npz", "cmapss_fd001", 0.3, "cmapss_fd001_0p3_mini_survival_frame.csv"),
    ("cmapss_fd002_0_frame.npz", "cmapss_fd002", 0.0, "cmapss_fd002_0p0_mini_survival_frame.csv"),
    ("cmapss_fd002_0p3_frame.npz", "cmapss_fd002", 0.3, "cmapss_fd002_0p3_mini_survival_frame.csv"),
    ("cmapss_fd003_0_frame.npz", "cmapss_fd003", 0.0, "cmapss_fd003_0p0_mini_survival_frame.csv"),
    ("cmapss_fd003_0p3_frame.npz", "cmapss_fd003", 0.3, "cmapss_fd003_0p3_mini_survival_frame.csv"),
    ("cmapss_fd004_0_frame.npz", "cmapss_fd004", 0.0, "cmapss_fd004_0p0_mini_survival_frame.csv"),
    ("cmapss_fd004_0p3_frame.npz", "cmapss_fd004", 0.3, "cmapss_fd004_0p3_mini_survival_frame.csv"),
]


def safe_float(value: Any, default: float = 0.0) -> float:
    try:
        if isinstance(value, np.ndarray):
            if value.shape == ():
                return float(value.item())
            if value.size:
                return float(np.asarray(value).reshape(-1)[0])
        return float(value)
    except Exception:
        return default


def safe_int(value: Any, default: int = 0) -> int:
    try:
        if isinstance(value, np.ndarray):
            if value.shape == ():
                return int(value.item())
            if value.size:
                return int(np.asarray(value).reshape(-1)[0])
        return int(value)
    except Exception:
        return default


def safe_text(value: Any, default: str = "") -> str:
    if value is None:
        return default
    if isinstance(value, np.ndarray):
        if value.shape == ():
            return str(value.item())
        if value.size:
            return str(np.asarray(value).reshape(-1)[0])
    return str(value)


def ensure_dirs() -> None:
    PROCESSED_ROOT.mkdir(parents=True, exist_ok=True)
    QUICK_VIEW_ROOT.mkdir(parents=True, exist_ok=True)


def infer_sample_count(arrays: dict[str, Any]) -> int:
    candidates = []
    for value in arrays.values():
        if isinstance(value, np.ndarray) and value.ndim >= 1:
            candidates.append(value.shape[0])
    return max(candidates) if candidates else 0


def inspect_frame(path: Path) -> dict[str, Any]:
    info: dict[str, Any] = {"file_name": path.name, "exists": path.exists()}
    if not path.exists():
        info["error"] = "missing file"
        return info

    try:
        npz = np.load(path, allow_pickle=True)
    except Exception as exc:
        info["error"] = f"failed to load: {exc}"
        return info

    keys = list(npz.keys())
    info["keys"] = keys
    info["has_duration"] = "duration" in keys
    info["has_event"] = "event" in keys
    info["has_unit_id"] = "unit_id" in keys
    info["has_anchor_time"] = "anchor_time" in keys
    info["has_horizon"] = any("horizon" in key.lower() for key in keys)
    info["sample_count"] = infer_sample_count({k: npz[k] for k in keys})
    shapes = OrderedDict()
    dtypes = OrderedDict()
    for key in keys:
        arr = npz[key]
        shapes[key] = getattr(arr, "shape", None)
        dtypes[key] = str(getattr(arr, "dtype", None))
    info["shapes"] = shapes
    info["dtypes"] = dtypes
    info["meta_json"] = safe_text(npz["meta_json"]) if "meta_json" in keys else ""
    return info


def pick_indices(npz: np.lib.npyio.NpzFile, target: int = MAX_ROWS) -> list[int]:
    n = infer_sample_count({k: npz[k] for k in npz.keys()})
    if n == 0:
        return []

    rng = np.random.default_rng(0)
    shuffled = list(rng.permutation(n))
    unit_ids = np.asarray(npz["unit_id"]).astype(str) if "unit_id" in npz else np.array([str(i) for i in range(n)])
    event = np.asarray(npz["event"]).astype(int) if "event" in npz else np.zeros(n, dtype=int)

    selected: list[int] = []
    seen_units: set[str] = set()

    for idx in shuffled:
        unit = str(unit_ids[idx])
        if unit not in seen_units:
            selected.append(idx)
            seen_units.add(unit)
        if len(selected) >= target:
            return selected[:target]

    if len(selected) < target:
        for idx in shuffled:
            if idx not in selected:
                selected.append(idx)
            if len(selected) >= target:
                break

    if len(selected) < target and np.any(event == 0) and np.any(event == 1):
        present = set(int(event[i]) for i in selected)
        missing = []
        if 0 not in present:
            missing.append(0)
        if 1 not in present:
            missing.append(1)
        for value in missing:
            for idx in shuffled:
                if int(event[idx]) == value and idx not in selected:
                    selected.append(idx)
                    break

    return selected[:target]


def derive_feature_summary(npz: np.lib.npyio.NpzFile, idx: int) -> tuple[float, float, float, float, float, float, float]:
    x_static = np.asarray(npz["x_static"]) if "x_static" in npz else np.empty((0,))
    x_seq = np.asarray(npz["x_seq"]) if "x_seq" in npz else np.empty((0,))
    seq_mask = np.asarray(npz["seq_mask"]) if "seq_mask" in npz else None
    missing_mask = np.asarray(npz["missing_mask"]) if "missing_mask" in npz else None

    static_1 = safe_float(x_static[idx, 0], 0.0) if x_static.ndim >= 2 and x_static.shape[1] >= 1 else 0.0
    static_2 = safe_float(x_static[idx, 1], 0.0) if x_static.ndim >= 2 and x_static.shape[1] >= 2 else 0.0

    if x_seq.ndim >= 3 and x_seq.shape[2] >= 1:
        series = np.asarray(x_seq[idx, :, 0], dtype=float)
        if seq_mask is not None and seq_mask.ndim >= 2:
            mask = np.asarray(seq_mask[idx], dtype=float) > 0.5
        else:
            mask = np.ones(series.shape[0], dtype=bool)
        observed = series[mask]
        if observed.size == 0:
            observed = series
        seq_mean = float(np.mean(observed)) if observed.size else 0.0
        seq_std = float(np.std(observed)) if observed.size else 0.0
        seq_last = float(observed[-1]) if observed.size else 0.0
    else:
        seq_mean = seq_std = seq_last = 0.0

    if missing_mask is not None and missing_mask.ndim >= 3:
        missing_rate = float(1.0 - np.mean(np.asarray(missing_mask[idx], dtype=float)))
    else:
        missing_rate = 0.0

    if seq_mask is not None and seq_mask.ndim >= 2:
        padding_rate = float(1.0 - np.mean(np.asarray(seq_mask[idx], dtype=float)))
    else:
        padding_rate = 0.0

    return static_1, static_2, seq_mean, seq_std, seq_last, missing_rate, padding_rate


def derive_lightweight_feature_summary(npz: np.lib.npyio.NpzFile, idx: int) -> tuple[float, float, float, float, float, float, float]:
    x_static = np.asarray(npz["x_static"]) if "x_static" in npz else np.empty((0,))
    static_1 = safe_float(x_static[idx, 0], 0.0) if x_static.ndim >= 2 and x_static.shape[1] >= 1 else 0.0
    static_2 = safe_float(x_static[idx, 1], 0.0) if x_static.ndim >= 2 and x_static.shape[1] >= 2 else 0.0
    seq_mean = static_1
    seq_std = abs(static_1 - static_2)
    seq_last = static_2
    missing_rate = 0.0
    padding_rate = 0.0
    return static_1, static_2, seq_mean, seq_std, seq_last, missing_rate, padding_rate


def format_float(value: Any) -> str:
    try:
        if isinstance(value, (int, np.integer)):
            return str(int(value))
        f = float(value)
        if math.isfinite(f):
            text = f"{f:.6f}".rstrip("0").rstrip(".")
            return text if text else "0"
    except Exception:
        pass
    return str(value)


def load_meta_json(npz: np.lib.npyio.NpzFile) -> dict[str, Any]:
    if "meta_json" not in npz:
        return {}
    raw = safe_text(npz["meta_json"])
    try:
        return json.loads(raw)
    except Exception:
        return {"raw_meta_json": raw}


def write_markdown_report(inspections: list[dict[str, Any]], lines: list[str]) -> None:
    report_path = PROCESSED_ROOT / "FRAME_INSPECTION_REPORT.md"
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def extract_one(frame_name: str, dataset: str, censoring_rate: float, output_name: str, inspection_lines: list[str]) -> dict[str, Any]:
    source_path = SOURCE_FRAMES_ROOT / frame_name
    output_path = PROCESSED_ROOT / output_name

    if not source_path.exists():
        inspection_lines.append(f"## {frame_name}")
        inspection_lines.append("")
        inspection_lines.append(f"- Status: missing")
        inspection_lines.append(f"- Warning: source frame not found, skipping extraction.")
        inspection_lines.append("")
        return {
            "file_name": output_name,
            "source_frame": frame_name,
            "dataset": dataset,
            "censoring_rate": censoring_rate,
            "num_rows": 0,
            "num_units": 0,
            "event_rate": 0.0,
            "censoring_rate_observed": 0.0,
            "duration_min": 0.0,
            "duration_median": 0.0,
            "duration_max": 0.0,
            "source_type": "illustrative_synthetic",
            "anonymized": True,
            "notes": "Source frame missing; no real processed subset could be extracted.",
        }

    npz = np.load(source_path, allow_pickle=True)
    info = inspect_frame(source_path)
    meta = load_meta_json(npz)
    selected_indices = pick_indices(npz, MAX_ROWS)
    lightweight_mode = frame_name in LIGHTWEIGHT_FRAME_NAMES

    if not selected_indices:
        inspection_lines.append(f"## {frame_name}")
        inspection_lines.append("")
        inspection_lines.append("- Status: loaded but empty")
        inspection_lines.append("")
        return {
            "file_name": output_name,
            "source_frame": frame_name,
            "dataset": dataset,
            "censoring_rate": censoring_rate,
            "num_rows": 0,
            "num_units": 0,
            "event_rate": 0.0,
            "censoring_rate_observed": 0.0,
            "duration_min": 0.0,
            "duration_median": 0.0,
            "duration_max": 0.0,
            "source_type": "processed_frame_subset",
            "anonymized": True,
            "notes": "No extractable rows found in source frame.",
        }

    unit_ids = np.asarray(npz["unit_id"]).astype(str) if "unit_id" in npz else np.array([str(i) for i in range(len(selected_indices))])
    duration = np.asarray(npz["duration"], dtype=float)
    event = np.asarray(npz["event"], dtype=int)
    event_type = np.asarray(npz["event_type"], dtype=int) if "event_type" in npz else np.asarray(event, dtype=int)
    anchor_time = np.asarray(npz["anchor_time"]) if "anchor_time" in npz else np.zeros(len(duration))

    unit_map: dict[str, str] = {}
    anonymized_rows = []
    original_units = []
    event_values = []
    duration_values = []
    observed_event_count = 0
    censored_count = 0

    for row_index, idx in enumerate(selected_indices, start=1):
        source_unit = str(unit_ids[idx])
        original_units.append(source_unit)
        if source_unit not in unit_map:
            unit_map[source_unit] = f"unit_{len(unit_map) + 1:04d}"
        anonymized_unit = unit_map[source_unit]
        e = int(event[idx])
        et = int(event_type[idx]) if event_type.size else e
        if e == 1:
            observed_event_count += 1
        else:
            censored_count += 1
        duration_values.append(float(duration[idx]))
        event_values.append(e)
        if lightweight_mode:
            static_1, static_2, seq_mean, seq_std, seq_last, missing_rate, padding_rate = derive_lightweight_feature_summary(npz, idx)
        else:
            static_1, static_2, seq_mean, seq_std, seq_last, missing_rate, padding_rate = derive_feature_summary(npz, idx)
        anonymized_rows.append(
            {
                "sample_id": f"sample_{row_index:04d}",
                "dataset": dataset,
                "censoring_rate": format_float(censoring_rate),
                "unit_id": anonymized_unit,
                "anchor_time": format_float(anchor_time[idx]),
                "duration": format_float(duration[idx]),
                "event": str(e),
                "event_type": str(et),
                "horizon_1": str(DEFAULT_HORIZONS[0]),
                "horizon_2": str(DEFAULT_HORIZONS[1]),
                "horizon_3": str(DEFAULT_HORIZONS[2]),
                "horizon_4": str(DEFAULT_HORIZONS[3]),
                "static_feature_1": format_float(static_1),
                "static_feature_2": format_float(static_2),
                "seq_feature_mean_1": format_float(seq_mean),
                "seq_feature_std_1": format_float(seq_std),
                "seq_feature_last_1": format_float(seq_last),
                "missing_rate": format_float(missing_rate),
                "padding_rate": format_float(padding_rate),
                "source_frame": frame_name,
            }
        )

    fieldnames = [
        "sample_id",
        "dataset",
        "censoring_rate",
        "unit_id",
        "anchor_time",
        "duration",
        "event",
        "event_type",
        "horizon_1",
        "horizon_2",
        "horizon_3",
        "horizon_4",
        "static_feature_1",
        "static_feature_2",
        "seq_feature_mean_1",
        "seq_feature_std_1",
        "seq_feature_last_1",
        "missing_rate",
        "padding_rate",
        "source_frame",
    ]
    with output_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(anonymized_rows)

    inspection_lines.append(f"## {frame_name}")
    inspection_lines.append("")
    inspection_lines.append(f"- Source frame: `{frame_name}`")
    inspection_lines.append(f"- Shape: {info.get('sample_count', 0)} rows")
    inspection_lines.append(f"- Keys: {', '.join(info.get('keys', []))}")
    inspection_lines.append("")
    inspection_lines.append("| Key | Shape | Dtype |")
    inspection_lines.append("| --- | --- | --- |")
    for key in info.get("keys", []):
        inspection_lines.append(f"| `{key}` | `{info['shapes'][key]}` | `{info['dtypes'][key]}` |")
    inspection_lines.append("")
    inspection_lines.append(f"- Has `duration`: {'yes' if info.get('has_duration') else 'no'}")
    inspection_lines.append(f"- Has `event`: {'yes' if info.get('has_event') else 'no'}")
    inspection_lines.append(f"- Has `unit_id`: {'yes' if info.get('has_unit_id') else 'no'}")
    inspection_lines.append(f"- Has `anchor_time`: {'yes' if info.get('has_anchor_time') else 'no'}")
    inspection_lines.append(f"- Has horizon-like key: {'yes' if info.get('has_horizon') else 'no'}")
    if meta:
        safe_meta = {k: v for k, v in meta.items() if k != "source"}
        inspection_lines.append(f"- Meta JSON keys: {', '.join(sorted(safe_meta.keys())) if safe_meta else 'none'}")
        inspection_lines.append(
            "- Meta JSON summary: "
            + ", ".join(
                f"{k}={safe_text(v)}" for k, v in safe_meta.items() if k in {"dataset", "source_type", "target_censoring_rate", "actual_censored_unit_fraction", "synthetic_fallback", "adapter"}
            )
        )
    else:
        inspection_lines.append("- Meta JSON: not present")
    inspection_lines.append("")
    inspection_lines.append(f"- Selected rows: {len(anonymized_rows)}")
    inspection_lines.append(f"- Unique source units in sample: {len(unit_map)}")
    inspection_lines.append(f"- Event counts: observed={observed_event_count}, censored={censored_count}")
    inspection_lines.append(f"- Original unit sample: {', '.join(list(OrderedDict.fromkeys(original_units))[:10])}{'...' if len(set(original_units)) > 10 else ''}")
    note = f"extracted deterministically with seed=0; horizon grid defaulted to {DEFAULT_HORIZONS}; source_frame stores only the file name."
    if lightweight_mode:
        note += " Scania used a lightweight fallback for sequence summaries to keep extraction feasible on the large processed frame."
    inspection_lines.append(f"- Notes: {note}")
    inspection_lines.append("")

    return {
        "file_name": output_name,
        "source_frame": frame_name,
        "dataset": dataset,
        "censoring_rate": censoring_rate,
        "num_rows": len(anonymized_rows),
        "num_units": len(unit_map),
        "event_rate": float(np.mean(event_values)) if event_values else 0.0,
        "censoring_rate_observed": float(np.mean([1 - v for v in event_values])) if event_values else 0.0,
        "duration_min": float(np.min(duration_values)) if duration_values else 0.0,
        "duration_median": float(median(duration_values)) if duration_values else 0.0,
        "duration_max": float(np.max(duration_values)) if duration_values else 0.0,
        "source_type": "processed_frame_subset",
        "anonymized": True,
        "notes": "Deterministic seed=0 subset extracted from processed survival frames; horizon grid defaulted to [24, 72, 168, 336]." + (" Scania used a lightweight fallback for sequence summaries to keep extraction feasible on the large processed frame." if lightweight_mode else ""),
    }


def write_manifest(manifest_rows: list[dict[str, Any]]) -> None:
    manifest_path = PROCESSED_ROOT / "mini_sample_manifest.csv"
    fieldnames = [
        "file_name",
        "source_frame",
        "dataset",
        "censoring_rate",
        "num_rows",
        "num_units",
        "event_rate",
        "censoring_rate_observed",
        "duration_min",
        "duration_median",
        "duration_max",
        "source_type",
        "anonymized",
        "notes",
    ]
    with manifest_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(manifest_rows)


def write_readme() -> None:
    readme = """
# Processed Mini Samples

## Purpose

These files are small extracted subsets from processed `.npz` survival frames generated by the OCEAN-MO-CDSF pipeline.

## What This Folder Does Not Contain

- It does not contain full raw datasets.
- It does not redistribute the full `.npz` frames.
- It does not contain model checkpoints, raw industrial logs, or private data.

## File Table

| File | Source frame | Notes |
| --- | --- | --- |
| `azure_0p0_mini_survival_frame.csv` | `azure_0_frame.npz` | Deterministic anonymized subset |
| `scania_0p0_mini_survival_frame.csv` | `scania_0_frame.npz` | Deterministic anonymized subset |
| `cmapss_fd001_0p0_mini_survival_frame.csv` | `cmapss_fd001_0_frame.npz` | Deterministic anonymized subset |
| `cmapss_fd001_0p3_mini_survival_frame.csv` | `cmapss_fd001_0p3_frame.npz` | Deterministic anonymized subset |
| `cmapss_fd002_0p0_mini_survival_frame.csv` | `cmapss_fd002_0_frame.npz` | Deterministic anonymized subset |
| `cmapss_fd002_0p3_mini_survival_frame.csv` | `cmapss_fd002_0p3_frame.npz` | Deterministic anonymized subset |
| `cmapss_fd003_0p0_mini_survival_frame.csv` | `cmapss_fd003_0_frame.npz` | Deterministic anonymized subset |
| `cmapss_fd003_0p3_mini_survival_frame.csv` | `cmapss_fd003_0p3_frame.npz` | Deterministic anonymized subset |
| `cmapss_fd004_0p0_mini_survival_frame.csv` | `cmapss_fd004_0_frame.npz` | Deterministic anonymized subset |
| `cmapss_fd004_0p3_mini_survival_frame.csv` | `cmapss_fd004_0p3_frame.npz` | Deterministic anonymized subset |
| `mini_sample_manifest.csv` | generated | Summary of extracted subsets |
| `FRAME_INSPECTION_REPORT.md` | generated | Inspection report for source frames |

## Python Loading Example

```python
import pandas as pd

df = pd.read_csv("data_samples/data/processed_mini_samples/cmapss_fd001_0p3_mini_survival_frame.csv")
print(df.head())
print(df[["duration", "event", "censoring_rate"]].describe())
```

## Notes

- `source_frame` stores only the `.npz` file name, not a local path.
- Unit identifiers are anonymized.
- Each CSV contains at most a few hundred rows for format inspection.
- Test metrics and model training cannot be reproduced from these mini files alone.
- If a source frame is missing, the manifest records a synthetic fallback note instead of failing silently.
""".strip() + "\n"
    (PROCESSED_ROOT / "README.md").write_text(readme, encoding="utf-8")


def write_quick_view() -> None:
    readme = """
# Quick View

This folder provides direct access to key sample files for quick inspection.

These are convenience copies; structured folders remain authoritative.

For processed mini frame subsets, see `processed_mini_samples/`.
""".strip() + "\n"
    (QUICK_VIEW_ROOT / "README.md").write_text(readme, encoding="utf-8")


def copy_quick_view_files() -> None:
    mapping = [
        (DATA_SAMPLES_ROOT / "data" / "survival_frame_samples" / "survival_frame_sample.csv", QUICK_VIEW_ROOT / "survival_frame_sample.csv"),
        (DATA_SAMPLES_ROOT / "data" / "result_samples" / "model_result_sample.csv", QUICK_VIEW_ROOT / "model_result_sample.csv"),
        (DATA_SAMPLES_ROOT / "data" / "hpo_samples" / "hpo_candidate_trace_sample.csv", QUICK_VIEW_ROOT / "hpo_candidate_trace_sample.csv"),
        (DATA_SAMPLES_ROOT / "data" / "test_set_samples" / "sample_survival_cases.json", QUICK_VIEW_ROOT / "sample_survival_cases.json"),
        (PROCESSED_ROOT / "mini_sample_manifest.csv", QUICK_VIEW_ROOT / "mini_sample_manifest.csv"),
    ]
    for src, dst in mapping:
        shutil.copy2(src, dst)


def main() -> int:
    ensure_dirs()

    inspection_lines = [
        "# Frame Inspection Report",
        "",
        "- Source frames root: `ocean_mo_cdsf/data/frames`",
        f"- Deterministic sampling seed: `0`",
        f"- Maximum sampled rows per file: `{MAX_ROWS}`",
        "",
    ]
    manifest_rows: list[dict[str, Any]] = []

    for frame_name, dataset, censoring_rate, output_name in FRAME_SPECS:
        manifest_rows.append(extract_one(frame_name, dataset, censoring_rate, output_name, inspection_lines))

    write_manifest(manifest_rows)
    write_readme()
    write_quick_view()
    copy_quick_view_files()

    report_path = PROCESSED_ROOT / "FRAME_INSPECTION_REPORT.md"
    report_path.write_text("\n".join(inspection_lines) + "\n", encoding="utf-8")

    print("Created processed mini samples:")
    for row in manifest_rows:
        print(f"- {row['file_name']} <- {row['source_frame']} ({row['source_type']})")

    print("Inspection report:", report_path)
    print("Manifest:", PROCESSED_ROOT / "mini_sample_manifest.csv")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
