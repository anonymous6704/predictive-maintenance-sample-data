# Data Format Specification

This document provides detailed specifications for all sample data formats used in the OCEAN-MO-CDSF predictive-maintenance survival-analysis sample repository.

## Table of Contents

1. Test Set Format
2. Survival Frame Format
3. Audit Table Formats
4. Result Table Format
5. HPO Format
6. Metadata Fields
7. Data Types
8. Validation Rules
9. Encoding and Special Characters
10. File Naming Conventions
11. Version Information

## 1. Test Set Format
- Format: JSON
- Encoding: UTF-8
- Structure: array of objects

### Object Schema
```json
{
  "case_id": "string (required)",
  "dataset": "enum/string (required)",
  "unit_id": "string (required)",
  "anchor_time": "string (required)",
  "sequence_length": "integer (required)",
  "horizon_grid": ["array of integers (required)"],
  "duration": "number (required)",
  "event": "integer enum 0/1 (required)",
  "event_type": "string (required)",
  "censoring_type": "enum/string (required)",
  "feature_summary": "string (required)",
  "expected_behavior": "string (required)",
  "notes": "string (optional)"
}
```

### Field Descriptions
| Field | Type | Required | Description |
| --- | --- | --- | --- |
| case_id | string | Yes | Unique sample case identifier |
| dataset | string/enum | Yes | Dataset family such as `azure`, `scania`, `cmapss_fd001`, or `cmapss_fd004` |
| unit_id | string | Yes | Anonymized unit identifier |
| anchor_time | string | Yes | Prediction anchor time in ISO 8601 format |
| sequence_length | integer | Yes | Number of historical timesteps |
| horizon_grid | array[number] | Yes | Prediction horizons |
| duration | number | Yes | Observed time-to-event or time-to-censoring |
| event | integer | Yes | `1` means observed failure and `0` means right-censored |
| event_type | string | Yes | Human-readable event category |
| censoring_type | string | Yes | `none`, `right_censored`, or `administrative_censoring_*` |
| feature_summary | string | Yes | Compact feature summary for illustration |
| expected_behavior | string | Yes | Expected validator or model interpretation |
| notes | string | No | Additional explanation |

## 2. Survival Frame Format
- Format: CSV
- Encoding: UTF-8
- Header: first row contains column names
- Delimiter: comma

### Column Schema
| Column | Type | Required | Role | Description |
| --- | --- | --- | --- | --- |
| sample_id | string | Yes | metadata | Unique sample or anchor identifier |
| dataset | string | Yes | metadata | Dataset family |
| unit_id | string | Yes | metadata | Anonymized unit identifier |
| anchor_time | string | Yes | metadata | Prediction anchor |
| duration | number | Yes | label | Observed time-to-event or censoring |
| event | integer | Yes | label | `1` observed event, `0` censored |
| event_type | string | Yes | label | Event code or label |
| censoring_rate | number | Yes | metadata | Administrative censoring setting or scenario |
| horizon_1 | number | Yes | metadata | First prediction horizon |
| horizon_2 | number | Yes | metadata | Second prediction horizon |
| horizon_3 | number | Yes | metadata | Third prediction horizon |
| horizon_4 | number | Yes | metadata | Fourth prediction horizon |
| static_feature_1 | number | Yes | feature | Example static covariate |
| static_feature_2 | number | Yes | feature | Example static covariate |
| seq_feature_mean_1 | number | Yes | feature | Sequence summary mean |
| seq_feature_std_1 | number | Yes | feature | Sequence summary standard deviation |
| seq_feature_last_1 | number | Yes | feature | Last observed sequence value |
| missing_rate | number | Yes | metadata/quality | Fraction missing; metadata by default unless explicitly promoted to a feature |
| padding_rate | number | Yes | metadata/quality | Fraction padded; metadata by default unless explicitly promoted to a feature |

