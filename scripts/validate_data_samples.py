from __future__ import annotations

import csv
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_SAMPLES_ROOT = REPO_ROOT / "data_samples"
REPORT_PATH = DATA_SAMPLES_ROOT / "VALIDATION_REPORT.md"


try:
    import pandas as pd  # type: ignore

    PANDAS_AVAILABLE = True
except Exception:  # pragma: no cover - optional dependency
    pd = None  # type: ignore
    PANDAS_AVAILABLE = False


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_csv(path: Path) -> list[dict[str, Any]]:
    if PANDAS_AVAILABLE:
        df = pd.read_csv(path)
        return df.to_dict(orient="records")
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def is_bool_like(value: Any) -> bool:
    if isinstance(value, bool):
        return True
    if value is None:
        return False
    if isinstance(value, (int, float)) and value in {0, 1}:
        return True
    if isinstance(value, str):
        return value.strip().lower() in {"true", "false", "yes", "no", "0", "1"}
    return False


def as_float(value: Any) -> float:
    if isinstance(value, bool):
        return float(int(value))
    return float(value)


def as_int(value: Any) -> int:
    if isinstance(value, bool):
        return int(value)
    return int(float(value))


def as_str(value: Any) -> str:
    if value is None:
        return ""
    return str(value)


@dataclass
class Check:
    name: str
    passed: bool
    details: str


def check_required_files() -> Check:
    required = [
        REPO_ROOT / "README.md",
        REPO_ROOT / ".gitignore",
        DATA_SAMPLES_ROOT / "README.md",
        DATA_SAMPLES_ROOT / ".gitignore",
        DATA_SAMPLES_ROOT / "data_format_specification.md",
        DATA_SAMPLES_ROOT / "data" / "test_set_samples" / "README.md",
        DATA_SAMPLES_ROOT / "data" / "test_set_samples" / "sample_survival_cases.json",
        DATA_SAMPLES_ROOT / "data" / "test_set_samples" / "sample_survival_cases_schema.json",
        DATA_SAMPLES_ROOT / "data" / "survival_frame_samples" / "README.md",
        DATA_SAMPLES_ROOT / "data" / "survival_frame_samples" / "survival_frame_sample.csv",
        DATA_SAMPLES_ROOT / "data" / "survival_frame_samples" / "survival_frame_schema.json",
        DATA_SAMPLES_ROOT / "data" / "survival_frame_samples" / "survival_frame_column_dictionary.csv",
        DATA_SAMPLES_ROOT / "data" / "audit_samples" / "README.md",
        DATA_SAMPLES_ROOT / "data" / "audit_samples" / "dataset_audit_sample.csv",
        DATA_SAMPLES_ROOT / "data" / "audit_samples" / "feature_leakage_audit_sample.csv",
        DATA_SAMPLES_ROOT / "data" / "audit_samples" / "split_audit_sample.csv",
        DATA_SAMPLES_ROOT / "data" / "result_samples" / "README.md",
        DATA_SAMPLES_ROOT / "data" / "result_samples" / "model_result_sample.csv",
        DATA_SAMPLES_ROOT / "data" / "hpo_samples" / "README.md",
        DATA_SAMPLES_ROOT / "data" / "hpo_samples" / "hpo_selected_config_sample.json",
        DATA_SAMPLES_ROOT / "data" / "hpo_samples" / "hpo_candidate_trace_sample.csv",
    ]
    missing = [str(path.relative_to(REPO_ROOT)) for path in required if not path.exists()]
    if missing:
        return Check("Required file existence", False, f"Missing files: {', '.join(missing)}")
    return Check("Required file existence", True, "All required files are present.")


def check_json_loads() -> list[Check]:
    checks = []
    for rel in [
        "data_samples/data/test_set_samples/sample_survival_cases.json",
        "data_samples/data/test_set_samples/sample_survival_cases_schema.json",
        "data_samples/data/survival_frame_samples/survival_frame_schema.json",
        "data_samples/data/hpo_samples/hpo_selected_config_sample.json",
    ]:
        path = REPO_ROOT / rel
        try:
            load_json(path)
            checks.append(Check(f"JSON load: {rel}", True, "Loaded successfully."))
        except Exception as exc:  # pragma: no cover - simple report path
            checks.append(Check(f"JSON load: {rel}", False, f"Failed to load JSON: {exc}"))
    return checks


