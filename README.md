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
data/processed/        # CSV tables built from notebooks
docs/week01/           # Week 1 written deliverables
notebooks/01_...         # Bulk EOL extraction
notebooks/02_...         # Inspect one JSON file (json.load)
```

## Project Status

Week 1: EOL + initial capacity extracted; inspect one cell in `02_inspect_one_cell.ipynb`; fill in `docs/week01/`

