from __future__ import annotations

from dataclasses import dataclass
import hashlib
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from frame import SurvivalFrame


LABEL_COLUMNS = {
    "dataset",
    "split",
    "datetime",
    "time_index",
    "time_cycle",
    "entity_id",
    "unit_id",
    "unit_number",
    "machineid",
    "machineID",
    "episode_id",
    "failure_time",
    "failure_datetime",
    "time_to_event",
    "remaining_useful_life",
    "next_failure_time",
    "censor_time",
    "duration",
    "event",
    "event_type",
    "rul_true",
    "rul",
    "RUL",
    "RUL_true",
}


@dataclass
class AdapterResult:
    frame: SurvivalFrame
    source_path: Path


def build_real_frame(dataset: str, censoring_rate: float, cfg: dict[str, Any], project_root: Path) -> AdapterResult:
    source_path = _find_source_csv(dataset, cfg, project_root)
    if source_path is None:
        roots = _candidate_roots(dataset, cfg, project_root)
        raise FileNotFoundError(
            f"No real CSV found for dataset={dataset}. Checked: {[str(path) for path in roots]}"
        )
    df = pd.read_csv(source_path)
    if df.empty:
        raise ValueError(f"Raw CSV is empty: {source_path}")
    if dataset.startswith("cmapss_"):
        frame = _build_cmapss(dataset, df, censoring_rate, cfg, source_path)
    elif dataset == "azure":
        frame = _build_azure(dataset, df, censoring_rate, cfg, source_path)
    elif dataset == "scania":
        frame = _build_scania(dataset, df, censoring_rate, cfg, source_path)
    else:
        raise ValueError(f"Unsupported dataset adapter: {dataset}")
    return AdapterResult(frame=frame, source_path=source_path)


def _candidate_roots(dataset: str, cfg: dict[str, Any], project_root: Path) -> list[Path]:
    roots = []
    for raw_root in cfg.get("raw_roots", []):
        path = Path(raw_root)
        roots.append(path if path.is_absolute() else project_root / path)
    roots.extend([
        project_root / "data" / "raw" / dataset,
    ])
    return roots


def _find_source_csv(dataset: str, cfg: dict[str, Any], project_root: Path) -> Path | None:
    expected = {
        "azure": "azure_pdm.csv",
        "scania": "scania_survival_samples.csv",
    }.get(dataset, f"{dataset}.csv")
    for root in _candidate_roots(dataset, cfg, project_root):
        candidates = [root / expected, *root.glob("*.csv")] if root.exists() else []
        for path in candidates:
            if path.exists() and path.is_file():
                return path
    return None


def _numeric_time(values: pd.Series) -> np.ndarray:
    if np.issubdtype(values.dtype, np.number):
        return pd.to_numeric(values, errors="coerce").to_numpy(dtype=float)
    parsed = pd.to_datetime(values, errors="coerce")
    if parsed.notna().any():
        first = parsed.dropna().min()
        hours = (parsed - first).dt.total_seconds() / 3600.0
        return hours.ffill().fillna(0).to_numpy(dtype=float)
    return pd.factorize(values.astype(str))[0].astype(float)


def _feature_columns(df: pd.DataFrame) -> list[str]:
    label_names = {name.lower() for name in LABEL_COLUMNS}
    cols = []
    for col in df.columns:
        if col in LABEL_COLUMNS or col.lower() in label_names:
            continue
        if pd.api.types.is_numeric_dtype(df[col]) or pd.api.types.is_bool_dtype(df[col]):
            cols.append(col)
    return cols


def _static_columns(df: pd.DataFrame, feature_cols: list[str]) -> list[str]:
    return [col for col in feature_cols if col.startswith("spec_") or col in {"age", "error_count"}]