def check_csv_loads() -> list[Check]:
    checks = []
    for rel in [
        "data_samples/data/survival_frame_samples/survival_frame_sample.csv",
        "data_samples/data/survival_frame_samples/survival_frame_column_dictionary.csv",
        "data_samples/data/audit_samples/dataset_audit_sample.csv",
        "data_samples/data/audit_samples/feature_leakage_audit_sample.csv",
        "data_samples/data/audit_samples/split_audit_sample.csv",
        "data_samples/data/result_samples/model_result_sample.csv",
        "data_samples/data/hpo_samples/hpo_candidate_trace_sample.csv",
    ]:
        path = REPO_ROOT / rel
        try:
            rows = load_csv(path)
            if not rows:
                raise ValueError("CSV contains no data rows.")
            checks.append(Check(f"CSV load: {rel}", True, f"Loaded {len(rows)} rows successfully."))
        except Exception as exc:  # pragma: no cover - simple report path
            checks.append(Check(f"CSV load: {rel}", False, f"Failed to load CSV: {exc}"))
    return checks


def check_survival_frame() -> list[Check]:
    path = REPO_ROOT / "data_samples/data/survival_frame_samples/survival_frame_sample.csv"
    rows = load_csv(path)
    checks: list[Check] = []

    required_datasets = {"azure", "scania", "cmapss_fd001", "cmapss_fd004"}
    datasets = {as_str(row["dataset"]) for row in rows}
    checks.append(Check("Survival frame datasets", required_datasets.issubset(datasets), f"Found datasets: {sorted(datasets)}"))

    checks.append(Check("Survival frame row count", len(rows) == 20, f"Row count = {len(rows)}"))

    has_event_1 = any(as_int(row["event"]) == 1 for row in rows)
    has_event_0 = any(as_int(row["event"]) == 0 for row in rows)
    has_censoring_0 = any(abs(as_float(row["censoring_rate"]) - 0.0) < 1e-9 for row in rows)
    has_censoring_03 = any(abs(as_float(row["censoring_rate"]) - 0.3) < 1e-9 for row in rows)
    checks.append(Check("Survival frame event coverage", has_event_0 and has_event_1, "event values 0 and 1 are both present."))
    checks.append(Check("Survival frame censoring coverage", has_censoring_0 and has_censoring_03, "censoring_rate values 0.0 and 0.3 are both present."))

    row_errors = []
    for idx, row in enumerate(rows, start=1):
        duration = as_float(row["duration"])
        event = as_int(row["event"])
        censoring_rate = as_float(row["censoring_rate"])
        horizons = [as_int(row[f"horizon_{i}"]) for i in range(1, 5)]
        missing_rate = as_float(row["missing_rate"])
        padding_rate = as_float(row["padding_rate"])

        if duration <= 0:
            row_errors.append(f"row {idx} duration <= 0")
        if event not in {0, 1}:
            row_errors.append(f"row {idx} event not in {{0,1}}")
        if not (0.0 <= censoring_rate <= 1.0):
            row_errors.append(f"row {idx} censoring_rate outside [0,1]")
        if not (horizons[0] <= horizons[1] <= horizons[2] <= horizons[3]):
            row_errors.append(f"row {idx} horizons not monotone")
        if not (0.0 <= missing_rate <= 1.0):
            row_errors.append(f"row {idx} missing_rate outside [0,1]")
        if not (0.0 <= padding_rate <= 1.0):
            row_errors.append(f"row {idx} padding_rate outside [0,1]")

    checks.append(Check("Survival frame value ranges", not row_errors, "All rows satisfy duration/event/censoring/horizon/missing/padding constraints." if not row_errors else "; ".join(row_errors)))
    return checks


