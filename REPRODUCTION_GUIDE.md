# Reproduction Guide

This repository contains preprocessing scripts exported from the main OCEAN-MO-CDSF project, plus small wrapper scripts for preparing downloaded upstream files into the CSV inputs expected by those frame builders.

It does not contain full raw datasets, full processed `.npz` frames, trained weights, model checkpoints, or full benchmark results.

Users must manually download upstream data from the links in:

- `data_samples/DATA_SOURCES.md`

## Expected Raw Directory Layout

Place downloaded upstream files under `raw/`:

```text
raw/
  azure/
    PdM_telemetry.csv
    PdM_errors.csv
    PdM_failures.csv
    PdM_machines.csv
    PdM_maint.csv

  scania_component_x/
    train_operational_readouts.csv
    test_operational_readouts.csv
    validation_operational_readouts.csv
    train_tte.csv
    train_specifications.csv
    test_labels.csv
    validation_labels.csv
    test_specifications.csv
    validation_specifications.csv

  cmapss/
    train_FD001.txt
    test_FD001.txt
    RUL_FD001.txt
    train_FD002.txt
    test_FD002.txt
    RUL_FD002.txt
    train_FD003.txt
    test_FD003.txt
    RUL_FD003.txt
    train_FD004.txt
    test_FD004.txt
    RUL_FD004.txt
```

## Prepare Project CSV Inputs

The frame builders consume project-prepared CSV files. Convert the upstream file layouts above with:

```bash
python scripts/preprocessing/prepare_all_csvs.py --raw-root raw
```

Equivalent per-dataset commands:

```bash
python scripts/preprocessing/prepare_azure_pdm_csv.py --raw-root raw
python scripts/preprocessing/prepare_scania_component_x_csv.py --raw-root raw
python scripts/preprocessing/prepare_cmapss_csv.py --raw-root raw
```

These commands write:

```text
raw/
  azure/
    azure_pdm.csv

  scania/
    scania_survival_samples.csv

  cmapss_fd001/
    cmapss_fd001.csv
  cmapss_fd002/
    cmapss_fd002.csv
  cmapss_fd003/
    cmapss_fd003.csv
  cmapss_fd004/
    cmapss_fd004.csv
```

`scania_survival_samples.csv` means SCANIA Component X-derived survival/time-series data. It is not UCI APS Failure at Scania Trucks.

The SCANIA Component X converter uses `train_operational_readouts.csv`, `train_tte.csv`, and `train_specifications.csv`, because the public train split contains observed time-to-event labels. The public validation/test labels are class labels for challenge evaluation, not full per-row time-to-event records.

## Commands

Verify raw inputs:

```bash
python scripts/preprocessing/verify_raw_data.py --config configs/preprocessing/build_all.yaml --raw-root raw
```

Prepare project CSV inputs and build project-compatible `.npz` survival frames in one command:

```bash
python scripts/preprocessing/build_all_frames.py --config configs/preprocessing/build_all.yaml --raw-root raw --out-root outputs/frames --prepare-from-upstream
```

Or build frames after CSV preparation:

```bash
python scripts/preprocessing/build_all_frames.py --config configs/preprocessing/build_all.yaml --raw-root raw --out-root outputs/frames
```

Validate generated frames:

```bash
python scripts/preprocessing/validate_npz_frames.py --frames-root outputs/frames
```

Extract lightweight mini samples from generated frames:

```bash
python scripts/extract_processed_mini_samples.py --frames-root outputs/frames
```

Validate sample artifacts:

```bash
python scripts/validate_data_samples.py
```

## Scope

Preprocessing creates `.npz` survival frames only. Training, model selection, calibration, and test reporting happen outside this sample-data repository.

Validation metrics are used for model selection in the full project. Test metrics are reported only after model or configuration selection is fixed.

This repository is not sufficient to reproduce paper-scale benchmark metrics by itself. Full reproduction requires upstream data, project-prepared CSV construction, `.npz` frame generation, training, validation-based model selection, and final test reporting.
