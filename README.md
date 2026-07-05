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
docs/week01/ … week08/ # Weekly deliverables (week08 = final wrap-up)
docs/report/           # Report sections §01–09
docs/slides/           # Final deck notes + weekly outlines
notebooks/01_ … 10_    # Pipeline (01 → 10; 02 optional)
results/figures/       # PNGs for report, slides, poster
results/metrics/       # Model metrics JSON
results/               # gnem_battery_report.pdf, slides PDF, showcase poster PDF
scripts/               # Data rebuild, figures, poster/slide helpers
```

## How to run

1. Place raw JSON in `data/raw/` (FastCharge*.json).
2. Run notebooks in order: `01` → `10` (`02` optional inspection).
3. Rebuild cleaned CSVs (after raw data change): `python scripts/rebuild_processed_data.py`
4. Regenerate Week 1–2 figures: `python scripts/generate_week12_figures.py`
5. ΔV(Q) explainer figure: `python scripts/generate_delta_v_explainer_figure.py`
6. Merge labels into cycle summary: `python scripts/merge_labeled_cycle_summary.py`

Install: `pip install -r requirements.txt` (pins **xgboost 2.x** so Week 4–7 metrics reproduce; 3.x changes grid-search winners and test MAE).

## Project status

**Week 8 complete (GNEM fellowship wrap-up).** Eight-week pipeline from raw JSON to report, slides, and showcase poster.

**Best holdout model:** XGBoost at *N* = 100 early cycles — about **85 cycles** test MAE (about **11%** MAPE, 20 test cells). Week 7 ablation: XGBoost **167 → 107 → 85** cycles MAE as the window grows from 20 to 100 cycles.

**Final artifacts:** `results/gnem_battery_report.pdf` · `results/gnem_battery_slides.pdf` · `results/LAU_gnem_battery_poster.pdf`

Index: `docs/week08/README.md`
