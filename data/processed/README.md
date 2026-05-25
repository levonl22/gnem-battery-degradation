# Processed data

| File | Grain | Contents |
|------|-------|----------|
| `cycle_summary.csv` | 1 row / cell / cycle | 16 `summary` fields + `cell_id` |
| `cycle_summary_labeled.csv` | same | above + **EOL** + **initial_capacity** |
| `cell_targets.csv` | 1 row / cell | labels only (in `data/`) |

Regenerate:
- `cycle_summary.csv` — `notebooks/03_build_cycle_summary.ipynb`
- `cycle_summary_labeled.csv` — `python scripts/merge_labeled_cycle_summary.py`

Merge keeps **first** row per `cell_id` when targets has duplicate barcodes (Week 2 policy TBD).
