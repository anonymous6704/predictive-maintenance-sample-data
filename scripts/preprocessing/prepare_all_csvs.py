#!/usr/bin/env python
from __future__ import annotations

import argparse

from common import CMAPSS_DATASETS
from upstream_converters import prepare_azure_csv, prepare_cmapss_csv, prepare_scania_component_x_csv


def main() -> None:
    parser = argparse.ArgumentParser(description="Prepare all downloaded upstream files into project CSV inputs.")
    parser.add_argument("--raw-root", default="raw")
    parser.add_argument(
        "--datasets",
        nargs="*",
        choices=["azure", "scania", *CMAPSS_DATASETS],
        default=["azure", "scania", *CMAPSS_DATASETS],
    )
    parser.add_argument("--scania-chunksize", type=int, default=250_000)
    args = parser.parse_args()

    written = []
    if "azure" in args.datasets:
        written.append(prepare_azure_csv(args.raw_root))
    if "scania" in args.datasets:
        written.append(prepare_scania_component_x_csv(args.raw_root, chunksize=args.scania_chunksize))
    for dataset in CMAPSS_DATASETS:
        if dataset in args.datasets:
            fd = dataset.split("_")[1].upper()
            written.append(prepare_cmapss_csv(args.raw_root, fd))

    print(f"Wrote {len(written)} project CSV input(s).")
    for path in written:
        print(path)


if __name__ == "__main__":
    main()