def check_column_dictionary() -> list[Check]:
    path = REPO_ROOT / "data_samples/data/survival_frame_samples/survival_frame_column_dictionary.csv"
    rows = load_csv(path)
    checks: list[Check] = []

    required_false = {"sample_id", "dataset", "unit_id", "anchor_time", "duration", "event", "event_type", "censoring_rate"}
    required_true = {"static_feature_1", "static_feature_2", "seq_feature_mean_1", "seq_feature_std_1", "seq_feature_last_1"}
    row_map = {as_str(row["column_name"]): row for row in rows}

    missing = sorted((required_false | required_true) - row_map.keys())
    checks.append(Check("Column dictionary completeness", not missing, "Missing columns: " + ", ".join(missing) if missing else "All expected columns are present."))

    false_issues = []
    for name in required_false:
        value = as_str(row_map[name]["used_as_feature"]).strip().lower()
        if value != "false":
            false_issues.append(name)
    checks.append(Check("Column dictionary metadata flags", not false_issues, "used_as_feature must be false for: " + ", ".join(false_issues) if false_issues else "All metadata/outcome columns are marked false."))

    true_issues = []
    for name in required_true:
        value = as_str(row_map[name]["used_as_feature"]).strip().lower()
        if value != "true":
            true_issues.append(name)
    checks.append(Check("Column dictionary feature flags", not true_issues, "used_as_feature must be true for: " + ", ".join(true_issues) if true_issues else "All model feature columns are marked true."))

    missing_and_padding = []
    for name in ["missing_rate", "padding_rate"]:
        if name in row_map and as_str(row_map[name]["used_as_feature"]).strip().lower() != "false":
            missing_and_padding.append(name)
    checks.append(Check("Column dictionary missing/padding flags", not missing_and_padding, "missing_rate and padding_rate remain metadata by default." if not missing_and_padding else ", ".join(missing_and_padding) + " should be false."))

    forbidden_tokens = ("failure_time", "rul", "censor_time")
    bad_names = [name for name, row in row_map.items() if as_str(row["used_as_feature"]).strip().lower() == "true" and any(token in name for token in forbidden_tokens)]
    checks.append(Check("Feature leakage tokens", not bad_names, "No feature column names contain forbidden tokens." if not bad_names else "Forbidden feature names: " + ", ".join(bad_names)))
    return checks


def check_hpo_json() -> list[Check]:
    path = REPO_ROOT / "data_samples/data/hpo_samples/hpo_selected_config_sample.json"
    payload = load_json(path)
    configs = payload.get("selected_configs", []) if isinstance(payload, dict) else []
    checks: list[Check] = []
    checks.append(Check("HPO JSON selected config count", len(configs) == 3, f"Selected config count = {len(configs)}"))

    required_models = {"ocean_gru_kan", "ocean_mamba_kan", "ocean_transformer_kan"}
    present_models = {cfg.get("model") for cfg in configs if isinstance(cfg, dict)}
    checks.append(Check("HPO JSON model coverage", required_models == present_models, f"Models present: {sorted(map(str, present_models))}"))

    required_fields = {"dataset", "censoring_rate", "seed", "model", "search_method", "config_hash", "hyperparameters", "validation_metric", "test_metric_reported_only", "fidelity_level", "selected_by_validation"}
    field_issues = []
    for idx, cfg in enumerate(configs, start=1):
        if not isinstance(cfg, dict):
            field_issues.append(f"config {idx} is not an object")
            continue
        missing = required_fields - cfg.keys()
        if missing:
            field_issues.append(f"config {idx} missing: {sorted(missing)}")
        if "test_metric_reported_only" in cfg and cfg["test_metric_reported_only"] is None:
            field_issues.append(f"config {idx} has empty test_metric_reported_only")
        if "selected_by_validation" in cfg and not is_bool_like(cfg["selected_by_validation"]):
            field_issues.append(f"config {idx} selected_by_validation is not boolean-like")
    checks.append(Check("HPO JSON required fields", not field_issues, "All required fields are present and boolean-like where needed." if not field_issues else "; ".join(field_issues)))
    return checks