### Important
Label and metadata columns are included for dataset construction and evaluation, but they must not be used as model features unless explicitly allowed by a column dictionary. `survival_frame_column_dictionary.csv` specifies `used_as_feature`.

## 3. Audit Table Formats
### 3.1 Dataset Audit
- Format: CSV
- Encoding: UTF-8

| Column | Type | Required | Description |
| --- | --- | --- | --- |
| dataset | string | Yes | Dataset family |
| censoring_rate | number | Yes | Censoring setting |
| samples | integer | Yes | Number of sample anchors |
| units | integer | Yes | Number of unique units |
| event_rate | number | Yes | Proportion of event=1 samples |
| censoring_rate_observed | number | Yes | Proportion of censored samples |
| duration_median | number | Yes | Median observed duration |
| padding_rate | number | Yes | Mean padding rate |
| missing_rate | number | Yes | Mean missing rate |
| fallback | boolean | Yes | Whether fallback or synthetic data was used |
| status | enum | Yes | `passed` or `failed` |

### 3.2 Feature Leakage Audit
| Column | Type | Required | Description |
| --- | --- | --- | --- |
| dataset | string | Yes | Dataset |
| censoring_rate | number | Yes | Censoring setting |
| seq_feature_count | integer | Yes | Number of sequence feature columns |
| static_feature_count | integer | Yes | Number of static feature columns |
| bad_seq_features | string | No | Forbidden sequence features |
| bad_static_features | string | No | Forbidden static features |
| status | enum | Yes | `passed` or `failed` |

### 3.3 Split Audit
| Column | Type | Required | Description |
| --- | --- | --- | --- |
| dataset | string | Yes | Dataset |
| censoring_rate | number | Yes | Censoring setting |
| seed | integer | Yes | Split seed |
| train_units | integer | Yes | Number of training units |
| calibration_units | integer | Yes | Number of calibration units |
| validation_units | integer | Yes | Number of validation units |
| test_units | integer | Yes | Number of test units |
| overlap_unit_count | integer | Yes | Unit overlap across splits |
| status | enum | Yes | `passed` or `failed` |

## 4. Result Table Format
- Format: CSV
- Encoding: UTF-8

| Column | Type | Required | Description |
| --- | --- | --- | --- |
| dataset | string | Yes | Dataset family |
| censoring_rate | number | Yes | Censoring setting |
| seed | integer | Yes | Random or split seed |
| model | string | Yes | Model name |
| validation_calibrated_monotone_ipcw_ibs | number | Yes | Validation selection metric |
| test_calibrated_monotone_ipcw_ibs | number | Yes | Test metric reported after selection |
| c_index | number | Yes | Concordance metric |
| ece | number | Yes | Expected calibration error |
| cost_top10 | number | Yes | Maintenance cost for the top-risk subset |
| riw | number | Yes | Relative interval width |
| runtime_sec | number | Yes | Runtime in seconds |
| selected_by_validation | boolean | Yes | Whether selected by validation criterion |

Lower IPCW-IBS is better, higher C-index is better, and test metrics must not be used for selection.

## 5. HPO Format
### 5.1 Selected Config JSON
- Format: JSON
- Encoding: UTF-8
- Structure: array of objects

```json
{
  "dataset": "string (required)",
  "censoring_rate": "number (required)",
  "seed": "integer (required)",
  "model": "string (required)",
  "search_method": "enum/string (required)",
  "config_hash": "string (required)",
  "fidelity_level": "string (required)",
  "hyperparameters": "object (required)",
  "validation_metric": "object (required)",
  "test_metric_reported_only": "object (required)",
  "selected_by_validation": "boolean (required)"
}
```

Hyperparameter examples include `hidden_dim`, `num_layers`, `dropout`, `learning_rate`, `batch_size`, `epochs`, `kan_grid_size`, and `kan_l2`.

