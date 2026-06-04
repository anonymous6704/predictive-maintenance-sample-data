# Result Samples

## Purpose

This folder contains small model-result records that demonstrate the separation between validation selection and final test reporting.

## File Descriptions

- `model_result_sample.csv`: compact per-model result table

## Metric Notes

- `validation_calibrated_monotone_ipcw_ibs`: validation-time selection metric
- `test_calibrated_monotone_ipcw_ibs`: final reporting metric, shown only after validation selection
- `c_index`: concordance-style ranking metric
- `ece`: calibration error
- `cost_top10`: cost-based top-10 measure
- `riw`: relative information weight or related efficiency score used in the paper workflow
- `runtime_sec`: wall-clock runtime in seconds
- `selected_by_validation`: indicates which row won validation-based selection

## Python Load Example

```python
import csv

with open("data_samples/data/result_samples/model_result_sample.csv", "r", encoding="utf-8", newline="") as f:
    rows = list(csv.DictReader(f))
```

## Validation vs Test Separation

Validation metrics drive model selection. Test metrics are reported only after the selected configuration is fixed.
