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
docs/week06/           # Week 6 (monotonic SOH constraint)
docs/week07/           # Week 7 (early-cycle ablation)
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
notebooks/09_...       # Monotonic SOH constraint (Week 6)
notebooks/10_...       # Early-cycle ablation (Week 7)
docs/week06/           # Week 6 (dual-head GRU, monotonic penalty)
docs/week07/           # Week 7 (early-cycle window ablation)
results/figures/       # PNGs for slides + report
scripts/               # figure generation, utilities
```

## How to run

1. Place raw JSON in `data/raw/` (FastCharge*.json).
2. Run notebooks in order: `01` → `10` (`02` optional inspection).
3. Rebuild cleaned CSVs (after raw data change): `python scripts/rebuild_processed_data.py`
4. Regenerate Week 1–2 figures: `python scripts/generate_week12_figures.py`
5. ΔV(Q) explainer figure: `python scripts/generate_delta_v_explainer_figure.py`
6. Merge labels into cycle summary: `python scripts/merge_labeled_cycle_summary.py`
7. Report sections: `docs/report/` (merge to PDF in Week 8 via pandoc or Word).

Install: `pip install -r requirements.txt`

## Project status

Week 7 complete: early-cycle window ablation at *N* = 20, 50, 100 cycles. XGBoost test MAE improves from about **167** → **107** → **85** cycles; GRU is flat at 20–50 (about **144** MAE) then about **110** at *N* = 100. XGBoost still best at full window. Index: `docs/week07/README.md`.

**Next (Week 8):** Final report PDF, slides deck polish (10–15 slides), repo cleanup.
