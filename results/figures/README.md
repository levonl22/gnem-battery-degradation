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

## Week 5

| File | Description |
|------|-------------|
| `pred_vs_true_eol_sequence.png` | GRU test-set predicted vs true EOL |

Regenerate: run `notebooks/08_sequence_model.ipynb`

## Week 6

| File | Description |
|------|-------------|
| `soh_curves_constrained.png` | Example test-set SOH trajectories (true vs unconstrained vs constrained) |
| `model_comparison_soh_penalty.png` | Test MAE — XGBoost vs unconstrained vs constrained GRU |

Regenerate: run `notebooks/09_monotonic_soh.ipynb`

## Week 7

| File | Description |
|------|-------------|
| `ablation_early_cycles.png` | Test MAE vs early-cycle window N — XGBoost vs GRU (N = 20, 50, 100) |

Regenerate: run `notebooks/10_early_cycle_ablation.ipynb` (Step D)

## Week 8 (poster)

| File | Description |
|------|-------------|
| `feature_correlation_poster.png` | Top 12 features + EOL — readable heatmap for showcase poster |
| `github_qr.png` | QR code → GitHub repo |

Regenerate: `python scripts/generate_poster_heatmap.py` (heatmap) · QR via `qrcode` (see `scripts/generate_poster.py` workflow in `docs/week08/README.md`)

Copy figures into Google Slides each week for check-in.
