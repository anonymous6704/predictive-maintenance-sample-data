# Survival Frame Samples

## Purpose

This folder contains compact survival-frame rows that demonstrate the tabular format used by OCEAN-MO-CDSF.

## Files

- `survival_frame_sample.csv`
- `survival_frame_schema.json`
- `survival_frame_column_dictionary.csv`

## Format Summary

CSV table with target, metadata, and feature columns plus a column dictionary.

## Example Row

```csv
sample_id,dataset,unit_id,anchor_time,duration,event,event_type,censoring_rate,horizon_1,horizon_2,horizon_3,horizon_4,static_feature_1,static_feature_2,seq_feature_mean_1,seq_feature_std_1,seq_feature_last_1,missing_rate,padding_rate
SF_001,azure,unit_0001,2026-05-01T08:00:00Z,96,1,observed_failure,0.0,24,72,168,336,0.45,0.12,0.62,0.08,0.70,0.00,0.00
```

## Python Loading Example

```python
import pandas as pd

df = pd.read_csv("data_samples/data/survival_frame_samples/survival_frame_sample.csv")
print(df.head())
```

## Notes and Warnings

- `duration`, `event`, `event_type`, `unit_id`, and `anchor_time` are labels or metadata and must not be used as predictive features.
- The column dictionary defines which columns are intended for features.
- `missing_rate` and `padding_rate` are metadata by default unless explicitly promoted.
