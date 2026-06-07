from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np


@dataclass
class SurvivalFrame:
    x_seq: np.ndarray
    x_static: np.ndarray
    seq_mask: np.ndarray
    missing_mask: np.ndarray
    delta_t: np.ndarray
    duration: np.ndarray
    event: np.ndarray
    event_type: np.ndarray
    unit_id: np.ndarray
    anchor_time: np.ndarray
    dataset_name: str
    feature_names_seq: list[str]
    feature_names_static: list[str]
    meta_json: dict[str, Any]

    def save_npz(self, path: str | Path) -> Path:
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)
        np.savez_compressed(
            out,
            x_seq=self.x_seq,
            x_static=self.x_static,
            seq_mask=self.seq_mask,
            missing_mask=self.missing_mask,
            delta_t=self.delta_t,
            duration=self.duration,
            event=self.event,
            event_type=self.event_type,
            unit_id=self.unit_id,
            anchor_time=self.anchor_time,
            dataset_name=np.array(self.dataset_name),
            feature_names_seq=np.array(self.feature_names_seq, dtype=object),
            feature_names_static=np.array(self.feature_names_static, dtype=object),
            meta_json=np.array(json.dumps(self.meta_json, sort_keys=True)),
        )
        return out

    @classmethod
    def load_npz(cls, path: str | Path) -> "SurvivalFrame":
        data = np.load(path, allow_pickle=True)
        return cls(
            x_seq=data["x_seq"],
            x_static=data["x_static"],
            seq_mask=data["seq_mask"],
            missing_mask=data["missing_mask"],
            delta_t=data["delta_t"],
            duration=data["duration"],
            event=data["event"],
            event_type=data["event_type"],
            unit_id=data["unit_id"],
            anchor_time=data["anchor_time"],
            dataset_name=str(data["dataset_name"].item()),
            feature_names_seq=[str(v) for v in data["feature_names_seq"].tolist()],
            feature_names_static=[str(v) for v in data["feature_names_static"].tolist()],
            meta_json=json.loads(str(data["meta_json"].item())),
        )
