from __future__ import annotations

import csv
import json
import os
from pathlib import Path
from textwrap import dedent


REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_SAMPLES_ROOT = REPO_ROOT / "data_samples"


def ensure_text_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    existing = path.read_text(encoding="utf-8") if path.exists() else None
    if existing != content:
        path.write_text(content, encoding="utf-8", newline="\n")


def write_json(path: Path, payload: object) -> None:
    ensure_text_file(path, json.dumps(payload, indent=2, ensure_ascii=False) + "\n")


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    buffer = []
    from io import StringIO

    sio = StringIO()
    writer = csv.DictWriter(sio, fieldnames=fieldnames, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    buffer.append(sio.getvalue())
    ensure_text_file(path, "".join(buffer))


ROOT_README = dedent(
    """
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
    """
).strip() + "\n"


ROOT_GITIGNORE = dedent(
    """
    __pycache__/
    .ipynb_checkpoints/
    .DS_Store
    Thumbs.db
    *.zip
    *.npz
    *.pt
    *.pth
    *.ckpt
    *.pkl
    *.joblib
    outputs/logs/
    outputs/checkpoints/
    data/raw/
    data/frames/
    """
).strip() + "\n"


DATA_SAMPLES_GITIGNORE = dedent(
    """
    __pycache__/
    .ipynb_checkpoints/
    .DS_Store
    Thumbs.db
    *.zip
    *.npz
    *.pt
    *.pth
    *.ckpt
    *.pkl
    *.joblib
    """
).strip() + "\n"


DATA_SAMPLES_README = dedent(
    """
    # OCEAN-MO-CDSF Dataset Samples

    ## Overview

    This folder contains sample data structures used by the OCEAN-MO-CDSF framework for censored predictive-maintenance survival analysis.

    The samples illustrate data schemas, censoring/event labels, survival frames, audit tables, model-result records, and HPO traces.

    These are small illustrative samples, not the full dataset.

    No raw industrial data, model weights, checkpoints, or private data are included.

    ## Dataset Components

    - Test Set Samples
    - Survival Frame Samples
    - Audit Samples
    - Result Samples
    - HPO Samples

    ## Directory Tree

    ```text
    data_samples/
    |-- README.md
    |-- data_format_specification.md
    |-- .gitignore
    |-- data/
        |-- test_set_samples/
        |   |-- README.md
        |   |-- sample_survival_cases.json
        |   `-- sample_survival_cases_schema.json
        |-- survival_frame_samples/
        |   |-- README.md
        |   |-- survival_frame_sample.csv
        |   |-- survival_frame_schema.json
        |   `-- survival_frame_column_dictionary.csv
        |-- audit_samples/
        |   |-- README.md
        |   |-- dataset_audit_sample.csv
        |   |-- feature_leakage_audit_sample.csv
        |   `-- split_audit_sample.csv
        |-- result_samples/
        |   |-- README.md
        |   `-- model_result_sample.csv
        `-- hpo_samples/
            |-- README.md
            |-- hpo_selected_config_sample.json
            `-- hpo_candidate_trace_sample.csv
    ```

    ## Test Set Samples

    ### Purpose
    Illustrative survival test cases showing observed failures, right-censoring, administrative censoring, padding, and missingness.

    ### Main Files
    - `data/test_set_samples/sample_survival_cases.json`
    - `data/test_set_samples/sample_survival_cases_schema.json`

    ### Format
    JSON array of compact case records with a companion JSON schema.

    ### Example Use
    Load a small set of survival cases for documentation, schema checks, and reader-facing examples.

    ## Survival Frame Samples

    ### Purpose
    Illustrative tabular survival frame records for censored predictive-maintenance modeling.

    ### Main Files
    - `data/survival_frame_samples/survival_frame_sample.csv`
    - `data/survival_frame_samples/survival_frame_schema.json`
    - `data/survival_frame_samples/survival_frame_column_dictionary.csv`

    ### Format
    CSV table with target, metadata, and feature columns plus a column dictionary.

    ### Example Use
    Load the survival frame into pandas, validate columns, and build feature matrices that exclude outcome and metadata fields.

    ## Audit Samples

    ### Purpose
    Compact dataset-audit, leakage-audit, and split-audit records for reproducibility and review.

    ### Main Files
    - `data/audit_samples/dataset_audit_sample.csv`
    - `data/audit_samples/feature_leakage_audit_sample.csv`
    - `data/audit_samples/split_audit_sample.csv`

    ### Format
    CSV audit tables with pass/fail style statuses and simple boolean-like fields.

    ### Example Use
    Load audits during documentation review to confirm censoring coverage, leakage checks, and unit-level splits.

    ## Result Samples

    ### Purpose
    Illustrative model-result records that separate validation selection from final test reporting.

    ### Main Files
    - `data/result_samples/model_result_sample.csv`

    ### Format
    CSV table with validation and test metrics, runtime, and selection flags.

    ### Example Use
    Load a result table to compare model families and trace which configuration was selected by validation.

    ## HPO Samples

    ### Purpose
    Illustrative hyperparameter-optimization traces and selected configurations.

    ### Main Files
    - `data/hpo_samples/hpo_selected_config_sample.json`
    - `data/hpo_samples/hpo_candidate_trace_sample.csv`

    ### Format
    JSON plus CSV showing selected configurations, multi-fidelity promotions, and candidate trace history.

    ### Example Use
    Load the selected config JSON, inspect the candidate trace, and explain how validation metrics drove the final choice.

    ## Usage Examples

    ```python
    import csv
    import json
    from pathlib import Path

    root = Path("data_samples/data")

    with open(root / "test_set_samples" / "sample_survival_cases.json", "r", encoding="utf-8") as f:
        cases = json.load(f)

    with open(root / "survival_frame_samples" / "survival_frame_sample.csv", "r", encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))

    with open(root / "audit_samples" / "dataset_audit_sample.csv", "r", encoding="utf-8", newline="") as f:
        audits = list(csv.DictReader(f))
    ```

    ```python
    import csv
    import json

    with open("data_samples/data/hpo_samples/hpo_selected_config_sample.json", "r", encoding="utf-8") as f:
        selected = json.load(f)

    with open("data_samples/data/hpo_samples/hpo_candidate_trace_sample.csv", "r", encoding="utf-8", newline="") as f:
        candidates = list(csv.DictReader(f))
    ```

    ## Notes

    - `event=1` means observed failure.
    - `event=0` means right-censored.
    - Test metrics are reported only after validation selection.
    - C-MAPSS administrative censoring is a stress-test setting if used.
    - SurvSHAP-style explanations, if used elsewhere in the paper, are model-behavior explanations, not causal claims.
    - These samples are for format demonstration only.

    ## Anonymization and Research Use

    All values in this folder are synthetic or anonymized and are intended for reproducibility, schema demonstration, and documentation. They are not a substitute for the full benchmark dataset or any proprietary industrial data.
    """
).strip() + "\n"


DATA_FORMAT_SPEC = dedent(
    """
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
    """
).strip() + "\n"


TEST_SET_README = dedent(
    """
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
    """
).strip() + "\n"


SURVIVAL_FRAME_README = dedent(
    """
    # Survival Frame Samples

    ## Purpose

    This folder contains compact survival-frame rows that demonstrate the tabular format used by OCEAN-MO-CDSF.

    ## File Descriptions

    - `survival_frame_sample.csv`: illustrative survival-frame records
    - `survival_frame_schema.json`: schema describing the CSV columns
    - `survival_frame_column_dictionary.csv`: column-level roles and usage flags

    ## Column-Role Explanation

    - Identifier and metadata fields describe the unit, anchor time, censoring setup, or sample identity.
    - Outcome fields describe the survival target and must not be used as predictive features.
    - Feature fields are the only columns intended for model inputs.
    - `missing_rate` and `padding_rate` are kept as metadata by default unless a specific experiment intentionally promotes them to features.

    ## Python Load Example

    ```python
    import csv

    with open("data_samples/data/survival_frame_samples/survival_frame_sample.csv", "r", encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    ```

    ## Warning

    Outcome and metadata columns must not be used as predictive features.
    """
).strip() + "\n"


AUDIT_README = dedent(
    """
    # Audit Samples

    ## Purpose

    These audit tables provide compact examples of dataset auditing, feature leakage review, and unit-level split checking.

    ## File Descriptions

    - `dataset_audit_sample.csv`: dataset-level quality and censoring summary
    - `feature_leakage_audit_sample.csv`: feature leakage review summary
    - `split_audit_sample.csv`: unit-level split integrity summary

    ## Audit Interpretation

    - `status` indicates pass or fail.
    - `fallback=false` means the sample is shown without synthetic fallback rows.
    - Feature leakage audits should confirm that outcome or metadata fields are not exposed as model features.
    - Split audits should show no overlap in units across training, calibration, validation, and test partitions.

    ## Python Load Example

    ```python
    import csv

    with open("data_samples/data/audit_samples/dataset_audit_sample.csv", "r", encoding="utf-8", newline="") as f:
        dataset_audit = list(csv.DictReader(f))
    ```
    """
).strip() + "\n"


RESULT_README = dedent(
    """
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
    """
).strip() + "\n"


HPO_README = dedent(
    """
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
    """
).strip() + "\n"


ROOT_README += dedent(
    """

    ## Processed Mini Samples and Quick View

    - `data/processed_mini_samples/` contains small anonymized subsets extracted from processed survival-frame `.npz` files.
    - `data/quick_view/` provides convenience copies for quick inspection.
    - The structured folders remain authoritative, and full raw datasets are not redistributed.
    """
).strip() + "\n"

DATA_SAMPLES_README += dedent(
    """

    ## Additional Components

    - `data/processed_mini_samples/` contains extracted processed mini survival frames.
    - `data/quick_view/` contains convenience copies for quick inspection.
    - These folders better reflect the real project structure where raw data live under `ocean_mo_cdsf/data/raw/` and processed frames live under `ocean_mo_cdsf/data/frames/`.
    """
).strip() + "\n"

DATA_FORMAT_SPEC += dedent(
    """

    ## 12. Processed Mini Survival Frame Format

    - Format: CSV
    - Encoding: UTF-8
    - These samples are small extracted subsets from processed survival-frame `.npz` artifacts.
    - `source_frame` stores the `.npz` file name only, not a local path.
    - Unit identifiers are anonymized.
    - The mini files are for schema inspection and validation only; they are not sufficient to reproduce benchmark-scale training or test metrics.
    """
).strip() + "\n"

PROCESSED_MINI_README = dedent(
    """
    # Processed Mini Samples

    These files are small extracted subsets from processed `.npz` survival frames generated by the OCEAN-MO-CDSF pipeline.
    They are not full raw datasets, and unit identifiers are anonymized.
    """
).strip() + "\n"

QUICK_VIEW_README = dedent(
    """
    # Quick View

    This folder provides direct access to key sample files for quick inspection.
    These are convenience copies; structured folders remain authoritative.
    """
).strip() + "\n"


TEST_CASES = {
    "generated_for": "OCEAN-MO-CDSF sample-data documentation",
    "cases": [
        {
            "case_id": "azure_recurrent_obs_01",
            "dataset": "azure",
            "unit_id": "AZ-1001",
            "anchor_time": "2026-05-01T08:00:00Z",
            "sequence_length": 72,
            "horizon_grid": [6, 12, 24, 48],
            "duration": 18.0,
            "event": 1,
            "event_type": "observed_failure",
            "censoring_type": "none",
            "feature_summary": "two static signals and a mild degradation trend in the sequence",
            "expected_behavior": "Near-term failure risk should be elevated and the observed event should occur before the longest horizon.",
            "notes": "Synthetic Azure-like recurrent failure episode for format demonstration only.",
        },
        {
            "case_id": "azure_final_censored_02",
            "dataset": "azure",
            "unit_id": "AZ-1002",
            "anchor_time": "2026-05-03T10:30:00Z",
            "sequence_length": 96,
            "horizon_grid": [6, 12, 24, 48],
            "duration": 30.0,
            "event": 0,
            "event_type": "right_censored",
            "censoring_type": "right_censoring",
            "feature_summary": "stable operating range with no observed failure before study end",
            "expected_behavior": "Model should treat this as a censored case and avoid interpreting the missing failure as a negative label.",
            "notes": "Synthetic Azure-like final censored episode.",
        },
        {
            "case_id": "cmapss_fd001_run_to_failure_03",
            "dataset": "cmapss_fd001",
            "unit_id": "FD001-003",
            "anchor_time": "2026-04-18T06:00:00Z",
            "sequence_length": 118,
            "horizon_grid": [5, 10, 20, 40],
            "duration": 21.0,
            "event": 1,
            "event_type": "observed_failure",
            "censoring_type": "none",
            "feature_summary": "single-regime sensor progression with a clear end-of-life pattern",
            "expected_behavior": "Run-to-failure trajectory should align with the end of the sequence and a positive event label.",
            "notes": "Synthetic C-MAPSS FD001 uncensored run-to-failure case.",
        },
        {
            "case_id": "cmapss_fd001_admin_censored_04",
            "dataset": "cmapss_fd001",
            "unit_id": "FD001-004",
            "anchor_time": "2026-04-20T06:00:00Z",
            "sequence_length": 112,
            "horizon_grid": [5, 10, 20, 40],
            "duration": 14.2,
            "event": 0,
            "event_type": "right_censored",
            "censoring_type": "administrative_censoring_0.3",
            "feature_summary": "healthy-looking segment truncated by administrative censoring",
            "expected_behavior": "This should behave as a stress-test example for censoring-aware survival modeling.",
            "notes": "Synthetic C-MAPSS FD001 administratively censored at 0.3.",
        },
        {
            "case_id": "cmapss_fd004_multiregime_05",
            "dataset": "cmapss_fd004",
            "unit_id": "FD004-005",
            "anchor_time": "2026-03-10T09:15:00Z",
            "sequence_length": 140,
            "horizon_grid": [8, 16, 24, 32],
            "duration": 26.0,
            "event": 1,
            "event_type": "observed_failure",
            "censoring_type": "none",
            "feature_summary": "multi-regime operating profile with a regime shift late in life",
            "expected_behavior": "The case should demonstrate a more complex sequence context while still ending in an observed failure.",
            "notes": "Synthetic C-MAPSS FD004 multi-regime uncensored case.",
        },
        {
            "case_id": "scania_high_censor_06",
            "dataset": "scania",
            "unit_id": "SC-2001",
            "anchor_time": "2026-05-10T07:45:00Z",
            "sequence_length": 64,
            "horizon_grid": [7, 14, 28, 56],
            "duration": 19.5,
            "event": 0,
            "event_type": "right_censored",
            "censoring_type": "high_censoring",
            "feature_summary": "mostly stable telemetry with sparse warning-like fluctuations",
            "expected_behavior": "High censoring should be reflected in conservative survival estimates and careful calibration.",
            "notes": "Synthetic Scania high-censoring case.",
        },
        {
            "case_id": "short_padded_sequence_07",
            "dataset": "azure",
            "unit_id": "AZ-1007",
            "anchor_time": "2026-05-15T12:00:00Z",
            "sequence_length": 8,
            "horizon_grid": [4, 8, 16, 32],
            "duration": 8.0,
            "event": 0,
            "event_type": "right_censored",
            "censoring_type": "padded_short_sequence",
            "feature_summary": "short observation window with explicit left-padding and few real timesteps",
            "expected_behavior": "Padding-aware preprocessing should preserve the short sequence without leaking padding into the feature set.",
            "notes": "Synthetic short sequence with padding.",
        },
        {
            "case_id": "missing_sensor_values_08",
            "dataset": "scania",
            "unit_id": "SC-2008",
            "anchor_time": "2026-05-18T11:20:00Z",
            "sequence_length": 88,
            "horizon_grid": [6, 12, 24, 48],
            "duration": 23.0,
            "event": 1,
            "event_type": "observed_failure",
            "censoring_type": "none",
            "feature_summary": "sensor series includes scattered missing values and imputation markers",
            "expected_behavior": "Missingness should be handled as metadata or preprocessing input, not as a proxy label.",
            "notes": "Synthetic missing sensor values case.",
        },
    ],
}


TEST_CASE_SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "Sample Survival Cases Schema",
    "type": "object",
    "required": ["generated_for", "cases"],
    "properties": {
        "generated_for": {"type": "string"},
        "cases": {
            "type": "array",
            "minItems": 8,
            "items": {
                "type": "object",
                "required": [
                    "case_id",
                    "dataset",
                    "unit_id",
                    "anchor_time",
                    "sequence_length",
                    "horizon_grid",
                    "duration",
                    "event",
                    "event_type",
                    "censoring_type",
                    "feature_summary",
                    "expected_behavior",
                    "notes",
                ],
                "properties": {
                    "case_id": {"type": "string"},
                    "dataset": {"type": "string"},
                    "unit_id": {"type": "string"},
                    "anchor_time": {"type": "string"},
                    "sequence_length": {"type": "integer", "minimum": 1},
                    "horizon_grid": {
                        "type": "array",
                        "minItems": 1,
                        "items": {"type": "integer", "minimum": 1},
                    },
                    "duration": {"type": "number", "exclusiveMinimum": 0},
                    "event": {"type": "integer", "enum": [0, 1]},
                    "event_type": {"type": "string"},
                    "censoring_type": {"type": "string"},
                    "feature_summary": {"type": "string"},
                    "expected_behavior": {"type": "string"},
                    "notes": {"type": "string"},
                },
            },
        },
    },
}


