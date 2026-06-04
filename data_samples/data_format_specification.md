# Data Format Specification

## Survival Test Case JSON

Fields:

- `case_id`
- `dataset`
- `unit_id`
- `anchor_time`
- `sequence_length`
- `horizon_grid`
- `duration`
- `event`
- `event_type`
- `censoring_type`
- `feature_summary`
- `expected_behavior`
- `notes`

Important warnings:

- Do not use `duration`, `event`, `event_type`, `unit_id`, `anchor_time`, `failure_time`, `rul`, or `censor_time` as predictive features.
- Label and metadata columns may exist in the frame, but validators must exclude them from model feature matrices.
- Test metrics must never be used for model selection.
- `event=1` means observed failure.
- `event=0` means right-censored.
- C-MAPSS administrative censoring is simulated or stress-test if used.

## Survival Frame CSV

Fields:

- `sample_id`
- `dataset`
- `unit_id`
- `anchor_time`
- `duration`
- `event`
- `event_type`
- `censoring_rate`
- `horizon_1`
- `horizon_2`
- `horizon_3`
- `horizon_4`
- `static_feature_1`
- `static_feature_2`
- `seq_feature_mean_1`
- `seq_feature_std_1`
- `seq_feature_last_1`
- `missing_rate`
- `padding_rate`

Important warnings:

- Do not use `duration`, `event`, `event_type`, `unit_id`, `anchor_time`, `failure_time`, `rul`, or `censor_time` as predictive features.
- Label and metadata columns may exist in the frame, but validators must exclude them from model feature matrices.
- Test metrics must never be used for model selection.
- `event=1` means observed failure.
- `event=0` means right-censored.
- C-MAPSS administrative censoring is simulated or stress-test if used.

## Audit CSV

Fields:

- `dataset`
- `censoring_rate`
- `samples`
- `units`
- `event_rate`
- `censoring_rate_observed`
- `duration_median`
- `padding_rate`
- `missing_rate`
- `fallback`
- `status`

Important warnings:

- Do not use `duration`, `event`, `event_type`, `unit_id`, `anchor_time`, `failure_time`, `rul`, or `censor_time` as predictive features.
- Label and metadata columns may exist in the frame, but validators must exclude them from model feature matrices.
- Test metrics must never be used for model selection.
- `event=1` means observed failure.
- `event=0` means right-censored.
- C-MAPSS administrative censoring is simulated or stress-test if used.

## Result CSV

Fields:

- `dataset`
- `censoring_rate`
- `seed`
- `model`
- `validation_calibrated_monotone_ipcw_ibs`
- `test_calibrated_monotone_ipcw_ibs`
- `c_index`
- `ece`
- `cost_top10`
- `riw`
- `runtime_sec`
- `selected_by_validation`

Important warnings:

- Do not use `duration`, `event`, `event_type`, `unit_id`, `anchor_time`, `failure_time`, `rul`, or `censor_time` as predictive features.
- Label and metadata columns may exist in the frame, but validators must exclude them from model feature matrices.
- Test metrics must never be used for model selection.
- `event=1` means observed failure.
- `event=0` means right-censored.
- C-MAPSS administrative censoring is simulated or stress-test if used.

## HPO Selected Config JSON

Fields:

- `dataset`
- `censoring_rate`
- `seed`
- `model`
- `search_method`
- `config_hash`
- `hyperparameters`
- `validation_metric`
- `test_metric_reported_only`
- `fidelity_level`
- `selected_by_validation`

Important warnings:

- Do not use `duration`, `event`, `event_type`, `unit_id`, `anchor_time`, `failure_time`, `rul`, or `censor_time` as predictive features.
- Label and metadata columns may exist in the frame, but validators must exclude them from model feature matrices.
- Test metrics must never be used for model selection.
- `event=1` means observed failure.
- `event=0` means right-censored.
- C-MAPSS administrative censoring is simulated or stress-test if used.

## HPO Candidate Trace CSV

Fields:

- `dataset`
- `censoring_rate`
- `seed`
- `model`
- `search_method`
- `candidate_id`
- `fidelity_level`
- `promoted`
- `validation_calibrated_monotone_ipcw_ibs`
- `runtime_sec`
- `config_hash`

Important warnings:

- Do not use `duration`, `event`, `event_type`, `unit_id`, `anchor_time`, `failure_time`, `rul`, or `censor_time` as predictive features.
- Label and metadata columns may exist in the frame, but validators must exclude them from model feature matrices.
- Test metrics must never be used for model selection.
- `event=1` means observed failure.
- `event=0` means right-censored.
- C-MAPSS administrative censoring is simulated or stress-test if used.
