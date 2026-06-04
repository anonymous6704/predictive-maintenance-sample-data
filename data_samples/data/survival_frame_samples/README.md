# Survival Frame Samples

## Purpose

This folder contains compact survival-frame rows that demonstrate the tabular format used by OCEAN-MO-CDSF.

## File Descriptions

- `survival_frame_sample.csv`: illustrative survival-frame records
- `survival_frame_schema.json`: schema describing the CSV columns
- `survival_frame_column_dictionary.csv`: column-level roles and usage flags

## Column-Role Explanation

- Identifier and metadata fields describe the unit, anchor time, censoring setup, or sample identity.
- Outcome fields describe the survival target and must not be used as predictive features.
- Feature fields are the only columns intended for model inputs.
- `missing_rate` and `padding_rate` are kept as metadata by default unless a specific experiment intentionally promotes them to features.

## Python Load Example

```python
import csv

with open("data_samples/data/survival_frame_samples/survival_frame_sample.csv", "r", encoding="utf-8", newline="") as f:
    rows = list(csv.DictReader(f))
```

## Warning

Outcome and metadata columns must not be used as predictive features.
