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

## What This Repository Does Not Contain

- It does not contain the full benchmark dataset.
- It does not redistribute raw Azure, Scania, or C-MAPSS data.
- It does not contain model checkpoints, trained weights, raw industrial logs, or private data.
- It does not contain ontology, KG, or graph data.

## Directory Structure

```text
predictive-maintenance-sample-data/
├── README.md
├── .gitignore
├── scripts/
│   ├── create_data_samples.py
│   ├── extract_processed_mini_samples.py
│   └── validate_data_samples.py
└── data_samples/
    ├── README.md
    ├── data_format_specification.md
    ├── VALIDATION_REPORT.md
    └── data/
        ├── README.md
        ├── test_set_samples/
        ├── survival_frame_samples/
        ├── audit_samples/
        ├── result_samples/
        ├── hpo_samples/
        ├── processed_mini_samples/
        └── quick_view/
```

## Quick Start

```bash
python scripts/create_data_samples.py
python scripts/extract_processed_mini_samples.py
python scripts/validate_data_samples.py
```

## Main Data Format

The central format is a multi-horizon survival frame with metadata columns, event and censoring labels, feature-summary columns, and a processed mini subset derived from the real pipeline frames.

## Validation

The validator checks required files, JSON and CSV readability, event and duration validity, censoring-rate range, horizon monotonicity, feature leakage column names, HPO trace consistency, processed mini frame coverage, and file-size constraints.

## Citation / Paper Placeholder

If you use this sample repository, please cite the associated OCEAN-MO-CDSF paper once available.

## License / Data Note

All provided values are illustrative and anonymized or synthetic for format demonstration.
