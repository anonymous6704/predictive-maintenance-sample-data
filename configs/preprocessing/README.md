# Preprocessing Configs

These configs preserve the frame-construction settings from the main project's `configs/main.yaml` data-build section.

`build_all.yaml` enables Azure PdM, SCANIA Component X-derived Scania frames, and C-MAPSS FD001-FD004. Dataset-specific configs restrict the same settings to one dataset family.

Use `scripts/preprocessing/prepare_all_csvs.py` to convert manually downloaded upstream files into the project-prepared CSV inputs under `raw/`. Then use `scripts/preprocessing/build_all_frames.py` to build `.npz` survival frames, as documented in `REPRODUCTION_GUIDE.md`.
