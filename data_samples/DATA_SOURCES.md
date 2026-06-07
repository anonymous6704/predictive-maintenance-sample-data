# Original Dataset Sources

This repository contains lightweight schema-valid samples and derived mini frames for inspection, validation, and artifact review.

It does not redistribute:
- full raw datasets,
- full processed benchmark frames,
- model checkpoints,
- trained weights,
- private industrial logs.

Full benchmark reproduction requires downloading the upstream datasets listed below and rerunning the preprocessing, training, model-selection, and evaluation pipeline.

## Dataset provenance table

| Dataset ID in this repository | Correct upstream dataset | Source / download links | Used as | Notes |
|---|---|---|---|---|
| `azure` | Microsoft Azure Predictive Maintenance / PdM sample data | Source folder: https://github.com/microsoft/sqlworkshops/tree/master/SQLServerAndAzureMachineLearning/ML%20Services%20for%20SQL%20Server/data ; files: `PdM_telemetry.csv`, `PdM_errors.csv`, `PdM_failures.csv`, `PdM_machines.csv`, `PdM_maint.csv` | Public PdM source data transformed by the project preprocessing scripts | Any merged `azure_pdm` file or survival-frame file in this repository is derived from the upstream source files, not an untouched raw upstream package. |
| `scania` | SCANIA Component X Dataset: A Real-World Multivariate Time Series Dataset for Predictive Maintenance | Dataset page: https://researchdata.se/en/catalogue/dataset/2024-34 ; latest dataset DOI: https://doi.org/10.5878/bnh5-ka77 ; Scientific Data paper DOI: https://doi.org/10.1038/s41597-025-04802-6 | Large real-world multivariate time-series predictive-maintenance dataset transformed into survival/time-to-event frames | This is the correct source for `scania` in this repository. The full dataset is approximately 11 files / 1.54 GiB. Key upstream files include `train_operational_readouts.csv`, `test_operational_readouts.csv`, `validation_operational_readouts.csv`, `train_tte.csv`, `train_specifications.csv`, `test_labels.csv`, `validation_labels.csv`, and specification files. |
| `cmapss_fd001` | NASA C-MAPSS / Turbofan Engine Degradation Simulation Data Set, FD001 | NASA Open Data metadata: https://data.nasa.gov/dataset/cmapss-jet-engine-simulated-data ; NASA/DASHlink legacy source: https://c3.ndc.nasa.gov/dashlink/resources/139/ | Turbofan run-to-failure simulation subset transformed into survival-frame samples | FD001 has one operating condition and one fault mode. |
| `cmapss_fd002` | NASA C-MAPSS / Turbofan Engine Degradation Simulation Data Set, FD002 | NASA Open Data metadata: https://data.nasa.gov/dataset/cmapss-jet-engine-simulated-data ; NASA/DASHlink legacy source: https://c3.ndc.nasa.gov/dashlink/resources/139/ | Turbofan run-to-failure simulation subset transformed into survival-frame samples | FD002 has multiple operating conditions and one fault mode. |
| `cmapss_fd003` | NASA C-MAPSS / Turbofan Engine Degradation Simulation Data Set, FD003 | NASA Open Data metadata: https://data.nasa.gov/dataset/cmapss-jet-engine-simulated-data ; NASA/DASHlink legacy source: https://c3.ndc.nasa.gov/dashlink/resources/139/ | Turbofan run-to-failure simulation subset transformed into survival-frame samples | FD003 has one operating condition and two fault modes. |
| `cmapss_fd004` | NASA C-MAPSS / Turbofan Engine Degradation Simulation Data Set, FD004 | NASA Open Data metadata: https://data.nasa.gov/dataset/cmapss-jet-engine-simulated-data ; NASA/DASHlink legacy source: https://c3.ndc.nasa.gov/dashlink/resources/139/ | Turbofan run-to-failure simulation subset transformed into survival-frame samples | FD004 has multiple operating conditions and two fault modes. |

## Direct upstream files and download notes

### Azure PdM

Primary source folder:

```text
https://github.com/microsoft/sqlworkshops/tree/master/SQLServerAndAzureMachineLearning/ML%20Services%20for%20SQL%20Server/data
```

Expected upstream files:

```text
PdM_telemetry.csv
PdM_errors.csv
PdM_failures.csv
PdM_machines.csv
PdM_maint.csv
```

Do not document a merged `azure_pdm` file as raw upstream data. It is a project-derived file if it was created by joining or transforming the five upstream CSV files.

### SCANIA Component X

Primary dataset page:

```text
https://researchdata.se/en/catalogue/dataset/2024-34
```

Latest dataset DOI:

```text
https://doi.org/10.5878/bnh5-ka77
```

Associated Scientific Data paper:

```text
https://doi.org/10.1038/s41597-025-04802-6
```

Expected upstream files include:

```text
train_operational_readouts.csv
test_operational_readouts.csv
validation_operational_readouts.csv
train_tte.csv
train_specifications.csv
test_labels.csv
validation_labels.csv
test_specifications.csv
validation_specifications.csv
2024_IDA_challenge_v2.pdf
Scania_Component_X.pdf
```

Important:
`scania` in this repository means SCANIA Component X. It must not be linked to UCI APS Failure at Scania Trucks.

### NASA C-MAPSS

NASA Open Data metadata page:

```text
https://data.nasa.gov/dataset/cmapss-jet-engine-simulated-data
```

NASA/DASHlink legacy source:

```text
https://c3.ndc.nasa.gov/dashlink/resources/139/
```

NASA Open Data describes C-MAPSS as multiple multivariate time series split into training and test subsets, with each time series representing a different engine. The FD001-FD004 subsets differ by operating conditions and fault modes.

## Important distinction: SCANIA Component X vs UCI APS

This repository must not conflate two different Scania datasets.

`SCANIA Component X` is a large real-world multivariate time-series predictive-maintenance dataset with operational readouts, truck specifications, repair information, and time-to-event information. It is the correct source for repository samples with fields such as:

```text
unit_id
time_index
duration
event
spec_Cat*
```

`APS Failure at Scania Trucks` from the UCI Machine Learning Repository is a different and smaller classification dataset focused on Air Pressure System failures. It is not the provenance source for `scania_survival_samples` or SCANIA Component X-derived files in this repository.

Do not cite UCI APS for the `scania` dataset unless a separate APS-derived sample is explicitly added and documented under a different dataset ID, such as `scania_aps`.

## Full data policy

This repository does not redistribute the full raw or full processed benchmark datasets.

The sample files are intended for:

* schema inspection,
* validator testing,
* artifact provenance review,
* lightweight examples for reviewers.

They are not sufficient to reproduce full paper-scale benchmark metrics.

Full reproduction requires:

1. downloading the original datasets from the upstream sources listed above,
2. running the preprocessing pipeline,
3. running training and validation-based model selection,
4. reporting test metrics only after selection.

Large derived files such as full SCANIA survival frames or merged Azure PdM frames should not be tracked in Git. If full derived artifacts are released, place them in Zenodo, OSF, Figshare, GitHub Releases, Hugging Face datasets, or a DVC remote, and document checksums.