SURVIVAL_FRAME_ROWS = [
    {"sample_id": "s001", "dataset": "azure", "unit_id": "AZ-1001", "anchor_time": "2026-05-01T08:00:00Z", "duration": 14.5, "event": 1, "event_type": "observed_failure", "censoring_rate": 0.0, "horizon_1": 3, "horizon_2": 6, "horizon_3": 9, "horizon_4": 12, "static_feature_1": 0.82, "static_feature_2": 0.41, "seq_feature_mean_1": 0.28, "seq_feature_std_1": 0.05, "seq_feature_last_1": 0.31, "missing_rate": 0.00, "padding_rate": 0.00},
    {"sample_id": "s002", "dataset": "azure", "unit_id": "AZ-1002", "anchor_time": "2026-05-03T10:30:00Z", "duration": 18.0, "event": 0, "event_type": "right_censored", "censoring_rate": 0.3, "horizon_1": 4, "horizon_2": 8, "horizon_3": 12, "horizon_4": 16, "static_feature_1": 0.77, "static_feature_2": 0.36, "seq_feature_mean_1": 0.25, "seq_feature_std_1": 0.07, "seq_feature_last_1": 0.20, "missing_rate": 0.02, "padding_rate": 0.00},
    {"sample_id": "s003", "dataset": "azure", "unit_id": "AZ-1003", "anchor_time": "2026-05-04T11:15:00Z", "duration": 12.0, "event": 1, "event_type": "observed_failure", "censoring_rate": 0.3, "horizon_1": 2, "horizon_2": 4, "horizon_3": 8, "horizon_4": 12, "static_feature_1": 0.69, "static_feature_2": 0.44, "seq_feature_mean_1": 0.34, "seq_feature_std_1": 0.08, "seq_feature_last_1": 0.39, "missing_rate": 0.01, "padding_rate": 0.00},
    {"sample_id": "s004", "dataset": "azure", "unit_id": "AZ-1004", "anchor_time": "2026-05-05T09:00:00Z", "duration": 9.5, "event": 0, "event_type": "right_censored", "censoring_rate": 0.0, "horizon_1": 1, "horizon_2": 2, "horizon_3": 4, "horizon_4": 8, "static_feature_1": 0.61, "static_feature_2": 0.33, "seq_feature_mean_1": 0.21, "seq_feature_std_1": 0.04, "seq_feature_last_1": 0.18, "missing_rate": 0.00, "padding_rate": 0.10},
    {"sample_id": "s005", "dataset": "azure", "unit_id": "AZ-1005", "anchor_time": "2026-05-06T14:30:00Z", "duration": 22.2, "event": 1, "event_type": "observed_failure", "censoring_rate": 0.0, "horizon_1": 5, "horizon_2": 10, "horizon_3": 15, "horizon_4": 20, "static_feature_1": 0.88, "static_feature_2": 0.52, "seq_feature_mean_1": 0.47, "seq_feature_std_1": 0.09, "seq_feature_last_1": 0.51, "missing_rate": 0.03, "padding_rate": 0.00},
    {"sample_id": "s006", "dataset": "scania", "unit_id": "SC-2001", "anchor_time": "2026-05-10T07:45:00Z", "duration": 19.5, "event": 0, "event_type": "right_censored", "censoring_rate": 0.3, "horizon_1": 4, "horizon_2": 8, "horizon_3": 16, "horizon_4": 32, "static_feature_1": 0.57, "static_feature_2": 0.49, "seq_feature_mean_1": 0.19, "seq_feature_std_1": 0.05, "seq_feature_last_1": 0.17, "missing_rate": 0.04, "padding_rate": 0.00},
    {"sample_id": "s007", "dataset": "scania", "unit_id": "SC-2002", "anchor_time": "2026-05-11T08:20:00Z", "duration": 16.0, "event": 1, "event_type": "observed_failure", "censoring_rate": 0.3, "horizon_1": 3, "horizon_2": 6, "horizon_3": 12, "horizon_4": 24, "static_feature_1": 0.64, "static_feature_2": 0.45, "seq_feature_mean_1": 0.31, "seq_feature_std_1": 0.06, "seq_feature_last_1": 0.36, "missing_rate": 0.05, "padding_rate": 0.00},
    {"sample_id": "s008", "dataset": "scania", "unit_id": "SC-2003", "anchor_time": "2026-05-12T09:10:00Z", "duration": 25.0, "event": 0, "event_type": "right_censored", "censoring_rate": 0.3, "horizon_1": 5, "horizon_2": 10, "horizon_3": 20, "horizon_4": 40, "static_feature_1": 0.52, "static_feature_2": 0.39, "seq_feature_mean_1": 0.22, "seq_feature_std_1": 0.03, "seq_feature_last_1": 0.20, "missing_rate": 0.02, "padding_rate": 0.00},
    {"sample_id": "s009", "dataset": "scania", "unit_id": "SC-2004", "anchor_time": "2026-05-13T10:05:00Z", "duration": 13.2, "event": 1, "event_type": "observed_failure", "censoring_rate": 0.0, "horizon_1": 2, "horizon_2": 4, "horizon_3": 8, "horizon_4": 16, "static_feature_1": 0.71, "static_feature_2": 0.48, "seq_feature_mean_1": 0.29, "seq_feature_std_1": 0.07, "seq_feature_last_1": 0.35, "missing_rate": 0.00, "padding_rate": 0.00},
    {"sample_id": "s010", "dataset": "scania", "unit_id": "SC-2005", "anchor_time": "2026-05-14T12:40:00Z", "duration": 20.8, "event": 0, "event_type": "right_censored", "censoring_rate": 0.3, "horizon_1": 4, "horizon_2": 8, "horizon_3": 12, "horizon_4": 24, "static_feature_1": 0.54, "static_feature_2": 0.42, "seq_feature_mean_1": 0.24, "seq_feature_std_1": 0.04, "seq_feature_last_1": 0.22, "missing_rate": 0.07, "padding_rate": 0.02},
    {"sample_id": "s011", "dataset": "cmapss_fd001", "unit_id": "FD001-001", "anchor_time": "2026-04-18T06:00:00Z", "duration": 21.0, "event": 1, "event_type": "observed_failure", "censoring_rate": 0.0, "horizon_1": 5, "horizon_2": 10, "horizon_3": 20, "horizon_4": 40, "static_feature_1": 0.83, "static_feature_2": 0.56, "seq_feature_mean_1": 0.46, "seq_feature_std_1": 0.08, "seq_feature_last_1": 0.52, "missing_rate": 0.01, "padding_rate": 0.00},
    {"sample_id": "s012", "dataset": "cmapss_fd001", "unit_id": "FD001-002", "anchor_time": "2026-04-19T06:00:00Z", "duration": 14.2, "event": 0, "event_type": "right_censored", "censoring_rate": 0.3, "horizon_1": 3, "horizon_2": 6, "horizon_3": 12, "horizon_4": 24, "static_feature_1": 0.67, "static_feature_2": 0.43, "seq_feature_mean_1": 0.25, "seq_feature_std_1": 0.06, "seq_feature_last_1": 0.23, "missing_rate": 0.00, "padding_rate": 0.00},
    {"sample_id": "s013", "dataset": "cmapss_fd001", "unit_id": "FD001-003", "anchor_time": "2026-04-20T06:00:00Z", "duration": 19.0, "event": 1, "event_type": "observed_failure", "censoring_rate": 0.0, "horizon_1": 4, "horizon_2": 8, "horizon_3": 16, "horizon_4": 32, "static_feature_1": 0.79, "static_feature_2": 0.51, "seq_feature_mean_1": 0.37, "seq_feature_std_1": 0.05, "seq_feature_last_1": 0.42, "missing_rate": 0.02, "padding_rate": 0.00},
    {"sample_id": "s014", "dataset": "cmapss_fd001", "unit_id": "FD001-004", "anchor_time": "2026-04-21T06:00:00Z", "duration": 11.8, "event": 0, "event_type": "right_censored", "censoring_rate": 0.3, "horizon_1": 2, "horizon_2": 4, "horizon_3": 8, "horizon_4": 16, "static_feature_1": 0.63, "static_feature_2": 0.41, "seq_feature_mean_1": 0.21, "seq_feature_std_1": 0.03, "seq_feature_last_1": 0.19, "missing_rate": 0.04, "padding_rate": 0.00},
    {"sample_id": "s015", "dataset": "cmapss_fd001", "unit_id": "FD001-005", "anchor_time": "2026-04-22T06:00:00Z", "duration": 24.5, "event": 1, "event_type": "observed_failure", "censoring_rate": 0.0, "horizon_1": 6, "horizon_2": 12, "horizon_3": 18, "horizon_4": 24, "static_feature_1": 0.87, "static_feature_2": 0.59, "seq_feature_mean_1": 0.49, "seq_feature_std_1": 0.09, "seq_feature_last_1": 0.55, "missing_rate": 0.00, "padding_rate": 0.00},
    {"sample_id": "s016", "dataset": "cmapss_fd004", "unit_id": "FD004-001", "anchor_time": "2026-03-10T09:15:00Z", "duration": 26.0, "event": 1, "event_type": "observed_failure", "censoring_rate": 0.0, "horizon_1": 8, "horizon_2": 16, "horizon_3": 24, "horizon_4": 32, "static_feature_1": 0.81, "static_feature_2": 0.62, "seq_feature_mean_1": 0.53, "seq_feature_std_1": 0.10, "seq_feature_last_1": 0.60, "missing_rate": 0.03, "padding_rate": 0.00},
    {"sample_id": "s017", "dataset": "cmapss_fd004", "unit_id": "FD004-002", "anchor_time": "2026-03-11T09:15:00Z", "duration": 17.8, "event": 0, "event_type": "right_censored", "censoring_rate": 0.3, "horizon_1": 4, "horizon_2": 8, "horizon_3": 16, "horizon_4": 24, "static_feature_1": 0.58, "static_feature_2": 0.47, "seq_feature_mean_1": 0.27, "seq_feature_std_1": 0.05, "seq_feature_last_1": 0.24, "missing_rate": 0.06, "padding_rate": 0.01},
    {"sample_id": "s018", "dataset": "cmapss_fd004", "unit_id": "FD004-003", "anchor_time": "2026-03-12T09:15:00Z", "duration": 22.0, "event": 1, "event_type": "observed_failure", "censoring_rate": 0.0, "horizon_1": 5, "horizon_2": 10, "horizon_3": 15, "horizon_4": 25, "static_feature_1": 0.72, "static_feature_2": 0.53, "seq_feature_mean_1": 0.38, "seq_feature_std_1": 0.06, "seq_feature_last_1": 0.44, "missing_rate": 0.01, "padding_rate": 0.00},
    {"sample_id": "s019", "dataset": "cmapss_fd004", "unit_id": "FD004-004", "anchor_time": "2026-03-13T09:15:00Z", "duration": 13.6, "event": 0, "event_type": "right_censored", "censoring_rate": 0.3, "horizon_1": 3, "horizon_2": 6, "horizon_3": 12, "horizon_4": 24, "static_feature_1": 0.62, "static_feature_2": 0.46, "seq_feature_mean_1": 0.23, "seq_feature_std_1": 0.04, "seq_feature_last_1": 0.21, "missing_rate": 0.05, "padding_rate": 0.02},
    {"sample_id": "s020", "dataset": "cmapss_fd004", "unit_id": "FD004-005", "anchor_time": "2026-03-14T09:15:00Z", "duration": 28.4, "event": 1, "event_type": "observed_failure", "censoring_rate": 0.0, "horizon_1": 7, "horizon_2": 14, "horizon_3": 21, "horizon_4": 28, "static_feature_1": 0.85, "static_feature_2": 0.57, "seq_feature_mean_1": 0.51, "seq_feature_std_1": 0.08, "seq_feature_last_1": 0.58, "missing_rate": 0.00, "padding_rate": 0.00},
]


