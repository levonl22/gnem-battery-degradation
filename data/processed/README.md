# Processed data

| File | Grain | Contents |
|------|-------|----------|
| `cycle_summary.csv` | 1 row / cell / cycle | `file_id`, `cell_id`, 16 `summary` fields |
| `cycle_summary_labeled.csv` | same | above + **EOL** + **initial_capacity** |
| `cell_targets.csv` | 1 row / cell | labels in `data/` (`file_id`, `cell_id`, EOL, initial_capacity) |

**Counts (Week 2 dedupe):** 134 cells · 110,910 cycle rows · 18 columns in `cycle_summary.csv`

Regenerate:
- `cycle_summary.csv` + `data/cell_targets.csv` — `python scripts/rebuild_processed_data.py` or notebooks `01` + `03`
- `cycle_summary_labeled.csv` — `python scripts/merge_labeled_cycle_summary.py`

Policy: `docs/week02/duplicate_barcode_policy.md` (140 raw files → 134 unique barcodes).