def _frame_from_landmarks(
    dataset: str,
    df: pd.DataFrame,
    unit_col: str,
    time_col: str,
    duration: np.ndarray,
    event: np.ndarray,
    feature_cols: list[str],
    static_cols: list[str],
    cfg: dict[str, Any],
    meta: dict[str, Any],
) -> SurvivalFrame:
    data_cfg = cfg.get("data_build", {})
    seq_len = int(data_cfg.get("sequence_length", 20))
    stride = max(1, int(data_cfg.get("stride", 5)))
    max_anchors = data_cfg.get("max_anchors_per_unit", 500)
    max_anchors = None if max_anchors in {None, "none", "None"} else int(max_anchors)
    work = df.copy()
    work["_duration"] = duration.astype(float)
    work["_event"] = event.astype(int)
    work["_time_num"] = _numeric_time(work[time_col])
    work = work[np.isfinite(work["_duration"]) & (work["_duration"] > 0)].copy()
    work = work.sort_values([unit_col, "_time_num"]).reset_index(drop=True)
    features = work[feature_cols].apply(pd.to_numeric, errors="coerce").astype(float)
    missing_raw = features.notna().astype(np.float32).to_numpy()
    features = features.replace([np.inf, -np.inf], np.nan).fillna(0.0)
    static_cols = [col for col in static_cols if col in features.columns]
    seq_cols = [col for col in feature_cols if col not in static_cols]
    if not seq_cols:
        seq_cols = feature_cols
        static_cols = []
    seq_values = features[seq_cols].to_numpy(dtype=np.float32)
    seq_missing = missing_raw[:, [feature_cols.index(col) for col in seq_cols]]
    static_values = (
        features[static_cols].to_numpy(dtype=np.float32)
        if static_cols
        else np.zeros((len(work), 1), dtype=np.float32)
    )
    static_names = static_cols if static_cols else ["bias_static"]

    anchors: list[int] = []
    for _, group in work.groupby(unit_col, sort=False):
        idxs = group.index.to_numpy()
        valid = idxs[seq_len - 1 :: stride] if len(idxs) >= seq_len else idxs[-1:]
        if max_anchors is not None and len(valid) > max_anchors:
            take = np.unique(np.round(np.linspace(0, len(valid) - 1, max_anchors)).astype(int))
            valid = valid[take]
        anchors.extend(valid.tolist())
    if not anchors:
        raise ValueError(f"No valid anchors generated for {dataset}")

    n = len(anchors)
    d_seq = len(seq_cols)
    x_seq = np.zeros((n, seq_len, d_seq), dtype=np.float32)
    seq_mask = np.zeros((n, seq_len), dtype=np.float32)
    missing_mask = np.zeros((n, seq_len, d_seq), dtype=np.float32)
    delta_t = np.zeros((n, seq_len), dtype=np.float32)
    x_static = np.zeros((n, len(static_names)), dtype=np.float32)
    out_duration = np.zeros(n, dtype=np.float32)
    out_event = np.zeros(n, dtype=np.int64)
    unit_id = np.empty(n, dtype=object)
    anchor_time = np.zeros(n, dtype=np.float32)
    row_unit = work[unit_col].astype(str).to_numpy()
    row_time = work["_time_num"].to_numpy(dtype=float)
    for out_i, row_i in enumerate(anchors):
        unit = row_unit[row_i]
        unit_positions = np.where(row_unit[: row_i + 1] == unit)[0]
        hist = unit_positions[-seq_len:]
        start = seq_len - len(hist)
        x_seq[out_i, start:] = seq_values[hist]
        missing_mask[out_i, start:] = seq_missing[hist]
        seq_mask[out_i, start:] = 1.0
        times = row_time[hist]
        delta_t[out_i, start:] = np.maximum(0.0, row_time[row_i] - times)
        x_static[out_i] = static_values[row_i]
        out_duration[out_i] = float(work.at[row_i, "_duration"])
        out_event[out_i] = int(work.at[row_i, "_event"])
        unit_id[out_i] = unit
        anchor_time[out_i] = float(row_time[row_i])
    event_type = np.where(out_event == 1, 1, 0).astype(np.int64)
    return SurvivalFrame(
        x_seq=x_seq,
        x_static=x_static,
        seq_mask=seq_mask,
        missing_mask=missing_mask,
        delta_t=delta_t,
        duration=out_duration,
        event=out_event,
        event_type=event_type,
        unit_id=unit_id,
        anchor_time=anchor_time,
        dataset_name=dataset,
        feature_names_seq=[str(col) for col in seq_cols],
        feature_names_static=[str(col) for col in static_names],
        meta_json=meta,
    )


