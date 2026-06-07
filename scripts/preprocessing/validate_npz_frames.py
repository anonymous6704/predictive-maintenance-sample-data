#!/usr/bin/env python
from __future__ import annotations

import argparse
from pathlib import Path

from frame import SurvivalFrame
from frame_validator import validate_frame


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate exported project-compatible .npz survival frames.")
    parser.add_argument("--frames-root", default="outputs/frames")
    parser.add_argument("--horizons", nargs="*", type=float, default=[24, 72, 168, 336])
    parser.add_argument("--allow-short-sequences", action="store_true")
    args = parser.parse_args()

    frames = sorted(Path(args.frames_root).glob("*_frame.npz"))
    if not frames:
        raise SystemExit(f"No .npz frames found under {args.frames_root}")
    failures = []
    for path in frames:
        frame = SurvivalFrame.load_npz(path)
        audit = validate_frame(frame, horizons=args.horizons, allow_short_sequences=args.allow_short_sequences)
        print(f"{path}: {audit['status']} rows={audit['n_rows']} units={audit['n_units']}")
        if audit["status"] != "passed":
            failures.append((path, audit["errors"]))
    if failures:
        raise SystemExit(f"Frame validation failed: {failures}")


if __name__ == "__main__":
    main()
