#!/usr/bin/env python
from __future__ import annotations

import argparse

from build_all_frames import build_dataset_frames
from common import CMAPSS_DATASETS, add_common_build_args


def main() -> None:
    parser = argparse.ArgumentParser(description="Build NASA C-MAPSS FD001-FD004 .npz survival frames using exported main-project adapters.")
    add_common_build_args(parser)
    parser.add_argument("--fd", nargs="*", choices=["FD001", "FD002", "FD003", "FD004"], default=None)
    args = parser.parse_args()
    if args.fd:
        args.datasets = [f"cmapss_{fd.lower()}" for fd in args.fd]
    elif args.datasets is None:
        args.datasets = CMAPSS_DATASETS
    build_dataset_frames(args)


if __name__ == "__main__":
    main()
