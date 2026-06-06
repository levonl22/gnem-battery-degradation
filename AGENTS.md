# AGENTS.md

## Cursor Cloud specific instructions

### Overview

GNEM Battery Degradation Research is a **Python data-science / ML research project** (not a web app). There are no Docker services, databases, or formal lint/test CI. End-to-end validation means running the data pipeline scripts or Jupyter notebooks against committed processed CSVs.

### Python runtime

- Use **`python3`** — there is no `python` symlink on the Cloud VM.
- Install dependencies: `pip install -r requirements.txt` (see root `README.md`).
- Invoke Jupyter via `python3 -m jupyter lab` if the `jupyter` shim is not on `PATH`.

### Running the pipeline

All scripts are run from the **repo root** (`/workspace`):

| Script | Purpose | Raw data required? |
|---|---|---|
| `python3 scripts/merge_labeled_cycle_summary.py` | Merge EOL labels into cycle summary | No (uses committed CSVs) |
| `python3 scripts/generate_week12_figures.py` | Regenerate EDA PNGs in `results/figures/` | No |
| `python3 scripts/rebuild_processed_data.py` | Rebuild from raw JSON | **Yes** — `data/raw/FastCharge*.json` (gitignored; download from [MATR.io](https://data.matr.io/1/projects/5c48dd2bc625d700019f3204)) |

`rebuild_processed_data.py` imports `dedupe_policy` as a sibling module under `scripts/`; do not change the working directory when running it.

### Jupyter Lab (optional)

```bash
python3 -m jupyter lab --no-browser --ip=0.0.0.0 --port=8888
```

Default URL: `http://localhost:8888/lab`. Notebooks `01`–`05` in `notebooks/` follow the pipeline order in `README.md`.

### Validation without raw data

Committed artifacts in `data/processed/` and `data/cell_targets.csv` are sufficient for most development. Quick sanity checks:

```bash
python3 -m py_compile scripts/*.py
python3 scripts/merge_labeled_cycle_summary.py
python3 scripts/generate_week12_figures.py
```

### Optional tooling

- **Pandoc** — PDF report export from `docs/report/` (see `docs/report/README.md`). Not required for pipeline development.
