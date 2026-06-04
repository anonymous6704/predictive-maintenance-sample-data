# Audit Samples

## Purpose

This folder contains compact examples of dataset auditing, feature leakage review, and unit-level split checking.

## Files

- `dataset_audit_sample.csv`
- `feature_leakage_audit_sample.csv`
- `split_audit_sample.csv`

## Format Summary

CSV audit tables with pass or fail style statuses and simple boolean-like fields.

## Example Rows

```csv
dataset,censoring_rate,samples,units,event_rate,censoring_rate_observed,duration_median,padding_rate,missing_rate,fallback,status
azure,0.0,120,14,0.42,0.08,18.4,0.01,0.02,false,pass
```

## Python Loading Example

```python
import pandas as pd

dataset_audit = pd.read_csv("data_samples/data/audit_samples/dataset_audit_sample.csv")
print(dataset_audit[["dataset", "event_rate", "status"]])
```

## Notes and Warnings

- Dataset audits summarize censoring, duration, missingness, and fallback state.
- Feature leakage audits should confirm that forbidden tokens do not appear in feature names.
- Split audits should be unit-disjoint with `overlap_unit_count = 0` for passed rows.
