from __future__ import annotations

from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd

from common import scania_component_x_guard


CMAPSS_FDS = ["FD001", "FD002", "FD003", "FD004"]
CMAPSS_COLUMNS = [
    "unit_number",
    "time_cycle",
    "op_setting_1",
    "op_setting_2",
    "op_setting_3",
    *[f"sensor_{i}" for i in range(1, 22)],
]


def _read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(path)
    return pd.read_csv(path)


def _find_col(columns: Iterable[str], names: Iterable[str]) -> str | None:
    lookup = {str(col).lower(): str(col) for col in columns}
    for name in names:
        if name.lower() in lookup:
            return lookup[name.lower()]
    return None


def _require_col(columns: Iterable[str], names: Iterable[str], label: str) -> str:
    col = _find_col(columns, names)
    if col is None:
        raise ValueError(f"Could not find {label}; accepted names: {list(names)}")
    return col


def prepare_azure_csv(raw_root: str | Path, out_path: str | Path | None = None) -> Path:
    root = Path(raw_root) / "azure"
    telemetry = _read_csv(root / "PdM_telemetry.csv")
    errors = _read_csv(root / "PdM_errors.csv")
    failures = _read_csv(root / "PdM_failures.csv")
    machines = _read_csv(root / "PdM_machines.csv")
    maint = _read_csv(root / "PdM_maint.csv")

    for frame in [telemetry, errors, failures, maint]:
        frame["datetime"] = pd.to_datetime(frame["datetime"], errors="coerce")
    telemetry = telemetry.rename(columns={"machineID": "entity_id", "datetime": "time_index"})
    machines = machines.rename(columns={"machineID": "entity_id"})

    failure_times = failures.rename(columns={"machineID": "entity_id", "datetime": "time_index"})
    failure_times = failure_times[["entity_id", "time_index"]].drop_duplicates()
    failure_times["event"] = 1

    error_counts = (
        errors.rename(columns={"machineID": "entity_id", "datetime": "time_index"})
        .groupby(["entity_id", "time_index"])
        .size()
        .rename("error_count")
        .reset_index()
    )
    maint_counts = (
        maint.rename(columns={"machineID": "entity_id", "datetime": "time_index"})
        .groupby(["entity_id", "time_index"])
        .size()
        .rename("maint_count")
        .reset_index()
    )

    out = telemetry.merge(machines, on="entity_id", how="left")
    out = out.merge(error_counts, on=["entity_id", "time_index"], how="left")
    out = out.merge(maint_counts, on=["entity_id", "time_index"], how="left")
    out = out.merge(failure_times, on=["entity_id", "time_index"], how="left")
    out["event"] = out["event"].fillna(0).astype(int)
    out["error_count"] = out["error_count"].fillna(0).astype(int)
    out["maint_count"] = out["maint_count"].fillna(0).astype(int)
    if "model" in out.columns:
        out["model_id"] = pd.Categorical(out["model"]).codes.astype(int)
        out = out.drop(columns=["model"])
    out["time_index"] = pd.to_datetime(out["time_index"], errors="coerce").dt.strftime("%Y-%m-%d %H:%M:%S")
    out = out.sort_values(["entity_id", "time_index"]).reset_index(drop=True)
    target = Path(out_path) if out_path else root / "azure_pdm.csv"
    target.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(target, index=False)
    return target


