# Porting Notes

The preprocessing code in this folder is exported from the main OCEAN-MO-CDSF project with minimal compatibility edits.

Source files copied from the main project:

- `src/ocean/data/frame.py` -> `frame.py`
- `src/ocean/data/adapters.py` -> `adapters.py`
- `src/ocean/data/builders.py` -> `builders.py`
- `src/ocean/data/splits.py` -> `splits.py`
- `src/ocean/validation/frame_validator.py` -> `frame_validator.py`
- `src/ocean/utils/io.py` -> `io_utils.py`
- `src/ocean/utils/logging.py` -> `logging_utils.py`

Compatibility edits:

- Imports were changed from `ocean.*` package imports to local script-folder imports.
- CLI wrappers accept `--raw-root` and `--out-root` so generated `.npz` files are written outside the sample repository by default.
- Synthetic fallback is not introduced by the wrappers.

Frame-builder inputs:

The main-project adapters currently start from project-prepared CSV files:

- `raw/azure/azure_pdm.csv`
- `raw/scania/scania_survival_samples.csv`
- `raw/cmapss_fd001/cmapss_fd001.csv`
- `raw/cmapss_fd002/cmapss_fd002.csv`
- `raw/cmapss_fd003/cmapss_fd003.csv`
- `raw/cmapss_fd004/cmapss_fd004.csv`

Upstream-to-CSV converters added in this sample-data repository:

- `prepare_azure_pdm_csv.py`
- `prepare_scania_component_x_csv.py`
- `prepare_cmapss_csv.py`
- `prepare_all_csvs.py`
- `upstream_converters.py`

No separate vendor-raw-to-project-CSV converter was found in the main project during the export. The files above were added here to complete the documented reproduction chain from manually downloaded upstream files to project CSV inputs, while keeping that new preparation layer separate from the copied CSV-to-frame code.

The exported frame-builder code preserves the existing CSV-to-frame schema, label construction, anchor construction, and validation behavior.

The SCANIA converter uses the public train split, where `train_tte.csv` supplies observed time-to-event labels. The public validation/test labels are class labels for challenge evaluation, not full per-row survival durations.

`scania` means SCANIA Component X-derived survival/time-series data. UCI APS Failure at Scania Trucks is not accepted as the Scania source for these scripts.
