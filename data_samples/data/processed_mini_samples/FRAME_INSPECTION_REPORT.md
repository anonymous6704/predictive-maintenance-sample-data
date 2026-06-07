# Frame Inspection Report

- Source frames root: `ocean_mo_cdsf/data/frames`
- Deterministic sampling seed: `0`
- Maximum sampled rows per file: `300`

## azure_0_frame.npz

- Source frame: `azure_0_frame.npz`
- Shape: 50000 rows
- Keys: x_seq, x_static, seq_mask, missing_mask, delta_t, duration, event, event_type, unit_id, anchor_time, dataset_name, feature_names_seq, feature_names_static, meta_json

| Key | Shape | Dtype |
| --- | --- | --- |
| `x_seq` | `(50000, 20, 9)` | `float32` |
| `x_static` | `(50000, 2)` | `float32` |
| `seq_mask` | `(50000, 20)` | `float32` |
| `missing_mask` | `(50000, 20, 9)` | `float32` |
| `delta_t` | `(50000, 20)` | `float32` |
| `duration` | `(50000,)` | `float32` |
| `event` | `(50000,)` | `int64` |
| `event_type` | `(50000,)` | `int64` |
| `unit_id` | `(50000,)` | `object` |
| `anchor_time` | `(50000,)` | `float32` |
| `dataset_name` | `()` | `<U5` |
| `feature_names_seq` | `(9,)` | `object` |
| `feature_names_static` | `(2,)` | `object` |
| `meta_json` | `()` | `<U754` |

- Has `duration`: yes
- Has `event`: yes
- Has `unit_id`: yes
- Has `anchor_time`: yes
- Has horizon-like key: no
- Meta JSON keys: adapter, azure_censoring_explanation, censored_anchor_rows_before_duration_filter, censored_final_episodes, dataset, no_failure_units, observed_anchor_rows_before_duration_filter, observed_failure_episodes, source_type, synthetic_fallback, target_censoring_rate
- Meta JSON summary: adapter=azure_recurrent_event, dataset=azure, source_type=real_raw_csv, synthetic_fallback=False, target_censoring_rate=0.0

- Selected rows: 300
- Unique source units in sample: 100
- Event counts: observed=255, censored=45
- Original unit sample: 51, 12, 21, 58, 20, 88, 45, 9, 99, 69...
- Notes: extracted deterministically with seed=0; horizon grid defaulted to [24, 72, 168, 336]; source_frame stores only the file name.

## scania_0_frame.npz

- Source frame: `scania_0_frame.npz`
- Upstream provenance: SCANIA Component X-derived survival/time-to-event frame; not UCI APS Failure at Scania Trucks.
- Shape: 151031 rows
- Keys: x_seq, x_static, seq_mask, missing_mask, delta_t, duration, event, event_type, unit_id, anchor_time, dataset_name, feature_names_seq, feature_names_static, meta_json

| Key | Shape | Dtype |
| --- | --- | --- |
| `x_seq` | `(151031, 20, 105)` | `float32` |
| `x_static` | `(151031, 29)` | `float32` |
| `seq_mask` | `(151031, 20)` | `float32` |
| `missing_mask` | `(151031, 20, 105)` | `float32` |
| `delta_t` | `(151031, 20)` | `float32` |
| `duration` | `(151031,)` | `float32` |
| `event` | `(151031,)` | `int64` |
| `event_type` | `(151031,)` | `int64` |
| `unit_id` | `(151031,)` | `object` |
| `anchor_time` | `(151031,)` | `float32` |
| `dataset_name` | `()` | `<U6` |
| `feature_names_seq` | `(105,)` | `object` |
| `feature_names_static` | `(29,)` | `object` |
| `meta_json` | `()` | `<U362` |

- Has `duration`: yes
- Has `event`: yes
- Has `unit_id`: yes
- Has `anchor_time`: yes
- Has horizon-like key: no
- Meta JSON keys: adapter, dataset, note, source_type, synthetic_fallback, target_censoring_rate
- Meta JSON summary: adapter=scania_observed_censoring, dataset=scania, source_type=real_raw_csv, synthetic_fallback=False, target_censoring_rate=0.0