def _read_cmapss_txt(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(path)
    return pd.read_csv(path, sep=r"\s+", header=None, names=CMAPSS_COLUMNS)


def prepare_cmapss_csv(raw_root: str | Path, fd: str, out_path: str | Path | None = None) -> Path:
    fd = fd.upper()
    if fd not in CMAPSS_FDS:
        raise ValueError(f"Unsupported C-MAPSS subset: {fd}")
    root = Path(raw_root)
    source_root = root / "cmapss"
    train = _read_cmapss_txt(source_root / f"train_{fd}.txt")
    test = _read_cmapss_txt(source_root / f"test_{fd}.txt")
    rul = pd.read_csv(source_root / f"RUL_{fd}.txt", sep=r"\s+", header=None, names=["rul"])

    train["split"] = "train"
    train_max = train.groupby("unit_number")["time_cycle"].transform("max")
    train["time_to_event"] = train_max - train["time_cycle"]

    test["split"] = "test"
    test_max = test.groupby("unit_number")["time_cycle"].transform("max")
    rul_by_unit = pd.Series(rul["rul"].to_numpy(), index=np.arange(1, len(rul) + 1))
    test["time_to_event"] = test["unit_number"].map(test_max.groupby(test["unit_number"]).first() + rul_by_unit) - test["time_cycle"]

    out = pd.concat([train, test], ignore_index=True)
    dataset = f"cmapss_{fd.lower()}"
    target = Path(out_path) if out_path else root / dataset / f"{dataset}.csv"
    target.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(target, index=False)
    return target


def _load_tte(root: Path, vehicle_ids: list[str] | None = None) -> pd.DataFrame:
    tte = _read_csv(root / "train_tte.csv")
    vehicle_col = _find_col(tte.columns, ["vehicle_id", "unit_id", "id"])
    length_col = _require_col(tte.columns, ["length_of_study_time_step", "time_to_event", "tte"], "SCANIA TTE length column")
    event_col = _require_col(tte.columns, ["in_study_repair", "event", "label"], "SCANIA repair/event column")
    out = tte.copy()
    if vehicle_col is None:
        if vehicle_ids is None or len(vehicle_ids) != len(out):
            raise ValueError(
                "train_tte.csv has no vehicle_id column and could not be aligned. "
                "Provide train_specifications.csv with vehicle_id rows matching train_tte.csv."
            )
        out["vehicle_id"] = vehicle_ids
    else:
        out["vehicle_id"] = out[vehicle_col].astype(str)
    return out[["vehicle_id", length_col, event_col]].rename(
        columns={length_col: "length_of_study_time_step", event_col: "in_study_repair"}
    )


def _prepare_scania_specs(root: Path) -> pd.DataFrame:
    specs = _read_csv(root / "train_specifications.csv")
    vehicle_col = _require_col(specs.columns, ["vehicle_id", "unit_id", "id"], "SCANIA vehicle id column in specifications")
    out = specs.copy()
    out["vehicle_id"] = out[vehicle_col].astype(str)
    if vehicle_col != "vehicle_id":
        out = out.drop(columns=[vehicle_col])
    for col in list(out.columns):
        if col == "vehicle_id":
            continue
        new_col = col if str(col).startswith("spec_") else f"spec_{col}"
        if pd.api.types.is_numeric_dtype(out[col]):
            out[new_col] = pd.to_numeric(out[col], errors="coerce")
        else:
            out[new_col] = pd.Categorical(out[col].astype(str)).codes.astype(int)
        if new_col != col and col in out.columns:
            out = out.drop(columns=[col])
    return out.loc[:, ~out.columns.duplicated()]


def prepare_scania_component_x_csv(raw_root: str | Path, out_path: str | Path | None = None, chunksize: int = 250_000) -> Path:
    scania_component_x_guard(raw_root)
    root = Path(raw_root) / "scania_component_x"
    specs = _prepare_scania_specs(root)
    tte = _load_tte(root, specs["vehicle_id"].astype(str).tolist())
    labels = specs[["vehicle_id"]].merge(tte, on="vehicle_id", how="left")
    labels["length_of_study_time_step"] = pd.to_numeric(labels["length_of_study_time_step"], errors="coerce")
    labels["in_study_repair"] = pd.to_numeric(labels["in_study_repair"], errors="coerce").fillna(0).astype(int).clip(0, 1)

    source = root / "train_operational_readouts.csv"
    header = pd.read_csv(source, nrows=0)
    vehicle_col = _require_col(header.columns, ["vehicle_id", "unit_id", "id"], "SCANIA vehicle id column in operational readouts")
    time_col = _require_col(header.columns, ["time_step", "time_index", "timestep"], "SCANIA time-step column in operational readouts")

    target = Path(out_path) if out_path else Path(raw_root) / "scania" / "scania_survival_samples.csv"
    target.parent.mkdir(parents=True, exist_ok=True)
    wrote_header = False
    for chunk in pd.read_csv(source, chunksize=chunksize):
        chunk = chunk.rename(columns={vehicle_col: "unit_id", time_col: "time_index"})
        chunk["vehicle_id"] = chunk["unit_id"].astype(str)
        merged = chunk.merge(labels, on="vehicle_id", how="left").merge(specs, on="vehicle_id", how="left")
        merged["duration"] = pd.to_numeric(merged["length_of_study_time_step"], errors="coerce") - pd.to_numeric(
            merged["time_index"], errors="coerce"
        )
        merged["event"] = pd.to_numeric(merged["in_study_repair"], errors="coerce").fillna(0).astype(int).clip(0, 1)
        merged = merged.drop(columns=["vehicle_id", "length_of_study_time_step", "in_study_repair"], errors="ignore")
        merged = merged[merged["duration"].notna() & (merged["duration"] > 0)]
        merged.to_csv(target, index=False, mode="w" if not wrote_header else "a", header=not wrote_header)
        wrote_header = True
    return target
