# Test Set Samples

## Purpose

This folder provides small survival test-case examples for the OCEAN-MO-CDSF format. The cases show observed failures, right-censoring, administrative censoring, padding, and missingness.

## Files

- `sample_survival_cases.json`
- `sample_survival_cases_schema.json`

## Format Summary

JSON array of compact case records with a companion JSON schema.

## Example JSON Snippet

```json
{
  "case_id": "azure_recurrent_obs_01",
  "dataset": "azure",
  "unit_id": "AZ-1001",
  "event": 1,
  "event_type": "observed_failure"
}
```

## Python Loading Example

```python
import json

with open("data_samples/data/test_set_samples/sample_survival_cases.json", "r", encoding="utf-8") as f:
    payload = json.load(f)
cases = payload["cases"]
```

## Notes and Warnings

- `event=1` means observed failure.
- `event=0` means right-censored.
- `expected_behavior` explains the intended interpretation of the case.
- All values are illustrative, synthetic, and anonymized.