SURVIVAL_FRAME_SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "Survival Frame Sample Schema",
    "type": "object",
    "required": ["columns", "validation_rules"],
    "properties": {
        "columns": {
            "type": "array",
            "items": {"type": "string"},
        },
        "validation_rules": {
            "type": "array",
            "items": {"type": "string"},
        },
    },
}


SURVIVAL_FRAME_COLUMN_DICTIONARY_ROWS = [
    {"column_name": "sample_id", "role": "identifier", "dtype": "string", "allowed_values": "unique sample identifier", "description": "Synthetic sample identifier.", "used_as_feature": "false"},
    {"column_name": "dataset", "role": "metadata", "dtype": "string", "allowed_values": "azure|scania|cmapss_fd001|cmapss_fd004", "description": "Dataset family label.", "used_as_feature": "false"},
    {"column_name": "unit_id", "role": "identifier", "dtype": "string", "allowed_values": "unit identifier", "description": "Unit or machine identifier.", "used_as_feature": "false"},
    {"column_name": "anchor_time", "role": "metadata", "dtype": "string", "allowed_values": "ISO 8601 timestamp", "description": "Anchor timestamp for the observation window.", "used_as_feature": "false"},
    {"column_name": "duration", "role": "target", "dtype": "number", "allowed_values": "> 0", "description": "Observed or censored time-to-event duration.", "used_as_feature": "false"},
    {"column_name": "event", "role": "target", "dtype": "integer", "allowed_values": "0|1", "description": "Event indicator, where 1 means observed failure and 0 means right-censored.", "used_as_feature": "false"},
    {"column_name": "event_type", "role": "metadata", "dtype": "string", "allowed_values": "observed_failure|right_censored", "description": "Human-readable event category; do not use as a predictive feature.", "used_as_feature": "false"},
    {"column_name": "censoring_rate", "role": "metadata", "dtype": "number", "allowed_values": "0..1", "description": "Scenario-level censoring rate for the sample row.", "used_as_feature": "false"},
    {"column_name": "horizon_1", "role": "metadata", "dtype": "integer", "allowed_values": "positive integer", "description": "First prediction horizon for the sample.", "used_as_feature": "false"},
    {"column_name": "horizon_2", "role": "metadata", "dtype": "integer", "allowed_values": "positive integer", "description": "Second prediction horizon for the sample.", "used_as_feature": "false"},
    {"column_name": "horizon_3", "role": "metadata", "dtype": "integer", "allowed_values": "positive integer", "description": "Third prediction horizon for the sample.", "used_as_feature": "false"},
    {"column_name": "horizon_4", "role": "metadata", "dtype": "integer", "allowed_values": "positive integer", "description": "Fourth prediction horizon for the sample.", "used_as_feature": "false"},
    {"column_name": "static_feature_1", "role": "feature", "dtype": "number", "allowed_values": "synthetic numeric feature", "description": "Illustrative static feature used in model inputs.", "used_as_feature": "true"},
    {"column_name": "static_feature_2", "role": "feature", "dtype": "number", "allowed_values": "synthetic numeric feature", "description": "Illustrative static feature used in model inputs.", "used_as_feature": "true"},
    {"column_name": "seq_feature_mean_1", "role": "feature", "dtype": "number", "allowed_values": "synthetic numeric feature", "description": "Illustrative sequential summary feature used in model inputs.", "used_as_feature": "true"},
    {"column_name": "seq_feature_std_1", "role": "feature", "dtype": "number", "allowed_values": "synthetic numeric feature", "description": "Illustrative sequential variability feature used in model inputs.", "used_as_feature": "true"},
    {"column_name": "seq_feature_last_1", "role": "feature", "dtype": "number", "allowed_values": "synthetic numeric feature", "description": "Illustrative last-observation sequential feature used in model inputs.", "used_as_feature": "true"},
    {"column_name": "missing_rate", "role": "metadata", "dtype": "number", "allowed_values": "0..1", "description": "Observed missingness proportion; metadata by default unless explicitly modeled.", "used_as_feature": "false"},
    {"column_name": "padding_rate", "role": "metadata", "dtype": "number", "allowed_values": "0..1", "description": "Padding proportion for sequence alignment; metadata by default unless explicitly modeled.", "used_as_feature": "false"},
]


