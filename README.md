# GNEM Battery Degradation Research

ML-based prediction of lithium-ion battery cycle life using early-cycle data.

## Dataset
MIT-Stanford-Toyota battery dataset from:
- Severson et al. (2019). "Data-driven prediction of battery cycle life before capacity degradation." *Nature Energy*, 4, 383-391.
- DOI: 10.1038/s41560-019-0356-8
- Data: https://data.matr.io/1/projects/5c48dd2bc625d700019f3204

## Project layout

```
data/raw/              # JSON per cell (gitignored)
data/processed/        # cycle_summary.csv, cell_features.csv, etc.
data/cell_targets.csv  # EOL labels
docs/week01/           # Week 1 deliverables
docs/week02/           # Week 2 (dedupe policy)
docs/week03/           # Week 3 (features, correlation)
docs/week04/           # Week 4 (ML baselines)
docs/week05/           # Week 5 (GRU sequence model)
docs/report/           # Report sections (merge Week 8)
docs/slides/           # Google Slides outlines
notebooks/01_...       # EOL extraction
notebooks/02_...       # Inspect one JSON
notebooks/03_...       # cycle_summary export
notebooks/04_...       # voltage ΔV(Q) features
notebooks/05_...       # cell_features merge
notebooks/06_...       # correlation vs EOL
notebooks/07_...       # ML baselines (Week 4)
notebooks/08_...       # GRU sequence model (Week 5)
results/figures/       # PNGs for slides + report
scripts/               # figure generation, utilities
```

## How to run

1. Place raw JSON in `data/raw/` (FastCharge*.json).
2. Run notebooks in order: `01` → `08` (`02` optional inspection).
3. Rebuild cleaned CSVs (after raw data change): `python scripts/rebuild_processed_data.py`
4. Regenerate Week 1–2 figures: `python scripts/generate_week12_figures.py`
5. ΔV(Q) explainer figure: `python scripts/generate_delta_v_explainer_figure.py`
6. Merge labels into cycle summary: `python scripts/merge_labeled_cycle_summary.py`
7. Report sections: `docs/report/` (merge to PDF in Week 8 via pandoc or Word).
8. **After each week (post-push):** `./scripts/create_week_backup.sh N` → local snapshot at `../gnem-battery-degradation-weekN-backup` (no raw JSON).

Install: `pip install -r requirements.txt`

## Project status

Week 5 complete: GRU sequence model on first 100 cycles of `cycle_summary.csv` (4 channels per cycle). Test MAE **~111 cycles** vs XGBoost **~85 cycles** (Week 4). Index: `docs/week05/README.md`.

**Next (Week 6):** Monotonic SOH constraint — constrained vs unconstrained degradation curves.