- Selected rows: 300
- Unique source units in sample: 300
- Event counts: observed=26, censored=274
- Original unit sample: 24459, 3458, 25672, 11469, 26267, 19303, 13851, 14700, 14911, 3517...
- Notes: extracted deterministically with seed=0; horizon grid defaulted to [24, 72, 168, 336]; source_frame stores only the file name.

## cmapss_fd001_0_frame.npz

- Source frame: `cmapss_fd001_0_frame.npz`
- Shape: 6042 rows
- Keys: x_seq, x_static, seq_mask, missing_mask, delta_t, duration, event, event_type, unit_id, anchor_time, dataset_name, feature_names_seq, feature_names_static, meta_json

| Key | Shape | Dtype |
| --- | --- | --- |
| `x_seq` | `(6042, 20, 24)` | `float32` |
| `x_static` | `(6042, 1)` | `float32` |
| `seq_mask` | `(6042, 20)` | `float32` |
| `missing_mask` | `(6042, 20, 24)` | `float32` |
| `delta_t` | `(6042, 20)` | `float32` |
| `duration` | `(6042,)` | `float32` |
| `event` | `(6042,)` | `int64` |
| `event_type` | `(6042,)` | `int64` |
| `unit_id` | `(6042,)` | `object` |
| `anchor_time` | `(6042,)` | `float32` |
| `dataset_name` | `()` | `<U12` |
| `feature_names_seq` | `(24,)` | `object` |
| `feature_names_static` | `(1,)` | `object` |
| `meta_json` | `()` | `<U403` |

- Has `duration`: yes
- Has `event`: yes
- Has `unit_id`: yes
- Has `anchor_time`: yes
- Has horizon-like key: no
- Meta JSON keys: actual_censored_unit_fraction, adapter, dataset, note, source_type, synthetic_fallback, target_censoring_rate
- Meta JSON summary: actual_censored_unit_fraction=0.0, adapter=cmapss_administrative_censoring, dataset=cmapss_fd001, source_type=real_raw_csv, synthetic_fallback=False, target_censoring_rate=0.0

- Selected rows: 300
- Unique source units in sample: 200
- Event counts: observed=300, censored=0
- Original unit sample: train_25, test_47, train_73, test_58, test_43, test_81, test_41, train_84, test_74, test_90...
- Notes: extracted deterministically with seed=0; horizon grid defaulted to [24, 72, 168, 336]; source_frame stores only the file name.

## cmapss_fd001_0p3_frame.npz

- Source frame: `cmapss_fd001_0p3_frame.npz`
- Shape: 5021 rows
- Keys: x_seq, x_static, seq_mask, missing_mask, delta_t, duration, event, event_type, unit_id, anchor_time, dataset_name, feature_names_seq, feature_names_static, meta_json

| Key | Shape | Dtype |
| --- | --- | --- |
| `x_seq` | `(5021, 20, 24)` | `float32` |
| `x_static` | `(5021, 1)` | `float32` |
| `seq_mask` | `(5021, 20)` | `float32` |
| `missing_mask` | `(5021, 20, 24)` | `float32` |
| `delta_t` | `(5021, 20)` | `float32` |
| `duration` | `(5021,)` | `float32` |
| `event` | `(5021,)` | `int64` |
| `event_type` | `(5021,)` | `int64` |
| `unit_id` | `(5021,)` | `object` |
| `anchor_time` | `(5021,)` | `float32` |
| `dataset_name` | `()` | `<U12` |
| `feature_names_seq` | `(24,)` | `object` |
| `feature_names_static` | `(1,)` | `object` |
| `meta_json` | `()` | `<U403` |

- Has `duration`: yes
- Has `event`: yes
- Has `unit_id`: yes
- Has `anchor_time`: yes
- Has horizon-like key: no
- Meta JSON keys: actual_censored_unit_fraction, adapter, dataset, note, source_type, synthetic_fallback, target_censoring_rate
- Meta JSON summary: actual_censored_unit_fraction=0.3, adapter=cmapss_administrative_censoring, dataset=cmapss_fd001, source_type=real_raw_csv, synthetic_fallback=False, target_censoring_rate=0.3