DATASET_AUDIT_ROWS = [
    {"dataset": "azure", "censoring_rate": 0.0, "samples": 120, "units": 14, "event_rate": 0.42, "censoring_rate_observed": 0.08, "duration_median": 18.4, "padding_rate": 0.01, "missing_rate": 0.02, "fallback": "false", "status": "pass"},
    {"dataset": "scania", "censoring_rate": 0.0, "samples": 160, "units": 20, "event_rate": 0.31, "censoring_rate_observed": 0.11, "duration_median": 21.7, "padding_rate": 0.02, "missing_rate": 0.03, "fallback": "false", "status": "pass"},
    {"dataset": "cmapss_fd001", "censoring_rate": 0.0, "samples": 100, "units": 10, "event_rate": 0.55, "censoring_rate_observed": 0.00, "duration_median": 16.2, "padding_rate": 0.00, "missing_rate": 0.01, "fallback": "false", "status": "pass"},
    {"dataset": "cmapss_fd001", "censoring_rate": 0.3, "samples": 100, "units": 10, "event_rate": 0.37, "censoring_rate_observed": 0.28, "duration_median": 14.8, "padding_rate": 0.01, "missing_rate": 0.01, "fallback": "false", "status": "pass"},
    {"dataset": "cmapss_fd004", "censoring_rate": 0.0, "samples": 100, "units": 10, "event_rate": 0.51, "censoring_rate_observed": 0.00, "duration_median": 20.1, "padding_rate": 0.00, "missing_rate": 0.02, "fallback": "false", "status": "pass"},
    {"dataset": "cmapss_fd004", "censoring_rate": 0.3, "samples": 100, "units": 10, "event_rate": 0.33, "censoring_rate_observed": 0.29, "duration_median": 17.6, "padding_rate": 0.02, "missing_rate": 0.02, "fallback": "false", "status": "pass"},
]


