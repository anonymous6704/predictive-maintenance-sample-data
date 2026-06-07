#!/usr/bin/env python
from __future__ import annotations

import argparse
from pathlib import Path

from common import PROJECT_PREPARED_FILES, UPSTREAM_REQUIRED_FILES, active_datasets, load_config, scania_component_x_guard


def missing_files(root: Path, files: list[str]) -> list[Path]:
    return [root / name for name in files if not (root / name).exists()]


def main() -> None:
    parser = argparse.ArgumentParser(description="Verify upstream-download and project-prepared raw input files.")
    parser.add_argument("--config", default="configs/preprocessing/build_all.yaml")
    parser.add_argument("--raw-root", default="raw")
    args = parser.parse_args()

    cfg = load_config(args.config, args.raw_root)
    raw_root = Path(args.raw_root)
    scania_component_x_guard(raw_root)
    problems: list[str] = []

    print("Upstream download layout check:")
    for folder, files in UPSTREAM_REQUIRED_FILES.items():
        miss = missing_files(raw_root / folder, files)
        status = "OK" if not miss else "MISSING"
        print(f"- {folder}: {status}")
        for path in miss:
            print(f"  missing {path}")

    print("\nProject-prepared CSV inputs required by the exported main-project adapters:")
    for dataset in active_datasets(cfg):
        folder = "scania" if dataset == "scania" else dataset
        miss = missing_files(raw_root / folder, PROJECT_PREPARED_FILES[dataset])
        status = "OK" if not miss else "MISSING"
        print(f"- {dataset}: {status}")
        for path in miss:
            print(f"  missing {path}")
            problems.append(str(path))

    if problems:
        raise SystemExit(
            "Missing project-prepared CSV inputs for frame building. "
            "See PORTING_NOTES.md: the exported main-project adapters preserve existing CSV-to-frame logic and do not invent vendor-raw converters."
        )


if __name__ == "__main__":
    main()
