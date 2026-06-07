#!/usr/bin/env python
from __future__ import annotations

import argparse

from upstream_converters import prepare_scania_component_x_csv


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Prepare SCANIA Component X train files into raw/scania/scania_survival_samples.csv."
    )
    parser.add_argument("--raw-root", default="raw")
    parser.add_argument("--out", default=None)
    parser.add_argument("--chunksize", type=int, default=250_000)
    args = parser.parse_args()
    path = prepare_scania_component_x_csv(args.raw_root, args.out, args.chunksize)
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
