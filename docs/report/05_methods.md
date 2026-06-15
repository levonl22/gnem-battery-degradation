# 5. Methods

## 5.1 Machine learning baselines

We predict **EOL** (first cycle with `discharge_capacity < 0.8 × initial_capacity`, `cycle_index ≥ 1`) from the Week 3 feature matrix `cell_features.csv`: **134 cells**, **44** early-cycle inputs, target `EOL`. Labels `file_id`, `cell_id`, and `initial_capacity` are excluded from *X*; only `EOL` is the regression target.

**Notebook:** `notebooks/07_ml_baselines.ipynb`. Index: `docs/week04/README.md`.

### Train / validation / test split

All splits are **cell-level** (by `file_id`) so no battery appears in more than one set:

| Set | Cells | Role |
|-----|-------|------|
| Train | 94 (~70%) | Fit model weights |
| Validation | 20 (~15%) | Select hyperparameters |
| Test | 20 (~15%) | Final holdout metrics only |

Split is fixed (`random_state=42`) and saved to `data/processed/cell_split.csv` for reuse in Week 5 (sequence model).

### Models

Four feature-based regressors, increasing capacity:

1. **Linear regression** — ordinary least squares on standardized features (`StandardScaler` + `LinearRegression`).
2. **ElasticNet** — L1/L2-regularized linear model; grid search over `alpha ∈ [1, 100]` and `l1_ratio ∈ {0.1, 0.5, 0.9, 0.95, 1.0}` on validation MAE. Weak penalties below `alpha = 1` were excluded because they failed to converge with 44 correlated features.
3. **Random forest** — `RandomForestRegressor` (300 trees); tune `max_depth` and `min_samples_leaf` on validation MAE. No feature scaling.
4. **XGBoost** — `XGBRegressor` (`objective='reg:squarederror'`, 300 trees, `subsample=0.8`, `colsample_bytree=0.8`); tune `max_depth` and `learning_rate` on validation MAE.

Linear / ElasticNet use a sklearn `Pipeline` with scaling; tree models use raw feature values.

### Evaluation metrics

On each split we report:

- **MAE** — mean absolute error in cycles  
- **RMSE** — root mean squared error (penalizes large misses)  
- **MAPE** — mean absolute percentage error relative to true EOL  

Primary comparison uses **test-set** metrics. Validation is used only for hyperparameter selection; test cells are never used during tuning.

### Feature importance

For random forest and XGBoost we export **gain-based** (XGBoost) and **Gini impurity** (RF) importances for the top features (`results/figures/feature_importance_*.png`).

## 5.2 Sequence model *(Week 5)*

*(To be completed.)*

- LSTM or GRU on early capacity (or voltage) sequences
- Same cell-level split and metrics

## 5.3 Monotonic SOH constraint *(Week 6)*

*(To be completed.)*

- Penalty when predicted SOH increases across cycles
- Compare unconstrained vs constrained trajectories
