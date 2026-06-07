# Preprocessing Configs

These configs preserve the frame-construction settings from the main project's `configs/main.yaml` data-build section.

`build_all.yaml` enables Azure PdM, SCANIA Component X-derived Scania frames, and C-MAPSS FD001-FD004. Dataset-specific configs restrict the same settings to one dataset family.

The exported adapters expect project-prepared CSV inputs under `raw/`, as documented in `scripts/preprocessing/PORTING_NOTES.md`.
