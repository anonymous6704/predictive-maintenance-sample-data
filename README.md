# Predictive Maintenance Sample Data

## Overview

This repository provides small illustrative data samples for the OCEAN-MO-CDSF framework, an evidence-driven multi-objective deep survival framework for censored predictive maintenance.

## What This Repository Contains

- Survival test cases
- Survival frame samples
- Audit table samples
- Model result samples
- HPO trace samples
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
        └── hpo_samples/
```

## Quick Start

```bash
python scripts/create_data_samples.py
python scripts/validate_data_samples.py
```

## Main Data Format

The central format is a multi-horizon survival frame with metadata columns, event/censoring labels, and feature-summary columns.

## Validation

The validator checks required files, JSON and CSV readability, event and duration validity, censoring-rate range, horizon monotonicity, feature leakage column names, and HPO trace consistency.

## Citation / Paper Placeholder

If you use this sample repository, please cite the associated OCEAN-MO-CDSF paper once available.

## License / Data Note

All provided values are illustrative and anonymized/synthetic for format demonstration.
