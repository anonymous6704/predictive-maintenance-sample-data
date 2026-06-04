# HPO Samples

## Purpose

This folder contains compact hyperparameter-optimization examples for the OCEAN-MO-CDSF workflow.

## File Descriptions

- `hpo_selected_config_sample.json`: selected configurations for representative models
- `hpo_candidate_trace_sample.csv`: candidate trace showing multi-fidelity promotion behavior

## HPO Candidate Notes

- `random_search` and `ga_amfpo` are shown as example search methods.
- `fidelity_1`, `fidelity_2`, and `fidelity_3` show a multi-fidelity progression.
- `promoted=true` indicates that a candidate advanced to a higher-fidelity evaluation.

## Validation vs Test Separation

Test metrics are reported only after the selected configuration is fixed by validation.

## Python Load Example

```python
import csv
import json

with open("data_samples/data/hpo_samples/hpo_selected_config_sample.json", "r", encoding="utf-8") as f:
    selected = json.load(f)

with open("data_samples/data/hpo_samples/hpo_candidate_trace_sample.csv", "r", encoding="utf-8", newline="") as f:
    trace = list(csv.DictReader(f))
```