FEATURE_LEAKAGE_AUDIT_ROWS = [
    {"dataset": "azure", "censoring_rate": 0.0, "seq_feature_count": 3, "static_feature_count": 2, "bad_seq_features": "none", "bad_static_features": "none", "status": "pass"},
    {"dataset": "scania", "censoring_rate": 0.0, "seq_feature_count": 3, "static_feature_count": 2, "bad_seq_features": "none", "bad_static_features": "none", "status": "pass"},
    {"dataset": "cmapss_fd001", "censoring_rate": 0.0, "seq_feature_count": 3, "static_feature_count": 2, "bad_seq_features": "none", "bad_static_features": "none", "status": "pass"},
    {"dataset": "cmapss_fd001", "censoring_rate": 0.3, "seq_feature_count": 3, "static_feature_count": 2, "bad_seq_features": "none", "bad_static_features": "none", "status": "pass"},
    {"dataset": "cmapss_fd004", "censoring_rate": 0.0, "seq_feature_count": 3, "static_feature_count": 2, "bad_seq_features": "none", "bad_static_features": "none", "status": "pass"},
    {"dataset": "cmapss_fd004", "censoring_rate": 0.3, "seq_feature_count": 3, "static_feature_count": 2, "bad_seq_features": "none", "bad_static_features": "none", "status": "pass"},
]


SPLIT_AUDIT_ROWS = [
    {"dataset": "azure", "censoring_rate": 0.0, "seed": 0, "train_units": 8, "calibration_units": 2, "validation_units": 2, "test_units": 2, "overlap_unit_count": 0, "status": "pass"},
    {"dataset": "scania", "censoring_rate": 0.0, "seed": 0, "train_units": 12, "calibration_units": 3, "validation_units": 3, "test_units": 2, "overlap_unit_count": 0, "status": "pass"},
    {"dataset": "cmapss_fd001", "censoring_rate": 0.0, "seed": 0, "train_units": 6, "calibration_units": 1, "validation_units": 1, "test_units": 2, "overlap_unit_count": 0, "status": "pass"},
    {"dataset": "cmapss_fd001", "censoring_rate": 0.3, "seed": 0, "train_units": 6, "calibration_units": 1, "validation_units": 1, "test_units": 2, "overlap_unit_count": 0, "status": "pass"},
    {"dataset": "cmapss_fd004", "censoring_rate": 0.0, "seed": 0, "train_units": 6, "calibration_units": 1, "validation_units": 1, "test_units": 2, "overlap_unit_count": 0, "status": "pass"},
    {"dataset": "cmapss_fd004", "censoring_rate": 0.3, "seed": 0, "train_units": 6, "calibration_units": 1, "validation_units": 1, "test_units": 2, "overlap_unit_count": 0, "status": "pass"},
]


MODEL_RESULTS_ROWS = [
    {"dataset": "azure", "censoring_rate": 0.0, "seed": 0, "model": "coxph", "validation_calibrated_monotone_ipcw_ibs": 0.214, "test_calibrated_monotone_ipcw_ibs": 0.221, "c_index": 0.71, "ece": 0.08, "cost_top10": 0.19, "riw": 0.63, "runtime_sec": 2.4, "selected_by_validation": "false"},
    {"dataset": "azure", "censoring_rate": 0.0, "seed": 0, "model": "rsf", "validation_calibrated_monotone_ipcw_ibs": 0.198, "test_calibrated_monotone_ipcw_ibs": 0.205, "c_index": 0.73, "ece": 0.07, "cost_top10": 0.17, "riw": 0.66, "runtime_sec": 4.8, "selected_by_validation": "false"},
    {"dataset": "azure", "censoring_rate": 0.0, "seed": 0, "model": "coxkan", "validation_calibrated_monotone_ipcw_ibs": 0.186, "test_calibrated_monotone_ipcw_ibs": 0.193, "c_index": 0.75, "ece": 0.06, "cost_top10": 0.16, "riw": 0.69, "runtime_sec": 6.2, "selected_by_validation": "false"},
    {"dataset": "azure", "censoring_rate": 0.0, "seed": 0, "model": "deephit_mlp", "validation_calibrated_monotone_ipcw_ibs": 0.181, "test_calibrated_monotone_ipcw_ibs": 0.188, "c_index": 0.76, "ece": 0.06, "cost_top10": 0.15, "riw": 0.71, "runtime_sec": 8.5, "selected_by_validation": "false"},
    {"dataset": "azure", "censoring_rate": 0.0, "seed": 0, "model": "dynamic_deephit_gru", "validation_calibrated_monotone_ipcw_ibs": 0.172, "test_calibrated_monotone_ipcw_ibs": 0.179, "c_index": 0.77, "ece": 0.05, "cost_top10": 0.14, "riw": 0.74, "runtime_sec": 10.8, "selected_by_validation": "false"},
    {"dataset": "azure", "censoring_rate": 0.0, "seed": 0, "model": "dynamic_deephit_transformer", "validation_calibrated_monotone_ipcw_ibs": 0.166, "test_calibrated_monotone_ipcw_ibs": 0.173, "c_index": 0.78, "ece": 0.05, "cost_top10": 0.13, "riw": 0.76, "runtime_sec": 12.4, "selected_by_validation": "false"},
    {"dataset": "azure", "censoring_rate": 0.0, "seed": 0, "model": "ocean_gru_kan", "validation_calibrated_monotone_ipcw_ibs": 0.154, "test_calibrated_monotone_ipcw_ibs": 0.161, "c_index": 0.80, "ece": 0.04, "cost_top10": 0.11, "riw": 0.80, "runtime_sec": 13.2, "selected_by_validation": "false"},
    {"dataset": "azure", "censoring_rate": 0.0, "seed": 0, "model": "ocean_mamba_kan", "validation_calibrated_monotone_ipcw_ibs": 0.149, "test_calibrated_monotone_ipcw_ibs": 0.157, "c_index": 0.81, "ece": 0.04, "cost_top10": 0.10, "riw": 0.82, "runtime_sec": 14.0, "selected_by_validation": "false"},
    {"dataset": "azure", "censoring_rate": 0.0, "seed": 0, "model": "ocean_transformer_kan", "validation_calibrated_monotone_ipcw_ibs": 0.143, "test_calibrated_monotone_ipcw_ibs": 0.150, "c_index": 0.83, "ece": 0.03, "cost_top10": 0.09, "riw": 0.85, "runtime_sec": 15.1, "selected_by_validation": "true"},
    {"dataset": "cmapss_fd004", "censoring_rate": 0.3, "seed": 0, "model": "coxph", "validation_calibrated_monotone_ipcw_ibs": 0.244, "test_calibrated_monotone_ipcw_ibs": 0.251, "c_index": 0.68, "ece": 0.10, "cost_top10": 0.23, "riw": 0.58, "runtime_sec": 2.9, "selected_by_validation": "false"},
    {"dataset": "cmapss_fd004", "censoring_rate": 0.3, "seed": 0, "model": "rsf", "validation_calibrated_monotone_ipcw_ibs": 0.229, "test_calibrated_monotone_ipcw_ibs": 0.236, "c_index": 0.70, "ece": 0.09, "cost_top10": 0.21, "riw": 0.61, "runtime_sec": 5.3, "selected_by_validation": "false"},
    {"dataset": "cmapss_fd004", "censoring_rate": 0.3, "seed": 0, "model": "coxkan", "validation_calibrated_monotone_ipcw_ibs": 0.218, "test_calibrated_monotone_ipcw_ibs": 0.225, "c_index": 0.72, "ece": 0.08, "cost_top10": 0.20, "riw": 0.64, "runtime_sec": 6.8, "selected_by_validation": "false"},
    {"dataset": "cmapss_fd004", "censoring_rate": 0.3, "seed": 0, "model": "deephit_mlp", "validation_calibrated_monotone_ipcw_ibs": 0.213, "test_calibrated_monotone_ipcw_ibs": 0.220, "c_index": 0.73, "ece": 0.08, "cost_top10": 0.19, "riw": 0.66, "runtime_sec": 9.0, "selected_by_validation": "false"},
    {"dataset": "cmapss_fd004", "censoring_rate": 0.3, "seed": 0, "model": "dynamic_deephit_gru", "validation_calibrated_monotone_ipcw_ibs": 0.205, "test_calibrated_monotone_ipcw_ibs": 0.212, "c_index": 0.75, "ece": 0.07, "cost_top10": 0.18, "riw": 0.69, "runtime_sec": 11.1, "selected_by_validation": "false"},
    {"dataset": "cmapss_fd004", "censoring_rate": 0.3, "seed": 0, "model": "dynamic_deephit_transformer", "validation_calibrated_monotone_ipcw_ibs": 0.198, "test_calibrated_monotone_ipcw_ibs": 0.205, "c_index": 0.76, "ece": 0.07, "cost_top10": 0.17, "riw": 0.71, "runtime_sec": 12.9, "selected_by_validation": "false"},
    {"dataset": "cmapss_fd004", "censoring_rate": 0.3, "seed": 0, "model": "ocean_gru_kan", "validation_calibrated_monotone_ipcw_ibs": 0.187, "test_calibrated_monotone_ipcw_ibs": 0.193, "c_index": 0.79, "ece": 0.06, "cost_top10": 0.15, "riw": 0.76, "runtime_sec": 13.5, "selected_by_validation": "false"},
    {"dataset": "cmapss_fd004", "censoring_rate": 0.3, "seed": 0, "model": "ocean_mamba_kan", "validation_calibrated_monotone_ipcw_ibs": 0.179, "test_calibrated_monotone_ipcw_ibs": 0.186, "c_index": 0.80, "ece": 0.05, "cost_top10": 0.14, "riw": 0.79, "runtime_sec": 14.3, "selected_by_validation": "true"},
    {"dataset": "cmapss_fd004", "censoring_rate": 0.3, "seed": 0, "model": "ocean_transformer_kan", "validation_calibrated_monotone_ipcw_ibs": 0.181, "test_calibrated_monotone_ipcw_ibs": 0.188, "c_index": 0.81, "ece": 0.05, "cost_top10": 0.13, "riw": 0.81, "runtime_sec": 15.6, "selected_by_validation": "false"},
]