- Selected rows: 300
- Unique source units in sample: 200
- Event counts: observed=222, censored=78
- Original unit sample: test_97, train_83, test_62, train_25, train_33, train_17, train_43, train_89, train_44, train_54...
- Notes: extracted deterministically with seed=0; horizon grid defaulted to [24, 72, 168, 336]; source_frame stores only the file name.

## cmapss_fd002_0_frame.npz

- Source frame: `cmapss_fd002_0_frame.npz`
- Shape: 15728 rows
- Keys: x_seq, x_static, seq_mask, missing_mask, delta_t, duration, event, event_type, unit_id, anchor_time, dataset_name, feature_names_seq, feature_names_static, meta_json

| Key | Shape | Dtype |
| --- | --- | --- |
| `x_seq` | `(15728, 20, 24)` | `float32` |
| `x_static` | `(15728, 1)` | `float32` |
| `seq_mask` | `(15728, 20)` | `float32` |
| `missing_mask` | `(15728, 20, 24)` | `float32` |
| `delta_t` | `(15728, 20)` | `float32` |
| `duration` | `(15728,)` | `float32` |
| `event` | `(15728,)` | `int64` |
| `event_type` | `(15728,)` | `int64` |
| `unit_id` | `(15728,)` | `object` |
| `anchor_time` | `(15728,)` | `float32` |
| `dataset_name` | `()` | `<U12` |
| `feature_names_seq` | `(24,)` | `object` |
| `feature_names_static` | `(1,)` | `object` |
| `meta_json` | `()` | `<U403` |

- Has `duration`: yes
- Has `event`: yes
- Has `unit_id`: yes
- Has `anchor_time`: yes
- Has horizon-like key: no
- Meta JSON keys: actual_censored_unit_fraction, adapter, dataset, note, source_type, synthetic_fallback, target_censoring_rate
- Meta JSON summary: actual_censored_unit_fraction=0.0, adapter=cmapss_administrative_censoring, dataset=cmapss_fd002, source_type=real_raw_csv, synthetic_fallback=False, target_censoring_rate=0.0

- Selected rows: 300
- Unique source units in sample: 300
- Event counts: observed=300, censored=0
- Original unit sample: train_200, train_171, train_140, test_255, test_13, train_196, test_76, test_7, test_134, train_94...
- Notes: extracted deterministically with seed=0; horizon grid defaulted to [24, 72, 168, 336]; source_frame stores only the file name.

## cmapss_fd002_0p3_frame.npz

- Source frame: `cmapss_fd002_0p3_frame.npz`
- Shape: 13112 rows
- Keys: x_seq, x_static, seq_mask, missing_mask, delta_t, duration, event, event_type, unit_id, anchor_time, dataset_name, feature_names_seq, feature_names_static, meta_json

| Key | Shape | Dtype |
| --- | --- | --- |
| `x_seq` | `(13112, 20, 24)` | `float32` |
| `x_static` | `(13112, 1)` | `float32` |
| `seq_mask` | `(13112, 20)` | `float32` |
| `missing_mask` | `(13112, 20, 24)` | `float32` |
| `delta_t` | `(13112, 20)` | `float32` |
| `duration` | `(13112,)` | `float32` |
| `event` | `(13112,)` | `int64` |
| `event_type` | `(13112,)` | `int64` |
| `unit_id` | `(13112,)` | `object` |
| `anchor_time` | `(13112,)` | `float32` |
| `dataset_name` | `()` | `<U12` |
| `feature_names_seq` | `(24,)` | `object` |
| `feature_names_static` | `(1,)` | `object` |
| `meta_json` | `()` | `<U419` |

- Has `duration`: yes
- Has `event`: yes
- Has `unit_id`: yes
- Has `anchor_time`: yes
- Has horizon-like key: no
- Meta JSON keys: actual_censored_unit_fraction, adapter, dataset, note, source_type, synthetic_fallback, target_censoring_rate
- Meta JSON summary: actual_censored_unit_fraction=0.30057803468208094, adapter=cmapss_administrative_censoring, dataset=cmapss_fd002, source_type=real_raw_csv, synthetic_fallback=False, target_censoring_rate=0.3

- Selected rows: 300
- Unique source units in sample: 300
- Event counts: observed=246, censored=54
- Original unit sample: test_44, train_36, train_39, train_171, train_88, test_211, test_23, train_159, train_18, test_139...
- Notes: extracted deterministically with seed=0; horizon grid defaulted to [24, 72, 168, 336]; source_frame stores only the file name.

