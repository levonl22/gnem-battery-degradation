# Week 4 deliverables (complete)

Cell-level ML baselines on `cell_features.csv` — predict EOL from 44 early-cycle features.

| File | Status |
|------|--------|
| `notebooks/07_ml_baselines.ipynb` | Done |
| `data/processed/cell_split.csv` | Done — 94 / 20 / 20 (`random_state=42`) |
| `results/metrics/*.json` | Done — per-model MAE, RMSE, MAPE |
| Report `05_methods.md` §5.1, `06_results.md` §6.1 | Done |
| `docs/slides/week04_notes.md` | Done |

---

## Setup

```bash
pip install -r requirements.txt   # scikit-learn, xgboost
```

**macOS (XGBoost):** if import fails, `brew install libomp`.

**Run:** `notebooks/07_ml_baselines.ipynb` (top to bottom).  
**Clear outputs before commit:** `jupyter nbconvert --clear-output --inplace notebooks/07_ml_baselines.ipynb`

---

## Split policy

| Set | Cells | Use |
|-----|-------|-----|
| Train | 94 | Fit models |
| Val | 20 | Tune hyperparameters (ElasticNet, RF, XGBoost) |
| Test | 20 | **Final** metrics only |

Split by `file_id` (one row per cell). Saved in `cell_split.csv` for Week 5+.

**Features:** all 44 columns. **Target:** `EOL`. `initial_capacity` excluded from *X*.

---

## Models

| Model | Scaling | Val tuning |
|-------|---------|------------|
| Linear regression | Yes (`StandardScaler`) | None |
| ElasticNet | Yes | `alpha` (1–100), `l1_ratio` |
| Random forest | No | `max_depth`, `min_samples_leaf` |
| XGBoost | No | `max_depth`, `learning_rate` |

---

## Test-set results (holdout)

| Model | MAE (cycles) | RMSE | MAPE (%) |
|-------|-------------|------|----------|
| Linear regression | 133 | 186 | 18.4 |
| ElasticNet | 132 | 147 | 19.3 |
| Random forest | 101 | 132 | 13.3 |
| **XGBoost** | **85** | **108** | **11.0** |

Best val hyperparameters: ElasticNet `alpha≈40`, `l1_ratio=1.0`; RF `max_depth=5`; XGBoost `max_depth=5`, `learning_rate=0.1`.

Tree models rank **ΔV(Q)** and **energy efficiency** features highest (see importance plots). Linear models overfit less obviously on train but generalize worse than trees on this small dataset.

**Caveat:** 20 test cells → metrics have high variance; treat as indicative, not definitive.

---

## Outputs

| Path | Description |
|------|-------------|
| `results/metrics/linear_regression.json` | Linear metrics |
| `results/metrics/elasticnet.json` | ElasticNet metrics + best params |
| `results/metrics/random_forest.json` | RF metrics + best params |
| `results/metrics/xgboost.json` | XGBoost metrics + best params |
| `results/figures/model_comparison_baselines.png` | Test MAE bar chart |
| `results/figures/pred_vs_true_eol_baselines.png` | 2×2 pred vs true (all models) |
| `results/figures/pred_vs_true_eol_*.png` | Per-model pred vs true |
| `results/figures/feature_importance_rf.png` | RF top-15 features |
| `results/figures/feature_importance_xgb.png` | XGBoost top-15 features |

---

## Next

- **Week 5:** LSTM or GRU on `cycle_summary.csv` sequences — same `cell_split.csv`, compare to XGBoost baseline
