# OCEAN-MO-CDSF Dataset Samples

## Overview

This folder contains sample data structures used by the OCEAN-MO-CDSF framework for censored predictive-maintenance survival analysis.

The samples illustrate data schemas, censoring/event labels, survival frames, audit tables, model-result records, and HPO traces.

These are small illustrative samples, not the full dataset.

No raw industrial data, model weights, checkpoints, or private data are included.

## Dataset Components

- Test Set Samples
- Survival Frame Samples
- Audit Samples
- Result Samples
- HPO Samples

## Directory Tree

```text
data_samples/
|-- README.md
|-- data_format_specification.md
|-- .gitignore
|-- data/
    |-- test_set_samples/
    |   |-- README.md
    |   |-- sample_survival_cases.json
    |   `-- sample_survival_cases_schema.json
    |-- survival_frame_samples/
    |   |-- README.md
    |   |-- survival_frame_sample.csv
    |   |-- survival_frame_schema.json
    |   `-- survival_frame_column_dictionary.csv
    |-- audit_samples/
    |   |-- README.md
    |   |-- dataset_audit_sample.csv
    |   |-- feature_leakage_audit_sample.csv
    |   `-- split_audit_sample.csv
    |-- result_samples/
    |   |-- README.md
    |   `-- model_result_sample.csv
    `-- hpo_samples/
        |-- README.md
        |-- hpo_selected_config_sample.json
        `-- hpo_candidate_trace_sample.csv
```

## Test Set Samples

### Purpose
Illustrative survival test cases showing observed failures, right-censoring, administrative censoring, padding, and missingness.

### Main Files
- `data/test_set_samples/sample_survival_cases.json`
- `data/test_set_samples/sample_survival_cases_schema.json`

### Format
JSON array of compact case records with a companion JSON schema.

### Example Use
Load a small set of survival cases for documentation, schema checks, and reader-facing examples.

## Survival Frame Samples

### Purpose
Illustrative tabular survival frame records for censored predictive-maintenance modeling.

### Main Files
- `data/survival_frame_samples/survival_frame_sample.csv`
- `data/survival_frame_samples/survival_frame_schema.json`
- `data/survival_frame_samples/survival_frame_column_dictionary.csv`

### Format
CSV table with target, metadata, and feature columns plus a column dictionary.

### Example Use
Load the survival frame into pandas, validate columns, and build feature matrices that exclude outcome and metadata fields.

## Audit Samples

### Purpose
Compact dataset-audit, leakage-audit, and split-audit records for reproducibility and review.

### Main Files
- `data/audit_samples/dataset_audit_sample.csv`
- `data/audit_samples/feature_leakage_audit_sample.csv`
- `data/audit_samples/split_audit_sample.csv`

### Format
CSV audit tables with pass/fail style statuses and simple boolean-like fields.

### Example Use
Load audits during documentation review to confirm censoring coverage, leakage checks, and unit-level splits.

## Result Samples

### Purpose
Illustrative model-result records that separate validation selection from final test reporting.

### Main Files
- `data/result_samples/model_result_sample.csv`

### Format
CSV table with validation and test metrics, runtime, and selection flags.

### Example Use
Load a result table to compare model families and trace which configuration was selected by validation.

## HPO Samples

### Purpose
Illustrative hyperparameter-optimization traces and selected configurations.

### Main Files
- `data/hpo_samples/hpo_selected_config_sample.json`
- `data/hpo_samples/hpo_candidate_trace_sample.csv`

### Format
JSON plus CSV showing selected configurations, multi-fidelity promotions, and candidate trace history.

### Example Use
Load the selected config JSON, inspect the candidate trace, and explain how validation metrics drove the final choice.

## Usage Examples

```python
import csv
import json
from pathlib import Path

root = Path("data_samples/data")

with open(root / "test_set_samples" / "sample_survival_cases.json", "r", encoding="utf-8") as f:
    cases = json.load(f)

with open(root / "survival_frame_samples" / "survival_frame_sample.csv", "r", encoding="utf-8", newline="") as f:
    rows = list(csv.DictReader(f))

with open(root / "audit_samples" / "dataset_audit_sample.csv", "r", encoding="utf-8", newline="") as f:
    audits = list(csv.DictReader(f))
```

```python
import csv
import json

with open("data_samples/data/hpo_samples/hpo_selected_config_sample.json", "r", encoding="utf-8") as f:
    selected = json.load(f)

with open("data_samples/data/hpo_samples/hpo_candidate_trace_sample.csv", "r", encoding="utf-8", newline="") as f:
    candidates = list(csv.DictReader(f))
```

## Notes

- `event=1` means observed failure.
- `event=0` means right-censored.
- Test metrics are reported only after validation selection.
- C-MAPSS administrative censoring is a stress-test setting if used.
- SurvSHAP-style explanations, if used elsewhere in the paper, are model-behavior explanations, not causal claims.
- These samples are for format demonstration only.

## Anonymization and Research Use

All values in this folder are synthetic or anonymized and are intended for reproducibility, schema demonstration, and documentation. They are not a substitute for the full benchmark dataset or any proprietary industrial data.