def azure_episode_audit_table(df: pd.DataFrame) -> pd.DataFrame:
    required = {"entity_id", "time_index", "event"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Azure episode audit missing required columns: {sorted(missing)}")
    work = df[["entity_id", "time_index", "event"]].copy()
    work["_time_dt"] = pd.to_datetime(work["time_index"], errors="coerce")
    if work["_time_dt"].isna().any():
        raise ValueError("Azure episode audit requires parseable datetime time_index values")
    work["_event"] = pd.to_numeric(work["event"], errors="coerce").fillna(0).astype(int).clip(0, 1)
    rows: list[dict[str, Any]] = []
    for unit, group in work.sort_values(["entity_id", "_time_dt"]).groupby("entity_id", sort=False):
        times = group["_time_dt"]
        censor_time = times.max()
        start_time = times.min()
        failure_times = sorted(group.loc[group["_event"] == 1, "_time_dt"].dropna().unique())
        episode_start = start_time
        for episode_id, failure_time in enumerate(failure_times):
            failure_ts = pd.Timestamp(failure_time)
            duration = max((failure_time - episode_start).total_seconds() / 3600.0, 0.0)
            rows.append({
                "unit_id": str(unit),
                "episode_id": int(episode_id),
                "start_time": pd.Timestamp(episode_start).isoformat(),
                "end_time": failure_ts.isoformat(),
                "next_failure_time": failure_ts.isoformat(),
                "censor_time": pd.Timestamp(censor_time).isoformat(),
                "event": 1,
                "duration": duration,
            })
            episode_start = failure_ts
        if episode_start < censor_time:
            rows.append({
                "unit_id": str(unit),
                "episode_id": int(len(failure_times)),
                "start_time": pd.Timestamp(episode_start).isoformat(),
                "end_time": pd.Timestamp(censor_time).isoformat(),
                "next_failure_time": "",
                "censor_time": pd.Timestamp(censor_time).isoformat(),
                "event": 0,
                "duration": max((censor_time - episode_start).total_seconds() / 3600.0, 0.0),
            })
    return pd.DataFrame(rows)


def _azure_row_targets(df: pd.DataFrame) -> tuple[np.ndarray, np.ndarray, dict[str, Any]]:
    work = df[["entity_id", "time_index", "event"]].copy()
    work["_time_dt"] = pd.to_datetime(work["time_index"], errors="coerce")
    if work["_time_dt"].isna().any():
        raise ValueError("Azure adapter requires parseable datetime time_index values")
    work["_event"] = pd.to_numeric(work["event"], errors="coerce").fillna(0).astype(int).clip(0, 1)
    duration = np.full(len(work), np.nan, dtype=float)
    event = np.zeros(len(work), dtype=int)
    censored_rows = 0
    observed_rows = 0
    censored_final_episodes = 0
    observed_episodes = 0
    no_failure_units = 0
    ns_per_hour = 3_600_000_000_000.0
    for _, group in work.sort_values(["entity_id", "_time_dt"]).groupby("entity_id", sort=False):
        idx = group.index.to_numpy()
        time_ns = group["_time_dt"].astype("int64").to_numpy(dtype=np.int64)
        censor_ns = int(time_ns.max())
        failure_ns = np.asarray(
            sorted(group.loc[group["_event"] == 1, "_time_dt"].astype("int64").to_numpy(dtype=np.int64)),
            dtype=np.int64,
        )
        if len(failure_ns) == 0:
            no_failure_units += 1
        else:
            observed_episodes += len(failure_ns)
        pos = np.searchsorted(failure_ns, time_ns, side="left") if len(failure_ns) else np.full(len(group), -1)
        has_future = (pos >= 0) & (pos < len(failure_ns))
        if np.any(has_future):
            row_idx = idx[has_future]
            duration[row_idx] = (failure_ns[pos[has_future]] - time_ns[has_future]) / ns_per_hour
            event[row_idx] = 1
            observed_rows += int(np.sum(duration[row_idx] > 0))
        no_future = ~has_future
        if np.any(no_future):
            row_idx = idx[no_future]
            duration[row_idx] = (censor_ns - time_ns[no_future]) / ns_per_hour
            event[row_idx] = 0
            censored_rows += int(np.sum(duration[row_idx] > 0))
        if len(failure_ns) == 0 or int(failure_ns[-1]) < censor_ns:
            censored_final_episodes += 1
    meta = {
        "observed_failure_episodes": int(observed_episodes),
        "censored_final_episodes": int(censored_final_episodes),
        "no_failure_units": int(no_failure_units),
        "observed_anchor_rows_before_duration_filter": int(observed_rows),
        "censored_anchor_rows_before_duration_filter": int(censored_rows),
        "azure_censoring_explanation": (
            "Rows after a unit's last observed failure, and units with no observed failure, are administrative "
            "censoring episodes ending at the last timestamp for that unit. The old adapter dropped them because "
            "raw failure_datetime uses 0 and time_to_event uses 0 for no future failure."
        ),
    }
    return duration, event, meta


def _build_azure(dataset: str, df: pd.DataFrame, censoring_rate: float, cfg: dict[str, Any], source_path: Path) -> SurvivalFrame:
    required = {"entity_id", "time_index", "event"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Azure adapter missing required columns: {sorted(missing)}")
    duration, event, azure_meta = _azure_row_targets(df)
    feature_cols = _feature_columns(df)
    static_cols = _static_columns(df, feature_cols)
    return _frame_from_landmarks(
        dataset,
        df,
        unit_col="entity_id",
        time_col="time_index",
        duration=duration,
        event=event,
        feature_cols=feature_cols,
        static_cols=static_cols,
        cfg=cfg,
        meta={
            "dataset": dataset,
            "adapter": "azure_recurrent_event",
            "source": str(source_path),
            "source_type": "real_raw_csv",
            "target_censoring_rate": censoring_rate,
            "synthetic_fallback": False,
            **azure_meta,
        },
    )


def _build_cmapss(dataset: str, df: pd.DataFrame, censoring_rate: float, cfg: dict[str, Any], source_path: Path) -> SurvivalFrame:
    required = {"unit_number", "time_cycle"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"C-MAPSS adapter missing required columns: {sorted(missing)}")
    work = df.copy()
    split = work["split"].astype(str) if "split" in work.columns else "full"
    work["_unit_group"] = split + "_" + work["unit_number"].astype(str)
    time_cycle = pd.to_numeric(work["time_cycle"], errors="coerce")
    if "time_to_event" in work.columns:
        raw_failure = time_cycle + pd.to_numeric(work["time_to_event"], errors="coerce")
        failure_cycle = raw_failure.groupby(work["_unit_group"]).transform("median")
    else:
        failure_cycle = time_cycle.groupby(work["_unit_group"]).transform("max")
    seed_bytes = f"{dataset}|{float(censoring_rate):.6f}|cmapss".encode("utf-8")
    seed = int.from_bytes(hashlib.sha256(seed_bytes).digest()[:8], "little") % (2**32)
    rng = np.random.default_rng(seed)
    units = np.asarray(sorted(work["_unit_group"].unique()))
    n_censored = int(round(float(censoring_rate) * len(units)))
    censored_units = set(rng.choice(units, size=n_censored, replace=False).tolist()) if n_censored else set()
    censor_cycle_by_unit = {}
    for unit in censored_units:
        group_time = time_cycle[work["_unit_group"] == unit]
        lo = int(np.nanmin(group_time)) + 1
        hi = max(lo + 1, int(np.nanmax(group_time)))
        censor_cycle_by_unit[unit] = int(rng.integers(lo, hi))
    duration = (failure_cycle - time_cycle).to_numpy(dtype=float)
    event = np.ones(len(work), dtype=int)
    keep = np.ones(len(work), dtype=bool)
    for unit, censor_cycle in censor_cycle_by_unit.items():
        mask = work["_unit_group"].to_numpy() == unit
        keep &= ~(mask & (time_cycle.to_numpy() > censor_cycle))
        unit_idx = mask & (time_cycle.to_numpy() <= censor_cycle)
        duration[unit_idx] = censor_cycle - time_cycle.to_numpy()[unit_idx]
        event[unit_idx] = 0
    work = work[keep].copy()
    duration = duration[keep]
    event = event[keep]
    feature_cols = _feature_columns(work)
    static_cols: list[str] = []
    return _frame_from_landmarks(
        dataset,
        work,
        unit_col="_unit_group",
        time_col="time_cycle",
        duration=duration,
        event=event,
        feature_cols=feature_cols,
        static_cols=static_cols,
        cfg=cfg,
        meta={
            "dataset": dataset,
            "adapter": "cmapss_administrative_censoring",
            "source": str(source_path),
            "source_type": "real_raw_csv",
            "target_censoring_rate": censoring_rate,
            "actual_censored_unit_fraction": float(len(censored_units) / max(1, len(units))),
            "synthetic_fallback": False,
            "note": "C-MAPSS censoring is simulated administrative censoring, not natural censoring.",
        },
    )


def _build_scania(dataset: str, df: pd.DataFrame, censoring_rate: float, cfg: dict[str, Any], source_path: Path) -> SurvivalFrame:
    required = {"unit_id", "time_index", "duration", "event"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"SCANIA adapter missing required columns: {sorted(missing)}")
    duration = pd.to_numeric(df["duration"], errors="coerce").to_numpy(dtype=float)
    event = pd.to_numeric(df["event"], errors="coerce").fillna(0).astype(int).clip(0, 1).to_numpy()
    feature_cols = _feature_columns(df)
    static_cols = _static_columns(df, feature_cols)
    return _frame_from_landmarks(
        dataset,
        df,
        unit_col="unit_id",
        time_col="time_index",
        duration=duration,
        event=event,
        feature_cols=feature_cols,
        static_cols=static_cols,
        cfg=cfg,
        meta={
            "dataset": dataset,
            "adapter": "scania_observed_censoring",
            "source": str(source_path),
            "source_type": "real_raw_csv",
            "target_censoring_rate": censoring_rate,
            "synthetic_fallback": False,
            "note": "SCANIA preserves observed censoring labels; target censoring rate is not simulated.",
        },
    )
