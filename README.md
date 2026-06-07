# Predictive Maintenance Sample Data

## Overview

This repository provides small illustrative data samples for the OCEAN-MO-CDSF framework, an evidence-driven multi-objective deep survival framework for censored predictive maintenance.

## What This Repository Contains

- Survival test cases
- Survival frame samples
- Audit table samples
- Model result samples
- HPO trace samples
- Processed mini samples extracted from processed survival-frame `.npz` files
- Quick-view convenience copies
- Validation scripts
- Raw-to-frame preprocessing scripts

## What This Repository Does Not Contain

- It does not contain the full benchmark dataset.
- It does not redistribute raw Azure, Scania, or C-MAPSS data.
- It does not contain model checkpoints, trained weights, raw industrial logs, or private data.
- It does not contain ontology, KG, or graph data.

## Directory Structure

```text
predictive-maintenance-sample-data/
|-- README.md
|-- REPRODUCTION_GUIDE.md
|-- configs/
|   `-- preprocessing/
|-- scripts/
|   |-- create_data_samples.py
|   |-- extract_processed_mini_samples.py
|   |-- validate_data_samples.py
|   `-- preprocessing/
|       |-- prepare_all_csvs.py
|       |-- build_all_frames.py
|       |-- verify_raw_data.py
|       `-- validate_npz_frames.py
`-- data_samples/
    |-- README.md
    |-- DATA_SOURCES.md
    |-- data_format_specification.md
    |-- VALIDATION_REPORT.md
    `-- data/
        |-- test_set_samples/
        |-- survival_frame_samples/
        |-- audit_samples/
        |-- result_samples/
        |-- hpo_samples/
        |-- processed_mini_samples/
        `-- quick_view/
```

## Quick Start

```bash
python scripts/create_data_samples.py
python scripts/extract_processed_mini_samples.py
python scripts/validate_data_samples.py
```

## Original Dataset Sources

This repository provides lightweight sample files and derived mini frames only. It does not redistribute full raw datasets or full processed benchmark frames.

Original upstream sources are documented in:

- `data_samples/DATA_SOURCES.md`

Dataset source summary:

| Dataset ID | Upstream source |
| --- | --- |
| `azure` | Microsoft Azure Predictive Maintenance / PdM sample data |
| `scania` | SCANIA Component X Dataset, DOI: https://doi.org/10.5878/bnh5-ka77 |
| `cmapss_fd001`-`cmapss_fd004` | NASA C-MAPSS / Turbofan Engine Degradation Simulation Data Set |

Important: in this repository, `scania` refers to SCANIA Component X, not UCI APS Failure at Scania Trucks.

## Raw-to-frame Preprocessing

The repository includes preprocessing scripts under `scripts/preprocessing/` for converting manually downloaded upstream data into project-compatible `.npz` survival frames.

The local data-preparation chain is:

```text
manually downloaded upstream files -> project-prepared CSV inputs -> project-compatible .npz survival frames
```

See [REPRODUCTION_GUIDE.md](REPRODUCTION_GUIDE.md).

The repository does not redistribute full raw datasets, full processed frames, trained weights, or model checkpoints.

## Main Data Format

The central format is a multi-horizon survival frame with metadata columns, event and censoring labels, feature-summary columns, and a processed mini subset derived from the real pipeline frames.

## Validation

The validator checks required files, JSON and CSV readability, event and duration validity, censoring-rate range, horizon monotonicity, feature leakage column names, HPO trace consistency, processed mini frame coverage, and file-size constraints.

## Citation / Paper Placeholder

If you use this sample repository, please cite the associated OCEAN-MO-CDSF paper once available.

## License / Data Note

The repository contains two types of files: illustrative synthetic examples for schema demonstration, and small anonymized processed mini samples extracted from the OCEAN-MO-CDSF processed survival-frame files. It does not redistribute full raw datasets or full benchmark frames.
