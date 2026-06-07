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

Important limitation:

The main-project adapters currently start from project-prepared CSV files:

- `raw/azure/azure_pdm.csv`
- `raw/scania/scania_survival_samples.csv`
- `raw/cmapss_fd001/cmapss_fd001.csv`
- `raw/cmapss_fd002/cmapss_fd002.csv`
- `raw/cmapss_fd003/cmapss_fd003.csv`
- `raw/cmapss_fd004/cmapss_fd004.csv`

No vendor-raw-to-project-CSV converter for Azure's five PdM files, NASA C-MAPSS text files, or SCANIA Component X upstream files was found in the main project during this export. To avoid inventing new preprocessing behavior, those converters are not recreated here. The exported code preserves the existing CSV-to-frame schema, label construction, anchor construction, and validation behavior.

`scania` means SCANIA Component X-derived survival/time-series data. UCI APS Failure at Scania Trucks is not accepted as the Scania source for these scripts.
