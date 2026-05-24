# Processed data

CSV files built from `data/raw/*.json`. Safe to regenerate by re-running notebooks.

| File | Grain | Created by |
|------|-------|------------|
| `cell_targets.csv` | 1 row = 1 cell | `01_data_exploration.ipynb` |
| `cycle_summary.csv` | 1 row = 1 cell × 1 cycle | `03_build_cycle_summary.ipynb` *(coming)* |

Do not commit huge exports of `cycles_interpolated`; extract features in Week 3 instead.