## cmapss_fd003_0_frame.npz

- Source frame: `cmapss_fd003_0_frame.npz`
- Shape: 7562 rows
- Keys: x_seq, x_static, seq_mask, missing_mask, delta_t, duration, event, event_type, unit_id, anchor_time, dataset_name, feature_names_seq, feature_names_static, meta_json

| Key | Shape | Dtype |
| --- | --- | --- |
| `x_seq` | `(7562, 20, 24)` | `float32` |
| `x_static` | `(7562, 1)` | `float32` |
| `seq_mask` | `(7562, 20)` | `float32` |
| `missing_mask` | `(7562, 20, 24)` | `float32` |
| `delta_t` | `(7562, 20)` | `float32` |
| `duration` | `(7562,)` | `float32` |
| `event` | `(7562,)` | `int64` |
| `event_type` | `(7562,)` | `int64` |
| `unit_id` | `(7562,)` | `object` |
| `anchor_time` | `(7562,)` | `float32` |
| `dataset_name` | `()` | `<U12` |
| `feature_names_seq` | `(24,)` | `object` |
| `feature_names_static` | `(1,)` | `object` |
| `meta_json` | `()` | `<U403` |

- Has `duration`: yes
- Has `event`: yes
- Has `unit_id`: yes
- Has `anchor_time`: yes
- Has horizon-like key: no
- Meta JSON keys: actual_censored_unit_fraction, adapter, dataset, note, source_type, synthetic_fallback, target_censoring_rate
- Meta JSON summary: actual_censored_unit_fraction=0.0, adapter=cmapss_administrative_censoring, dataset=cmapss_fd003, source_type=real_raw_csv, synthetic_fallback=False, target_censoring_rate=0.0

- Selected rows: 300
- Unique source units in sample: 200
- Event counts: observed=300, censored=0
- Original unit sample: test_56, train_2, train_85, train_18, test_95, test_77, train_33, test_90, train_15, train_21...
- Notes: extracted deterministically with seed=0; horizon grid defaulted to [24, 72, 168, 336]; source_frame stores only the file name.

## cmapss_fd003_0p3_frame.npz

- Source frame: `cmapss_fd003_0p3_frame.npz`
- Shape: 6533 rows
- Keys: x_seq, x_static, seq_mask, missing_mask, delta_t, duration, event, event_type, unit_id, anchor_time, dataset_name, feature_names_seq, feature_names_static, meta_json

| Key | Shape | Dtype |
| --- | --- | --- |
| `x_seq` | `(6533, 20, 24)` | `float32` |
| `x_static` | `(6533, 1)` | `float32` |
| `seq_mask` | `(6533, 20)` | `float32` |
| `missing_mask` | `(6533, 20, 24)` | `float32` |
| `delta_t` | `(6533, 20)` | `float32` |
| `duration` | `(6533,)` | `float32` |
| `event` | `(6533,)` | `int64` |
| `event_type` | `(6533,)` | `int64` |
| `unit_id` | `(6533,)` | `object` |
| `anchor_time` | `(6533,)` | `float32` |
| `dataset_name` | `()` | `<U12` |
| `feature_names_seq` | `(24,)` | `object` |
| `feature_names_static` | `(1,)` | `object` |
| `meta_json` | `()` | `<U403` |

- Has `duration`: yes
- Has `event`: yes
- Has `unit_id`: yes
- Has `anchor_time`: yes
- Has horizon-like key: no
- Meta JSON keys: actual_censored_unit_fraction, adapter, dataset, note, source_type, synthetic_fallback, target_censoring_rate
- Meta JSON summary: actual_censored_unit_fraction=0.3, adapter=cmapss_administrative_censoring, dataset=cmapss_fd003, source_type=real_raw_csv, synthetic_fallback=False, target_censoring_rate=0.3

- Selected rows: 300
- Unique source units in sample: 200
- Event counts: observed=228, censored=72
- Original unit sample: test_27, test_31, train_60, train_89, test_12, train_20, train_75, test_79, train_34, test_18...
- Notes: extracted deterministically with seed=0; horizon grid defaulted to [24, 72, 168, 336]; source_frame stores only the file name.

