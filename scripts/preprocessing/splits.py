from __future__ import annotations

from pathlib import Path

import numpy as np

from frame import SurvivalFrame
from io_utils import write_json


def make_unit_splits(frame: SurvivalFrame, seed: int, out_path: str | Path) -> dict[str, list[str]]:
    rng = np.random.default_rng(seed)
    units = np.unique(frame.unit_id.astype(str))
    rng.shuffle(units)
    n = len(units)
    n_train = max(1, int(round(0.50 * n)))
    n_cal = max(1, int(round(0.15 * n)))
    n_val = max(1, int(round(0.15 * n)))
    splits = {
        "train": units[:n_train].tolist(),
        "calibration": units[n_train : n_train + n_cal].tolist(),
        "validation": units[n_train + n_cal : n_train + n_cal + n_val].tolist(),
        "test": units[n_train + n_cal + n_val :].tolist(),
    }
    if not splits["test"]:
        splits["test"] = splits["validation"][-1:]
        splits["validation"] = splits["validation"][:-1]
    write_json(out_path, splits)
    return splits


def split_indices(frame: SurvivalFrame, splits: dict[str, list[str]]) -> dict[str, np.ndarray]:
    units = frame.unit_id.astype(str)
    return {
        name: np.where(np.isin(units, np.asarray(unit_list, dtype=str)))[0]
        for name, unit_list in splits.items()
    }
