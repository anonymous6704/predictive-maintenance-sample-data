#!/usr/bin/env python
from __future__ import annotations

import argparse

from build_all_frames import build_dataset_frames
from common import add_common_build_args, scania_component_x_guard


def main() -> None:
    parser = argparse.ArgumentParser(description="Build SCANIA Component X .npz survival frames using the exported main-project adapter.")
    add_common_build_args(parser)
    args = parser.parse_args()
    scania_component_x_guard(args.raw_root)
    args.datasets = ["scania"]
    args.censoring_rates = [0.0] if args.censoring_rates is None else args.censoring_rates
    build_dataset_frames(args)


if __name__ == "__main__":
    main()
