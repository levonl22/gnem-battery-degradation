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
data/processed/        # cycle_summary.csv, etc.
data/cell_targets.csv  # EOL labels
docs/week01/           # Week 1 deliverables
docs/week02/           # Week 2 (dedupe policy)
docs/report/           # Report sections (merge Week 8)
docs/slides/           # Google Slides outlines
notebooks/01_...       # EOL extraction
notebooks/02_...       # Inspect one JSON
notebooks/03_...       # cycle_summary export
results/figures/       # PNGs for slides + report
scripts/               # figure generation, utilities
```

## How to run

1. Place raw JSON in `data/raw/` (FastCharge*.json).
2. Run notebooks in order: `01` → `03` (02 optional inspection).
3. Rebuild cleaned CSVs (after raw data change): `python scripts/rebuild_processed_data.py`
4. Regenerate Week 1–2 figures: `python scripts/generate_week12_figures.py`
5. Merge labels into cycle summary: `python scripts/merge_labeled_cycle_summary.py`
6. Report sections: `docs/report/` — see `docs/report/README.md` for PDF export.

Install: `pip install -r requirements.txt`

## Project Status

Week 2 complete: 134 cells, cycle_summary (~111k rows), dedupe policy, report §3, EDA figures. Week 3: features.

