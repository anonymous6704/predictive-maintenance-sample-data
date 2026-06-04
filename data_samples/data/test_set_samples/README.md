# Test Set Samples

## Purpose

This folder provides small survival test-case examples for the OCEAN-MO-CDSF format. The cases show observed failures, right-censoring, administrative censoring, short padded sequences, and missing sensor values.

## File Descriptions

- `sample_survival_cases.json`: illustrative case records
- `sample_survival_cases_schema.json`: JSON schema for the case file

## JSON Snippet

```json
{
  "case_id": "azure_recurrent_obs_01",
  "dataset": "azure",
  "unit_id": "AZ-1001",
  "event": 1,
  "event_type": "observed_failure"
}
```

## Python Load Example

```python
import json

with open("data_samples/data/test_set_samples/sample_survival_cases.json", "r", encoding="utf-8") as f:
    payload = json.load(f)

cases = payload["cases"]
```

## Notes on Event and Censoring Interpretation

- `event=1` means observed failure.
- `event=0` means right-censored.
- Administrative censoring is a simulated stress-test setting, especially for C-MAPSS-derived examples.

## Anonymization Note

All values in this folder are illustrative, synthetic, and anonymized.
