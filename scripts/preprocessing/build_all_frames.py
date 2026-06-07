#!/usr/bin/env python
from __future__ import annotations

import argparse
from pathlib import Path

from adapters import build_real_frame
from common import add_common_build_args, active_datasets, load_config, rates_for_dataset, scania_component_x_guard, tag
from frame_validator import export_audit, validate_frame
from logging_utils import log
from splits import make_unit_splits


def build_dataset_frames(args: argparse.Namespace) -> list[Path]:
    cfg = load_config(args.config, args.raw_root)
    out_root = Path(args.out_root)
    audit_root = out_root.parent / "audits"
    split_root = out_root.parent / "splits"
    horizons = cfg.get("data_build", {}).get("horizons", [24, 72, 168, 336])
    allow_short = bool(cfg.get("data_build", {}).get("allow_short_sequences", False))
    written: list[Path] = []
    for dataset in active_datasets(cfg, args.datasets):
        if dataset == "scania":
            scania_component_x_guard(args.raw_root)
        for censoring_rate in rates_for_dataset(cfg, dataset, args.censoring_rates):
            out_path = out_root / f"{tag(dataset, censoring_rate)}_frame.npz"
            if out_path.exists() and not args.force_rebuild:
                log("RESUME", f"existing frame kept: {out_path}")
                written.append(out_path)
                continue
            result = build_real_frame(dataset, float(censoring_rate), cfg, Path.cwd())
            out_path.parent.mkdir(parents=True, exist_ok=True)
            result.frame.save_npz(out_path)
            split_path = split_root / f"{tag(dataset, censoring_rate)}_seed0_splits.json"
            splits = make_unit_splits(result.frame, seed=0, out_path=split_path)
            audit = validate_frame(result.frame, horizons=horizons, splits=splits, allow_short_sequences=allow_short)
            audit["censoring_rate"] = float(censoring_rate)
            export_audit(
                audit,
                audit_root / f"{tag(dataset, censoring_rate)}_audit.json",
                audit_root / f"{tag(dataset, censoring_rate)}_audit.csv",
            )
            if audit["status"] != "passed":
                raise SystemExit(f"Frame audit failed for {dataset} censoring={censoring_rate}: {audit['errors']}")
            log("SAVE", f"frame saved to {out_path}")
            written.append(out_path)
    return written


def main() -> None:
    parser = argparse.ArgumentParser(description="Build project-compatible .npz survival frames from project-prepared raw CSV inputs.")
    add_common_build_args(parser)
    args = parser.parse_args()
    written = build_dataset_frames(args)
    print(f"Built or reused {len(written)} frame(s).")


if __name__ == "__main__":
    main()
