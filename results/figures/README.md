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

## Week 4

| File | Description |
|------|-------------|
| `model_comparison_baselines.png` | Test MAE bar chart — all four models |
| `pred_vs_true_eol_baselines.png` | 2×2 pred vs true EOL (test set) |
| `pred_vs_true_eol_linear.png` | Linear regression |
| `pred_vs_true_eol_elasticnet.png` | ElasticNet |
| `pred_vs_true_eol_random_forest.png` | Random forest |
| `pred_vs_true_eol_xgboost.png` | XGBoost |
| `feature_importance_rf.png` | RF top-15 features |
| `feature_importance_xgb.png` | XGBoost top-15 features |

Regenerate: run `notebooks/07_ml_baselines.ipynb`

## Planned (Weeks 5–7)

| Week | Suggested filename |
|------|-------------------|
| 5 | `pred_vs_true_eol_sequence.png` |
| 6 | `soh_curves_constrained.png` |
| 7 | `ablation_early_cycles.png` |

Copy figures into Google Slides each week for check-in.