HPO_SELECTED_CONFIG = {
    "selected_configs": [
        {
            "dataset": "azure",
            "censoring_rate": 0.0,
            "seed": 0,
            "model": "ocean_gru_kan",
            "search_method": "random_search",
            "config_hash": "ogk-0a31f7c1",
            "fidelity_level": "fidelity_3",
            "hyperparameters": {
                "hidden_dim": 48,
                "num_layers": 2,
                "dropout": 0.15,
                "learning_rate": 0.0007,
                "batch_size": 128,
                "epochs": 24,
                "kan_grid_size": 8,
                "kan_l2": 0.0001,
            },
            "validation_metric": {
                "name": "validation_calibrated_monotone_ipcw_ibs",
                "value": 0.154,
            },
            "test_metric_reported_only": {
                "name": "test_calibrated_monotone_ipcw_ibs",
                "value": 0.161,
            },
            "selected_by_validation": True,
        },
        {
            "dataset": "cmapss_fd004",
            "censoring_rate": 0.3,
            "seed": 0,
            "model": "ocean_mamba_kan",
            "search_method": "ga_amfpo",
            "config_hash": "omk-9c44d2ab",
            "fidelity_level": "fidelity_3",
            "hyperparameters": {
                "hidden_dim": 64,
                "num_layers": 3,
                "dropout": 0.18,
                "learning_rate": 0.0005,
                "batch_size": 256,
                "epochs": 24,
                "kan_grid_size": 10,
                "kan_l2": 0.0002,
            },
            "validation_metric": {
                "name": "validation_calibrated_monotone_ipcw_ibs",
                "value": 0.179,
            },
            "test_metric_reported_only": {
                "name": "test_calibrated_monotone_ipcw_ibs",
                "value": 0.186,
            },
            "selected_by_validation": True,
        },
        {
            "dataset": "scania",
            "censoring_rate": 0.0,
            "seed": 0,
            "model": "ocean_transformer_kan",
            "search_method": "ga_amfpo",
            "config_hash": "otk-3e77b5af",
            "fidelity_level": "fidelity_3",
            "hyperparameters": {
                "hidden_dim": 56,
                "num_layers": 2,
                "dropout": 0.12,
                "learning_rate": 0.0006,
                "batch_size": 128,
                "epochs": 24,
                "kan_grid_size": 12,
                "kan_l2": 0.00015,
            },
            "validation_metric": {
                "name": "validation_calibrated_monotone_ipcw_ibs",
                "value": 0.166,
            },
            "test_metric_reported_only": {
                "name": "test_calibrated_monotone_ipcw_ibs",
                "value": 0.173,
            },
            "selected_by_validation": True,
        },
    ]
}


HPO_CANDIDATE_TRACE_ROWS = [
    {"dataset": "azure", "censoring_rate": 0.0, "seed": 0, "model": "ocean_gru_kan", "search_method": "random_search", "candidate_id": "rs-001", "fidelity_level": "fidelity_1", "promoted": "true", "validation_calibrated_monotone_ipcw_ibs": 0.218, "runtime_sec": 1.2, "config_hash": "ogk-0a31f7c1"},
    {"dataset": "azure", "censoring_rate": 0.0, "seed": 0, "model": "ocean_gru_kan", "search_method": "random_search", "candidate_id": "rs-002", "fidelity_level": "fidelity_2", "promoted": "true", "validation_calibrated_monotone_ipcw_ibs": 0.182, "runtime_sec": 2.4, "config_hash": "ogk-1f2b3c4d"},
    {"dataset": "azure", "censoring_rate": 0.0, "seed": 0, "model": "ocean_gru_kan", "search_method": "random_search", "candidate_id": "rs-003", "fidelity_level": "fidelity_3", "promoted": "false", "validation_calibrated_monotone_ipcw_ibs": 0.154, "runtime_sec": 5.1, "config_hash": "ogk-0a31f7c1"},
    {"dataset": "azure", "censoring_rate": 0.0, "seed": 0, "model": "ocean_mamba_kan", "search_method": "ga_amfpo", "candidate_id": "ga-001", "fidelity_level": "fidelity_1", "promoted": "true", "validation_calibrated_monotone_ipcw_ibs": 0.224, "runtime_sec": 1.5, "config_hash": "omk-a1b2c3d4"},
    {"dataset": "azure", "censoring_rate": 0.0, "seed": 0, "model": "ocean_mamba_kan", "search_method": "ga_amfpo", "candidate_id": "ga-002", "fidelity_level": "fidelity_2", "promoted": "true", "validation_calibrated_monotone_ipcw_ibs": 0.197, "runtime_sec": 3.0, "config_hash": "omk-b2c3d4e5"},
    {"dataset": "azure", "censoring_rate": 0.0, "seed": 0, "model": "ocean_mamba_kan", "search_method": "ga_amfpo", "candidate_id": "ga-003", "fidelity_level": "fidelity_3", "promoted": "false", "validation_calibrated_monotone_ipcw_ibs": 0.149, "runtime_sec": 5.8, "config_hash": "omk-9c44d2ab"},
    {"dataset": "scania", "censoring_rate": 0.0, "seed": 0, "model": "ocean_transformer_kan", "search_method": "random_search", "candidate_id": "rs-101", "fidelity_level": "fidelity_1", "promoted": "true", "validation_calibrated_monotone_ipcw_ibs": 0.205, "runtime_sec": 1.4, "config_hash": "otk-11223344"},
    {"dataset": "scania", "censoring_rate": 0.0, "seed": 0, "model": "ocean_transformer_kan", "search_method": "random_search", "candidate_id": "rs-102", "fidelity_level": "fidelity_2", "promoted": "true", "validation_calibrated_monotone_ipcw_ibs": 0.178, "runtime_sec": 2.7, "config_hash": "otk-22334455"},
    {"dataset": "scania", "censoring_rate": 0.0, "seed": 0, "model": "ocean_transformer_kan", "search_method": "random_search", "candidate_id": "rs-103", "fidelity_level": "fidelity_3", "promoted": "false", "validation_calibrated_monotone_ipcw_ibs": 0.166, "runtime_sec": 5.4, "config_hash": "otk-3e77b5af"},
    {"dataset": "cmapss_fd004", "censoring_rate": 0.3, "seed": 0, "model": "ocean_transformer_kan", "search_method": "ga_amfpo", "candidate_id": "ga-201", "fidelity_level": "fidelity_1", "promoted": "true", "validation_calibrated_monotone_ipcw_ibs": 0.221, "runtime_sec": 1.6, "config_hash": "otk-55667788"},
    {"dataset": "cmapss_fd004", "censoring_rate": 0.3, "seed": 0, "model": "ocean_transformer_kan", "search_method": "ga_amfpo", "candidate_id": "ga-202", "fidelity_level": "fidelity_2", "promoted": "true", "validation_calibrated_monotone_ipcw_ibs": 0.197, "runtime_sec": 3.2, "config_hash": "otk-66778899"},
    {"dataset": "cmapss_fd004", "censoring_rate": 0.3, "seed": 0, "model": "ocean_transformer_kan", "search_method": "ga_amfpo", "candidate_id": "ga-203", "fidelity_level": "fidelity_3", "promoted": "false", "validation_calibrated_monotone_ipcw_ibs": 0.181, "runtime_sec": 6.0, "config_hash": "otk-3e77b5af"},
]


