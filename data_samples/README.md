# OCEAN-MO-CDSF Dataset Samples

## Overview

This folder documents the sample data formats used by OCEAN-MO-CDSF for censored predictive-maintenance survival analysis.

## Purpose

- Inspect the expected survival-frame schema
- Understand event and censoring labels
- Understand audit-table formats
- Understand model-result and HPO-trace formats
- Run lightweight validation without full raw datasets

## Dataset Components

| Component | Folder | Purpose | Main files |
| --- | --- | --- | --- |
| Test set samples | `data/test_set_samples/` | Survival and censoring case examples | `sample_survival_cases.json` |
| Survival frame samples | `data/survival_frame_samples/` | Model input frame format | `survival_frame_sample.csv` |
| Audit samples | `data/audit_samples/` | Data, leakage, and split audit examples | `dataset_audit_sample.csv`, `feature_leakage_audit_sample.csv`, `split_audit_sample.csv` |
| Result samples | `data/result_samples/` | Benchmark metric table example | `model_result_sample.csv` |
| HPO samples | `data/hpo_samples/` | Selected config and candidate trace examples | `hpo_selected_config_sample.json`, `hpo_candidate_trace_sample.csv` |

If present, `data/quick_view/` may provide convenience copies and `data/processed_mini_samples/` may provide small processed or anonymized mini frames.

## Directory Tree

```text
data_samples/
├── README.md
├── .gitignore
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

## Usage Examples

```python
import json
from pathlib import Path

path = Path("data_samples/data/test_set_samples/sample_survival_cases.json")
cases = json.loads(path.read_text(encoding="utf-8"))
print(cases["cases"][0] if isinstance(cases, dict) else cases[0])
```

```python
import pandas as pd

df = pd.read_csv("data_samples/data/survival_frame_samples/survival_frame_sample.csv")
print(df.head())
```

```python
audit = pd.read_csv("data_samples/data/audit_samples/dataset_audit_sample.csv")
print(audit[["dataset", "event_rate", "status"]])
```

```python
results = pd.read_csv("data_samples/data/result_samples/model_result_sample.csv")
print(results.sort_values("validation_calibrated_monotone_ipcw_ibs").head())
```

```python
trace = pd.read_csv("data_samples/data/hpo_samples/hpo_candidate_trace_sample.csv")
print(trace.groupby(["model", "fidelity_level"]).size())
```

## Event and Censoring Interpretation

- `event=1`: observed failure
- `event=0`: right-censored
- `duration`: observed time-to-event or time-to-censoring
- `censoring_rate`: administrative censoring setting or scenario indicator
- `censoring_rate_observed`: observed censoring proportion in an audit table

## Feature Leakage Warning

`duration`, `event`, `event_type`, `unit_id`, `anchor_time`, `failure_time`, `rul`, and `censor_time` must not be used as predictive features.

## Validation and Test Separation

Validation metrics are used for model selection. Test metrics are reported only after the selected model or configuration is fixed.

## Data Availability Note

These files are sufficient for schema inspection and validator testing, not for reproducing paper-scale benchmark metrics.
