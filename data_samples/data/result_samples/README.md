# Result Samples

## Purpose

This folder contains small model-result records that demonstrate validation selection and final test reporting.

## Files

- `model_result_sample.csv`

## Format Summary

CSV table with selection metrics, test metrics, ranking metrics, calibration metrics, cost, interval width, and runtime.

## Example Row

```csv
dataset,censoring_rate,seed,model,validation_calibrated_monotone_ipcw_ibs,test_calibrated_monotone_ipcw_ibs,c_index,ece,cost_top10,riw,runtime_sec,selected_by_validation
azure,0.0,0,ocean_transformer_kan,0.143,0.150,0.83,0.03,0.09,0.85,15.1,true
```

## Python Loading Example

```python
import pandas as pd

results = pd.read_csv("data_samples/data/result_samples/model_result_sample.csv")
print(results.sort_values("validation_calibrated_monotone_ipcw_ibs").head())
```

## Notes and Warnings

- Validation metrics are used for model selection.
- Test metrics are reported only after the selected model or configuration is fixed.
- `validation_calibrated_monotone_ipcw_ibs` and `test_calibrated_monotone_ipcw_ibs` are lower-is-better metrics.
- `c_index` is a discrimination metric, `ece` is a calibration error, `cost_top10` is a top-risk cost summary, `riw` is an interval-width summary, and `runtime_sec` is wall-clock time.