ROOT_README = dedent(
    """
    # Predictive Maintenance Sample Data

    ## Overview

    This repository provides small illustrative data samples for the OCEAN-MO-CDSF framework, an evidence-driven multi-objective deep survival framework for censored predictive maintenance.

    ## What This Repository Contains

    - Survival test cases
    - Survival frame samples
    - Audit table samples
    - Model result samples
    - HPO trace samples
    - Validation scripts

    ## What This Repository Does Not Contain

    - It does not contain the full benchmark dataset.
    - It does not redistribute raw Azure, Scania, or C-MAPSS data.
    - It does not contain model checkpoints, trained weights, raw industrial logs, or private data.
    - It does not contain ontology, KG, or graph data.

    ## Directory Structure

    ```text
    predictive-maintenance-sample-data/
    ├── README.md
    ├── .gitignore
    ├── scripts/
    │   ├── create_data_samples.py
    │   └── validate_data_samples.py
    └── data_samples/
        ├── README.md
        ├── data_format_specification.md
        ├── VALIDATION_REPORT.md
        └── data/
            ├── README.md
            ├── test_set_samples/
            ├── survival_frame_samples/
            ├── audit_samples/
            ├── result_samples/
            └── hpo_samples/
    ```

    ## Quick Start

    ```bash
    python scripts/create_data_samples.py
    python scripts/validate_data_samples.py
    ```

    ## Main Data Format

    The central format is a multi-horizon survival frame with metadata columns, event/censoring labels, and feature-summary columns.

    ## Validation

    The validator checks required files, JSON and CSV readability, event and duration validity, censoring-rate range, horizon monotonicity, feature leakage column names, and HPO trace consistency.

    ## Citation / Paper Placeholder

    If you use this sample repository, please cite the associated OCEAN-MO-CDSF paper once available.

    ## License / Data Note

    All provided values are illustrative and anonymized/synthetic for format demonstration.
    """
).strip() + "\n"

DATA_SAMPLES_README = dedent(
    """
    # OCEAN-MO-CDSF Dataset Samples

    ## Overview

    This folder documents the sample data formats used by OCEAN-MO-CDSF for censored predictive-maintenance survival analysis.

    ## Purpose

    - Inspect the expected survival-frame schema
    - Understand event and censoring labels
    - Understand audit-table formats
    - Understand model-result and HPO-trace formats
    - Run lightweight validation without full raw datasets

    ## Dataset Components

    | Component | Folder | Purpose | Main files |
    | --- | --- | --- | --- |
    | Test set samples | `data/test_set_samples/` | Survival and censoring case examples | `sample_survival_cases.json` |
    | Survival frame samples | `data/survival_frame_samples/` | Model input frame format | `survival_frame_sample.csv` |
    | Audit samples | `data/audit_samples/` | Data, leakage, and split audit examples | `dataset_audit_sample.csv`, `feature_leakage_audit_sample.csv`, `split_audit_sample.csv` |
    | Result samples | `data/result_samples/` | Benchmark metric table example | `model_result_sample.csv` |
    | HPO samples | `data/hpo_samples/` | Selected config and candidate trace examples | `hpo_selected_config_sample.json`, `hpo_candidate_trace_sample.csv` |

    If present, `data/quick_view/` may provide convenience copies and `data/processed_mini_samples/` may provide small processed or anonymized mini frames.

    ## Directory Tree

    ```text
    data_samples/
    ├── README.md
    ├── .gitignore
    ├── data_format_specification.md
    ├── VALIDATION_REPORT.md
    └── data/
        ├── README.md
        ├── test_set_samples/
        ├── survival_frame_samples/
        ├── audit_samples/
        ├── result_samples/
        └── hpo_samples/
    ```

    ## Usage Examples

    ```python
    import json
    from pathlib import Path

    path = Path("data_samples/data/test_set_samples/sample_survival_cases.json")
    cases = json.loads(path.read_text(encoding="utf-8"))
    print(cases["cases"][0] if isinstance(cases, dict) else cases[0])
    ```

    ```python
    import pandas as pd

    df = pd.read_csv("data_samples/data/survival_frame_samples/survival_frame_sample.csv")
    print(df.head())
    ```

    ```python
    audit = pd.read_csv("data_samples/data/audit_samples/dataset_audit_sample.csv")
    print(audit[["dataset", "event_rate", "status"]])
    ```

    ```python
    results = pd.read_csv("data_samples/data/result_samples/model_result_sample.csv")
    print(results.sort_values("validation_calibrated_monotone_ipcw_ibs").head())
    ```

    ```python
    trace = pd.read_csv("data_samples/data/hpo_samples/hpo_candidate_trace_sample.csv")
    print(trace.groupby(["model", "fidelity_level"]).size())
    ```

    ## Event and Censoring Interpretation

    - `event=1`: observed failure
    - `event=0`: right-censored
    - `duration`: observed time-to-event or time-to-censoring
    - `censoring_rate`: administrative censoring setting or scenario indicator
    - `censoring_rate_observed`: observed censoring proportion in an audit table

    ## Feature Leakage Warning

    `duration`, `event`, `event_type`, `unit_id`, `anchor_time`, `failure_time`, `rul`, and `censor_time` must not be used as predictive features.

    ## Validation and Test Separation

    Validation metrics are used for model selection. Test metrics are reported only after the selected model or configuration is fixed.

    ## Data Availability Note

    These files are sufficient for schema inspection and validator testing, not for reproducing paper-scale benchmark metrics.
    """
).strip() + "\n"

DATA_DIR_README = dedent(
    """
    # Data Directory Index

    ## Overview

    This directory contains grouped sample files for quick navigation.

    ## Folder Index

    | Folder | Contains | Main data file |
    | --- | --- | --- |
    | `test_set_samples/` | Survival case examples | `sample_survival_cases.json` |
    | `survival_frame_samples/` | Model input frame example | `survival_frame_sample.csv` |
    | `audit_samples/` | Audit table examples | `dataset_audit_sample.csv` |
    | `result_samples/` | Benchmark result example | `model_result_sample.csv` |
    | `hpo_samples/` | HPO config and trace examples | `hpo_candidate_trace_sample.csv` |

    ## Direct Links

    - `test_set_samples/sample_survival_cases.json`
    - `survival_frame_samples/survival_frame_sample.csv`
    - `survival_frame_samples/survival_frame_column_dictionary.csv`
    - `audit_samples/dataset_audit_sample.csv`
    - `audit_samples/feature_leakage_audit_sample.csv`
    - `audit_samples/split_audit_sample.csv`
    - `result_samples/model_result_sample.csv`
    - `hpo_samples/hpo_selected_config_sample.json`
    - `hpo_samples/hpo_candidate_trace_sample.csv`

    ## Notes

    The structured folders are authoritative. If `quick_view/` exists, it only provides convenience copies. If `processed_mini_samples/` exists, it only provides small processed or anonymized mini samples.
    """
).strip() + "\n"

DATA_FORMAT_SPEC = dedent(
    """
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
    """
).strip() + "\n"

TEST_SET_README = dedent(
    """
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
    """
).strip() + "\n"

