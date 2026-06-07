#!/usr/bin/env python
from __future__ import annotations

import argparse

from upstream_converters import prepare_azure_csv


def main() -> None:
    parser = argparse.ArgumentParser(description="Prepare Azure PdM upstream CSV files into raw/azure/azure_pdm.csv.")
    parser.add_argument("--raw-root", default="raw")
    parser.add_argument("--out", default=None)
    args = parser.parse_args()
    path = prepare_azure_csv(args.raw_root, args.out)
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
