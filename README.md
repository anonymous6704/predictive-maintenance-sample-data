# Predictive Maintenance Sample Data

This repository provides small illustrative data samples for the OCEAN-MO-CDSF predictive-maintenance survival-analysis framework.

It is not the full benchmark dataset.
It contains no raw industrial data.
It contains no model weights.
It contains no private or sensitive information.
All values are illustrative, anonymized, and synthetic for format demonstration.

Main documentation:

- [data_samples/README.md](data_samples/README.md)

Quick usage:

```powershell
python scripts/create_data_samples.py
python scripts/validate_data_samples.py
```

Directory overview:

- `data_samples/`: illustrative sample-data bundle for OCEAN-MO-CDSF
- `scripts/`: generator and validation utilities

Notes:

- `event=1` means an observed failure.
- `event=0` means right-censored.
- Test metrics are reported only after validation selection.
- C-MAPSS administrative censoring is a stress-test setting if used.
- SurvSHAP-style explanations, if used elsewhere in the paper, are model-behavior explanations, not causal claims.
