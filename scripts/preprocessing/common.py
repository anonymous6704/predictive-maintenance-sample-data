from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from io_utils import load_yaml


DATASETS = ["azure", "scania", "cmapss_fd001", "cmapss_fd002", "cmapss_fd003", "cmapss_fd004"]
CMAPSS_DATASETS = ["cmapss_fd001", "cmapss_fd002", "cmapss_fd003", "cmapss_fd004"]

PROJECT_PREPARED_FILES = {
    "azure": ["azure_pdm.csv"],
    "scania": ["scania_survival_samples.csv"],
    "cmapss_fd001": ["cmapss_fd001.csv"],
    "cmapss_fd002": ["cmapss_fd002.csv"],
    "cmapss_fd003": ["cmapss_fd003.csv"],
    "cmapss_fd004": ["cmapss_fd004.csv"],
}

UPSTREAM_REQUIRED_FILES = {
    "azure": [
        "PdM_telemetry.csv",
        "PdM_errors.csv",
        "PdM_failures.csv",
        "PdM_machines.csv",
        "PdM_maint.csv",
    ],
    "scania_component_x": [
        "train_operational_readouts.csv",
        "test_operational_readouts.csv",
        "validation_operational_readouts.csv",
        "train_tte.csv",
        "train_specifications.csv",
        "test_labels.csv",
        "validation_labels.csv",
        "test_specifications.csv",
        "validation_specifications.csv",
    ],
    "cmapss": [
        "train_FD001.txt",
        "test_FD001.txt",
        "RUL_FD001.txt",
        "train_FD002.txt",
        "test_FD002.txt",
        "RUL_FD002.txt",
        "train_FD003.txt",
        "test_FD003.txt",
        "RUL_FD003.txt",
        "train_FD004.txt",
        "test_FD004.txt",
        "RUL_FD004.txt",
    ],
}

UCI_APS_MARKERS = [
    "aps_failure_training_set.csv",
    "aps_failure_test_set.csv",
    "aps_failure_description.txt",
]


def tag(dataset: str, censoring_rate: float) -> str:
    return f"{dataset}_{float(censoring_rate):g}".replace(".", "p")


def load_config(path: str | Path, raw_root: str | Path | None = None) -> dict[str, Any]:
    cfg = load_yaml(path)
    if raw_root is not None:
        cfg["raw_roots"] = [str(raw_root)]
    return cfg


def active_datasets(cfg: dict[str, Any], requested: list[str] | None = None) -> list[str]:
    if requested:
        return requested
    flags = cfg.get("datasets", {})
    return [name for name in DATASETS if bool(flags.get(name, False))]


def rates_for_dataset(cfg: dict[str, Any], dataset: str, requested: list[float] | None = None) -> list[float]:
    if requested is not None:
        return [float(v) for v in requested]
    by_dataset = cfg.get("censoring_rates_by_dataset", {})
    if dataset in by_dataset:
        return [float(v) for v in by_dataset[dataset]]
    return [float(v) for v in cfg.get("data_build", {}).get("censoring_rates", [0.0])]


def add_common_build_args(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    parser.add_argument("--config", default="configs/preprocessing/build_all.yaml")
    parser.add_argument("--raw-root", default="raw")
    parser.add_argument("--out-root", default="outputs/frames")
    parser.add_argument("--datasets", nargs="*", default=None, choices=DATASETS)
    parser.add_argument("--censoring-rates", nargs="*", type=float, default=None)
    parser.add_argument("--force-rebuild", action="store_true")
    return parser


def scania_component_x_guard(raw_root: str | Path) -> None:
    root = Path(raw_root)
    scan_roots = [root / "scania_component_x", root / "scania"]
    found = []
    for scan_root in scan_roots:
        for marker in UCI_APS_MARKERS:
            candidate = scan_root / marker
            if candidate.exists():
                found.append(candidate)
    if found:
        paths = ", ".join(str(path) for path in found)
        raise SystemExit(
            "This script expects SCANIA Component X survival/time-series inputs, not UCI APS Failure at Scania Trucks. "
            f"UCI APS-like files detected: {paths}"
        )