### 5.2 Candidate Trace CSV
| Column | Type | Required | Description |
| --- | --- | --- | --- |
| dataset | string | Yes | Dataset family |
| censoring_rate | number | Yes | Censoring setting |
| seed | integer | Yes | Split seed |
| model | string | Yes | Model |
| search_method | enum | Yes | `random_search` or `ga_amfpo` |
| candidate_id | string | Yes | Candidate identifier |
| fidelity_level | enum | Yes | `fidelity_1`, `fidelity_2`, `fidelity_3` |
| promoted | boolean | Yes | Whether promoted to the next stage |
| validation_calibrated_monotone_ipcw_ibs | number | Yes | Validation score |
| runtime_sec | number | Yes | Runtime |
| config_hash | string | Yes | Hash of hyperparameters |

Final evidence should come from `fidelity_3`, and test metrics are report-only for selected full-fidelity configurations.

## 6. Metadata Fields
- `anchor_time`: time at which prediction is made
- `duration`: observed time-to-event or time-to-censoring
- `horizon_*`: prediction horizons
- `censoring_rate`: administrative censoring setting or scenario label
- `unit_id`: anonymized unit identifier used for splitting, not for model input

## 7. Data Types
- String: UTF-8 encoded identifiers such as `sample_id`, `dataset`, `unit_id`, `model`, and `config_hash`
- Number: integer or floating point values for durations, horizons, metrics, and rates
- Date/time: if used, ISO 8601 format
- Enum: `event`, `search_method`, `fidelity_level`, `status`, `selected_by_validation`
- Array: JSON array format for `horizon_grid`
- Object: JSON object format for `hyperparameters`, `validation_metric`, and `test_metric_reported_only`

## 8. Validation Rules
- Test cases: `case_id` must be unique, `duration` must be positive, `event` must be 0 or 1, `horizon_grid` must be non-empty and increasing, and `feature_summary` must be a string.
- Survival frame: `sample_id` must be unique, `duration > 0`, `event in {0,1}`, `censoring_rate in [0,1]`, `horizon_1 <= horizon_2 <= horizon_3 <= horizon_4`, and `missing_rate` and `padding_rate` must be in `[0,1]`.
- Audit tables: `status` must be `passed` or `failed`, `fallback` must be boolean-like, and `overlap_unit_count` must be `0` for passed split audits.
- Result tables: metric columns must be numeric, and `selected_by_validation` must be boolean-like.
- HPO: `config_hash`, `selected_by_validation`, `test_metric_reported_only`, and valid `fidelity_level` values must exist.
- Feature leakage: forbidden tokens must not appear in feature column names, including `failure_time`, `rul`, and `censor_time`.
- Label and metadata columns such as `sample_id`, `dataset`, `unit_id`, `anchor_time`, `duration`, `event`, `event_type`, and `censoring_rate` must not be used as predictive features.

## 9. Encoding and Special Characters
- All text files use UTF-8 encoding.
- CSV files use comma delimiters.
- JSON files use UTF-8 and pretty indentation.
- Entity identifiers use underscores rather than spaces.
- No local Windows paths should appear inside sample data files.
- No private identifiers should appear.

## 10. File Naming Conventions
- Test cases: `sample_survival_cases.json`
- Test case schema: `sample_survival_cases_schema.json`
- Survival frame sample: `survival_frame_sample.csv`
- Survival frame schema: `survival_frame_schema.json`
- Column dictionary: `survival_frame_column_dictionary.csv`
- Dataset audit: `dataset_audit_sample.csv`
- Feature leakage audit: `feature_leakage_audit_sample.csv`
- Split audit: `split_audit_sample.csv`
- Model result sample: `model_result_sample.csv`
- HPO selected config: `hpo_selected_config_sample.json`
- HPO candidate trace: `hpo_candidate_trace_sample.csv`
- Validation report: `VALIDATION_REPORT.md`

## 11. Version Information
- Current format version: 1.0
- Schema changes should increment the version number
- These files are illustrative samples, not full benchmark data