SURVIVAL_FRAME_README = dedent(
    """
    # Survival Frame Samples

    ## Purpose

    This folder contains compact survival-frame rows that demonstrate the tabular format used by OCEAN-MO-CDSF.

    ## Files

    - `survival_frame_sample.csv`
    - `survival_frame_schema.json`
    - `survival_frame_column_dictionary.csv`

    ## Format Summary

    CSV table with target, metadata, and feature columns plus a column dictionary.

    ## Example Row

    ```csv
    sample_id,dataset,unit_id,anchor_time,duration,event,event_type,censoring_rate,horizon_1,horizon_2,horizon_3,horizon_4,static_feature_1,static_feature_2,seq_feature_mean_1,seq_feature_std_1,seq_feature_last_1,missing_rate,padding_rate
    SF_001,azure,unit_0001,2026-05-01T08:00:00Z,96,1,observed_failure,0.0,24,72,168,336,0.45,0.12,0.62,0.08,0.70,0.00,0.00
    ```

    ## Python Loading Example

    ```python
    import pandas as pd

    df = pd.read_csv("data_samples/data/survival_frame_samples/survival_frame_sample.csv")
    print(df.head())
    ```

    ## Notes and Warnings

    - `duration`, `event`, `event_type`, `unit_id`, and `anchor_time` are labels or metadata and must not be used as predictive features.
    - The column dictionary defines which columns are intended for features.
    - `missing_rate` and `padding_rate` are metadata by default unless explicitly promoted.
    """
).strip() + "\n"

AUDIT_README = dedent(
    """
    # Audit Samples

    ## Purpose

    This folder contains compact examples of dataset auditing, feature leakage review, and unit-level split checking.

    ## Files

    - `dataset_audit_sample.csv`
    - `feature_leakage_audit_sample.csv`
    - `split_audit_sample.csv`

    ## Format Summary

    CSV audit tables with pass or fail style statuses and simple boolean-like fields.

    ## Example Rows

    ```csv
    dataset,censoring_rate,samples,units,event_rate,censoring_rate_observed,duration_median,padding_rate,missing_rate,fallback,status
    azure,0.0,120,14,0.42,0.08,18.4,0.01,0.02,false,pass
    ```

    ## Python Loading Example

    ```python
    import pandas as pd

    dataset_audit = pd.read_csv("data_samples/data/audit_samples/dataset_audit_sample.csv")
    print(dataset_audit[["dataset", "event_rate", "status"]])
    ```

    ## Notes and Warnings

    - Dataset audits summarize censoring, duration, missingness, and fallback state.
    - Feature leakage audits should confirm that forbidden tokens do not appear in feature names.
    - Split audits should be unit-disjoint with `overlap_unit_count = 0` for passed rows.
    """
).strip() + "\n"

RESULT_README = dedent(
    """
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
    """
).strip() + "\n"

HPO_README = dedent(
    """
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
    """
).strip() + "\n"

def print_tree(root: Path) -> None:
    def walk(path: Path, prefix: str = "") -> None:
        entries = sorted(path.iterdir(), key=lambda p: (p.is_file(), p.name.lower()))
        for index, entry in enumerate(entries):
            is_last = index == len(entries) - 1
            connector = "`-- " if is_last else "|-- "
            print(f"{prefix}{connector}{entry.name}")
            if entry.is_dir():
                extension = "    " if is_last else "|   "
                walk(entry, prefix + extension)

    print(root.name + "/")
    walk(root)


def main() -> None:
    ensure_text_file(REPO_ROOT / "README.md", ROOT_README)
    ensure_text_file(REPO_ROOT / ".gitignore", ROOT_GITIGNORE)
    ensure_text_file(DATA_SAMPLES_ROOT / ".gitignore", DATA_SAMPLES_GITIGNORE)
    ensure_text_file(DATA_SAMPLES_ROOT / "README.md", DATA_SAMPLES_README)
    ensure_text_file(DATA_SAMPLES_ROOT / "data" / "README.md", DATA_DIR_README)
    ensure_text_file(DATA_SAMPLES_ROOT / "data_format_specification.md", DATA_FORMAT_SPEC)
    ensure_text_file(DATA_SAMPLES_ROOT / "data" / "processed_mini_samples" / "README.md", PROCESSED_MINI_README)
    ensure_text_file(DATA_SAMPLES_ROOT / "data" / "quick_view" / "README.md", QUICK_VIEW_README)

    ensure_text_file(DATA_SAMPLES_ROOT / "data" / "test_set_samples" / "README.md", TEST_SET_README)
    write_json(DATA_SAMPLES_ROOT / "data" / "test_set_samples" / "sample_survival_cases.json", TEST_CASES)
    write_json(DATA_SAMPLES_ROOT / "data" / "test_set_samples" / "sample_survival_cases_schema.json", TEST_CASE_SCHEMA)

    ensure_text_file(DATA_SAMPLES_ROOT / "data" / "survival_frame_samples" / "README.md", SURVIVAL_FRAME_README)
    write_csv(
        DATA_SAMPLES_ROOT / "data" / "survival_frame_samples" / "survival_frame_sample.csv",
        SURVIVAL_FRAME_ROWS,
        [
            "sample_id",
            "dataset",
            "unit_id",
            "anchor_time",
            "duration",
            "event",
            "event_type",
            "censoring_rate",
            "horizon_1",
            "horizon_2",
            "horizon_3",
            "horizon_4",
            "static_feature_1",
            "static_feature_2",
            "seq_feature_mean_1",
            "seq_feature_std_1",
            "seq_feature_last_1",
            "missing_rate",
            "padding_rate",
        ],
    )
    write_json(DATA_SAMPLES_ROOT / "data" / "survival_frame_samples" / "survival_frame_schema.json", SURVIVAL_FRAME_SCHEMA)
    write_csv(
        DATA_SAMPLES_ROOT / "data" / "survival_frame_samples" / "survival_frame_column_dictionary.csv",
        SURVIVAL_FRAME_COLUMN_DICTIONARY_ROWS,
        ["column_name", "role", "dtype", "allowed_values", "description", "used_as_feature"],
    )

    ensure_text_file(DATA_SAMPLES_ROOT / "data" / "audit_samples" / "README.md", AUDIT_README)
    write_csv(
        DATA_SAMPLES_ROOT / "data" / "audit_samples" / "dataset_audit_sample.csv",
        DATASET_AUDIT_ROWS,
        ["dataset", "censoring_rate", "samples", "units", "event_rate", "censoring_rate_observed", "duration_median", "padding_rate", "missing_rate", "fallback", "status"],
    )
    write_csv(
        DATA_SAMPLES_ROOT / "data" / "audit_samples" / "feature_leakage_audit_sample.csv",
        FEATURE_LEAKAGE_AUDIT_ROWS,
        ["dataset", "censoring_rate", "seq_feature_count", "static_feature_count", "bad_seq_features", "bad_static_features", "status"],
    )
    write_csv(
        DATA_SAMPLES_ROOT / "data" / "audit_samples" / "split_audit_sample.csv",
        SPLIT_AUDIT_ROWS,
        ["dataset", "censoring_rate", "seed", "train_units", "calibration_units", "validation_units", "test_units", "overlap_unit_count", "status"],
    )

    ensure_text_file(DATA_SAMPLES_ROOT / "data" / "result_samples" / "README.md", RESULT_README)
    write_csv(
        DATA_SAMPLES_ROOT / "data" / "result_samples" / "model_result_sample.csv",
        MODEL_RESULTS_ROWS,
        ["dataset", "censoring_rate", "seed", "model", "validation_calibrated_monotone_ipcw_ibs", "test_calibrated_monotone_ipcw_ibs", "c_index", "ece", "cost_top10", "riw", "runtime_sec", "selected_by_validation"],
    )

    ensure_text_file(DATA_SAMPLES_ROOT / "data" / "hpo_samples" / "README.md", HPO_README)
    write_json(DATA_SAMPLES_ROOT / "data" / "hpo_samples" / "hpo_selected_config_sample.json", HPO_SELECTED_CONFIG)
    write_csv(
        DATA_SAMPLES_ROOT / "data" / "hpo_samples" / "hpo_candidate_trace_sample.csv",
        HPO_CANDIDATE_TRACE_ROWS,
        ["dataset", "censoring_rate", "seed", "model", "search_method", "candidate_id", "fidelity_level", "promoted", "validation_calibrated_monotone_ipcw_ibs", "runtime_sec", "config_hash"],
    )

    print("Created or updated the following sample-data tree:")
    print_tree(DATA_SAMPLES_ROOT)


if __name__ == "__main__":
    main()
