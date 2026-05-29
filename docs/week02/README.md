# Week 2 deliverables (complete)

| File | Status |
|------|--------|
| `duplicate_barcode_policy.md` | Done — longest-run-wins dedupe → 134 cells |
| Report `03_data.md` | Updated (cleaned counts, EDA) |
| `docs/slides/week02_notes.md` | Done — cleaning + EDA slides |

## Data (after Week 2 cleaning)

| Artifact | Rows | Notes |
|----------|------|--------|
| `data/cell_targets.csv` | 134 | `file_id`, `cell_id`, `EOL`, `initial_capacity` |
| `data/processed/cycle_summary.csv` | 110,910 | `file_id` + `cell_id` + 16 summary fields |
| `data/processed/cycle_summary_labeled.csv` | 110,910 | merge on `file_id` |

**Rebuild:** `python scripts/rebuild_processed_data.py` (requires `data/raw/`).  
**Figures:** `python scripts/generate_week12_figures.py`

## Also completed (mostly started in Week 1)

- EOL histogram + capacity fade plots (`results/figures/`)
- EDA narrative in report §3.3

## Next: Week 3

Early-cycle features → `cell_features.csv` (not started).
