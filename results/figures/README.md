# Figures for slides and report

Save notebook exports here as PNG (150–300 dpi). Reference in report as `../../results/figures/name.png`.

## Week 1–2

| File | Description |
|------|-------------|
| `eol_distribution.png` | Histogram of EOL across cells |
| `capacity_fade_example.png` | Single-cell capacity vs cycle with 80% threshold |

Regenerate: `python scripts/generate_week12_figures.py`

## Week 3

| File | Description |
|------|-------------|
| `feature_correlation.png` | Pearson heatmap — 44 features + EOL (134 cells) |

Regenerate: run `notebooks/06_feature_correlation.ipynb`

## Planned (Weeks 4–7)

| Week | Suggested filename |
|------|-------------------|
| 4 | `baseline_mae_comparison.png`, `pred_vs_true_eol_ml.png` |
| 5 | `pred_vs_true_eol_lstm.png` |
| 6 | `soh_curves_constrained.png` |
| 7 | `ablation_early_cycles.png` |

Copy figures into Google Slides each week for check-in.