## cmapss_fd004_0_frame.npz

- Source frame: `cmapss_fd004_0_frame.npz`
- Shape: 18756 rows
- Keys: x_seq, x_static, seq_mask, missing_mask, delta_t, duration, event, event_type, unit_id, anchor_time, dataset_name, feature_names_seq, feature_names_static, meta_json

| Key | Shape | Dtype |
| --- | --- | --- |
| `x_seq` | `(18756, 20, 24)` | `float32` |
| `x_static` | `(18756, 1)` | `float32` |
| `seq_mask` | `(18756, 20)` | `float32` |
| `missing_mask` | `(18756, 20, 24)` | `float32` |
| `delta_t` | `(18756, 20)` | `float32` |
| `duration` | `(18756,)` | `float32` |
| `event` | `(18756,)` | `int64` |
| `event_type` | `(18756,)` | `int64` |
| `unit_id` | `(18756,)` | `object` |
| `anchor_time` | `(18756,)` | `float32` |
| `dataset_name` | `()` | `<U12` |
| `feature_names_seq` | `(24,)` | `object` |
| `feature_names_static` | `(1,)` | `object` |
| `meta_json` | `()` | `<U403` |

- Has `duration`: yes
- Has `event`: yes
- Has `unit_id`: yes
- Has `anchor_time`: yes
- Has horizon-like key: no
- Meta JSON keys: actual_censored_unit_fraction, adapter, dataset, note, source_type, synthetic_fallback, target_censoring_rate
- Meta JSON summary: actual_censored_unit_fraction=0.0, adapter=cmapss_administrative_censoring, dataset=cmapss_fd004, source_type=real_raw_csv, synthetic_fallback=False, target_censoring_rate=0.0

- Selected rows: 300
- Unique source units in sample: 300
- Event counts: observed=300, censored=0
- Original unit sample: test_33, train_50, test_113, train_126, train_178, test_145, train_106, train_69, train_49, test_107...
- Notes: extracted deterministically with seed=0; horizon grid defaulted to [24, 72, 168, 336]; source_frame stores only the file name.

## cmapss_fd004_0p3_frame.npz

- Source frame: `cmapss_fd004_0p3_frame.npz`
- Shape: 15890 rows
- Keys: x_seq, x_static, seq_mask, missing_mask, delta_t, duration, event, event_type, unit_id, anchor_time, dataset_name, feature_names_seq, feature_names_static, meta_json

| Key | Shape | Dtype |
| --- | --- | --- |
| `x_seq` | `(15890, 20, 24)` | `float32` |
| `x_static` | `(15890, 1)` | `float32` |
| `seq_mask` | `(15890, 20)` | `float32` |
| `missing_mask` | `(15890, 20, 24)` | `float32` |
| `delta_t` | `(15890, 20)` | `float32` |
| `duration` | `(15890,)` | `float32` |
| `event` | `(15890,)` | `int64` |
| `event_type` | `(15890,)` | `int64` |
| `unit_id` | `(15890,)` | `object` |
| `anchor_time` | `(15890,)` | `float32` |
| `dataset_name` | `()` | `<U12` |
| `feature_names_seq` | `(24,)` | `object` |
| `feature_names_static` | `(1,)` | `object` |
| `meta_json` | `()` | `<U419` |

- Has `duration`: yes
- Has `event`: yes
- Has `unit_id`: yes
- Has `anchor_time`: yes
- Has horizon-like key: no
- Meta JSON keys: actual_censored_unit_fraction, adapter, dataset, note, source_type, synthetic_fallback, target_censoring_rate
- Meta JSON summary: actual_censored_unit_fraction=0.29979879275653926, adapter=cmapss_administrative_censoring, dataset=cmapss_fd004, source_type=real_raw_csv, synthetic_fallback=False, target_censoring_rate=0.3

- Selected rows: 300
- Unique source units in sample: 300
- Event counts: observed=236, censored=64
- Original unit sample: train_117, test_166, train_180, train_86, train_55, train_219, train_207, train_243, test_158, test_106...
- Notes: extracted deterministically with seed=0; horizon grid defaulted to [24, 72, 168, 336]; source_frame stores only the file name.

