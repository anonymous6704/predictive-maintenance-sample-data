#!/usr/bin/env python
from __future__ import annotations

import argparse

from common import CMAPSS_DATASETS
from upstream_converters import prepare_cmapss_csv


def main() -> None:
    parser = argparse.ArgumentParser(description="Prepare NASA C-MAPSS txt/RUL files into project CSV inputs.")
    parser.add_argument("--raw-root", default="raw")
    parser.add_argument("--fd", nargs="*", choices=["FD001", "FD002", "FD003", "FD004"], default=None)
    args = parser.parse_args()
    fds = args.fd or [name.split("_")[1].upper() for name in CMAPSS_DATASETS]
    for fd in fds:
        path = prepare_cmapss_csv(args.raw_root, fd)
        print(f"Wrote {path}")


if __name__ == "__main__":
    main()
