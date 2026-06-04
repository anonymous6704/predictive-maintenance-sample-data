# Audit Samples

## Purpose

These audit tables provide compact examples of dataset auditing, feature leakage review, and unit-level split checking.

## File Descriptions

- `dataset_audit_sample.csv`: dataset-level quality and censoring summary
- `feature_leakage_audit_sample.csv`: feature leakage review summary
- `split_audit_sample.csv`: unit-level split integrity summary

## Audit Interpretation

- `status` indicates pass or fail.
- `fallback=false` means the sample is shown without synthetic fallback rows.
- Feature leakage audits should confirm that outcome or metadata fields are not exposed as model features.
- Split audits should show no overlap in units across training, calibration, validation, and test partitions.

## Python Load Example

```python
import csv

with open("data_samples/data/audit_samples/dataset_audit_sample.csv", "r", encoding="utf-8", newline="") as f:
    dataset_audit = list(csv.DictReader(f))
```
