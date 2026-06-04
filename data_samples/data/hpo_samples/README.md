# HPO Samples

## Purpose

This folder contains compact hyperparameter-optimization examples for the OCEAN-MO-CDSF workflow.

## Files

- `hpo_selected_config_sample.json`
- `hpo_candidate_trace_sample.csv`

## Format Summary

JSON selected configurations plus a CSV candidate trace showing multi-fidelity promotion behavior.

## Example Snippets

```json
{
  "dataset": "azure",
  "model": "ocean_gru_kan",
  "search_method": "random_search",
  "selected_by_validation": true
}
```

```csv
dataset,censoring_rate,seed,model,search_method,candidate_id,fidelity_level,promoted,validation_calibrated_monotone_ipcw_ibs,runtime_sec,config_hash
azure,0.0,0,ocean_gru_kan,random_search,rs-001,fidelity_1,true,0.218,1.2,ogk-0a31f7c1
```

## Python Loading Example

```python
import csv
import json

with open("data_samples/data/hpo_samples/hpo_selected_config_sample.json", "r", encoding="utf-8") as f:
    selected = json.load(f)

with open("data_samples/data/hpo_samples/hpo_candidate_trace_sample.csv", "r", encoding="utf-8", newline="") as f:
    trace = list(csv.DictReader(f))
```

## Notes and Warnings

- `random_search` and `ga_amfpo` are example search methods.
- `fidelity_1` and `fidelity_2` are screening stages, while `fidelity_3` represents the final evidence stage.
- `promoted=true` indicates a candidate advanced to a higher-fidelity evaluation.
- Test metrics are report-only for selected configurations.