def check_result_sample() -> list[Check]:
    path = REPO_ROOT / "data_samples/data/result_samples/model_result_sample.csv"
    rows = load_csv(path)
    checks: list[Check] = []
    if not rows:
        return [Check("Result sample rows", False, "No rows found.")]

    bool_issues = []
    numeric_fields = [
        "validation_calibrated_monotone_ipcw_ibs",
        "test_calibrated_monotone_ipcw_ibs",
        "c_index",
        "ece",
        "cost_top10",
        "riw",
        "runtime_sec",
    ]
    numeric_issues = []
    selected_true = 0
    for idx, row in enumerate(rows, start=1):
        if not is_bool_like(row["selected_by_validation"]):
            bool_issues.append(f"row {idx}")
        else:
            if as_str(row["selected_by_validation"]).strip().lower() in {"true", "1", "yes"}:
                selected_true += 1
        for field in numeric_fields:
            try:
                as_float(row[field])
            except Exception:
                numeric_issues.append(f"row {idx} field {field}")

    checks.append(Check("Result sample boolean flag", not bool_issues, "selected_by_validation is boolean-like in every row." if not bool_issues else "Non-boolean-like rows: " + ", ".join(bool_issues)))
    checks.append(Check("Result sample numeric metrics", not numeric_issues, "Metric columns are numeric in every row." if not numeric_issues else "Numeric conversion issues: " + ", ".join(numeric_issues)))
    checks.append(Check("Result sample selection flag", selected_true >= 1, f"Rows marked selected_by_validation=true: {selected_true}"))
    return checks


def check_audit_samples() -> list[Check]:
    checks: list[Check] = []

    dataset_rows = load_csv(REPO_ROOT / "data_samples/data/audit_samples/dataset_audit_sample.csv")
    status_ok = all(as_str(row["status"]).strip().lower() in {"pass", "passed"} for row in dataset_rows)
    fallback_ok = all(is_bool_like(row["fallback"]) for row in dataset_rows)
    checks.append(Check("Dataset audit status values", status_ok, "All dataset audit statuses are pass/passed." if status_ok else "At least one dataset audit status is not pass/passed."))
    checks.append(Check("Dataset audit fallback flags", fallback_ok, "All fallback values are boolean-like." if fallback_ok else "At least one fallback value is not boolean-like."))

    leakage_rows = load_csv(REPO_ROOT / "data_samples/data/audit_samples/feature_leakage_audit_sample.csv")
    leakage_status_ok = all(as_str(row["status"]).strip().lower() in {"pass", "passed"} for row in leakage_rows)
    checks.append(Check("Feature leakage audit status", leakage_status_ok, "All leakage audit statuses are pass/passed." if leakage_status_ok else "At least one leakage audit status is not pass/passed."))

    split_rows = load_csv(REPO_ROOT / "data_samples/data/audit_samples/split_audit_sample.csv")
    split_status_ok = all(as_str(row["status"]).strip().lower() in {"pass", "passed"} for row in split_rows)
    overlap_ok = all(as_int(row["overlap_unit_count"]) == 0 for row in split_rows)
    checks.append(Check("Split audit status", split_status_ok, "All split audit statuses are pass/passed." if split_status_ok else "At least one split audit status is not pass/passed."))
    checks.append(Check("Split audit overlap", overlap_ok, "All overlap_unit_count values are 0." if overlap_ok else "At least one split shows overlap."))

    return checks


def write_report(checks: list[Check]) -> None:
    lines = [
        "# Data Samples Validation Report",
        "",
        f"- Pandas available: {PANDAS_AVAILABLE}",
        f"- Overall status: {'PASS' if all(check.passed for check in checks) else 'FAIL'}",
        "",
    ]
    for check in checks:
        status = "PASS" if check.passed else "FAIL"
        lines.append(f"- {status}: {check.name} - {check.details}")
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    checks: list[Check] = []
    checks.append(check_required_files())
    checks.extend(check_json_loads())
    checks.extend(check_csv_loads())
    checks.extend(check_survival_frame())
    checks.extend(check_column_dictionary())
    checks.extend(check_hpo_json())
    checks.extend(check_result_sample())
    checks.extend(check_audit_samples())

    for check in checks:
        print(f"{'PASS' if check.passed else 'FAIL'}: {check.name} - {check.details}")

    write_report(checks)

    return 0 if all(check.passed for check in checks) else 1


if __name__ == "__main__":
    sys.exit(main())
