#!/usr/bin/env python
from __future__ import annotations

import argparse

from build_all_frames import build_dataset_frames
from common import add_common_build_args


def main() -> None:
    parser = argparse.ArgumentParser(description="Build Azure PdM .npz survival frames using the exported main-project adapter.")
    add_common_build_args(parser)
    args = parser.parse_args()
    args.datasets = ["azure"]
    build_dataset_frames(args)


if __name__ == "__main__":
    main()
