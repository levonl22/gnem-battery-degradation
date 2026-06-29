# 5. Methods

## 5.1 Machine learning baselines

We predict **EOL** (first cycle with `discharge_capacity < 0.8 × initial_capacity`, `cycle_index ≥ 1`) from the Week 3 feature matrix `cell_features.csv`: **134 cells**, **44** early-cycle inputs, target `EOL`. Labels `file_id`, `cell_id`, and `initial_capacity` are excluded from *X*; only `EOL` is the regression target.

**Notebook:** `notebooks/07_ml_baselines.ipynb`. Index: `docs/week04/README.md`.

### Train / validation / test split

All splits are **cell-level** (by `file_id`) so no battery appears in more than one set:

| Set | Cells | Role |
|-----|-------|------|
| Train | 94 (about 70%) | Fit model weights |
| Validation | 20 (about 15%) | Select hyperparameters |
| Test | 20 (about 15%) | Final holdout metrics only |

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

## 5.2 Sequence model

We predict **EOL** from **per-cycle trajectories** in `cycle_summary.csv` rather than the Week 3 feature matrix. Each cell contributes a sequence of length **N = 100** (cycles with `cycle_index` 1–100; cycle 0 excluded) and **four channels**: state-of-health (SOH = `discharge_capacity / initial_capacity`), `dc_internal_resistance`, `energy_efficiency`, and `temperature_average`. Tensor shape per split: (*n* cells, 100 timesteps, 4 channels). Target: `EOL` in cycles.

**Notebook:** `notebooks/08_sequence_model.ipynb`. Index: `docs/week05/README.md`.

**Split:** identical to §5.1 (`data/processed/cell_split.csv`, 94 / 20 / 20, `random_state=42`).

### Preprocessing

1. **Input scaling** — `StandardScaler` on the four channels, fit on all timesteps from **train cells only**, applied to val and test.
2. **Target scaling** — EOL is standardized using train mean and standard deviation for the training loss; predictions are converted back to cycles before MAE / RMSE / MAPE.

Voltage-curve **ΔV(Q)** features (Week 3) are **not** included—they are derived from raw JSON, not `cycle_summary.csv`. The Week 4 XGBoost baseline used them; sequence-vs-tabular comparison therefore differs in input information as well as model class.

### Model

**GRU (Gated Recurrent Unit)** regressor in PyTorch: unidirectional GRU (`batch_first=True`) reads timesteps in order; the final hidden state passes through dropout and a linear head to predict scaled EOL.

| Setting | Value |
|---------|-------|
| Loss | Mean squared error on scaled EOL |
| Optimizer | Adam |
| Batch size | 16 |
| Early stopping | Validation MAE, patience 20, max 200 epochs |

### Hyperparameter selection

Grid search on **validation MAE** over 16 combinations:

- Hidden size ∈ {32, 64}
- Layers ∈ {1, 2}
- Dropout ∈ {0.1, 0.2}
- Learning rate ∈ {0.001, 0.0003}

Best validation settings: hidden size 64, 2 layers, dropout 0.2, learning rate 0.0003. Test-set metrics are reported once using this configuration; test cells are not used during tuning.

### Evaluation metrics

Same as §5.1: **MAE**, **RMSE**, and **MAPE** on train, validation, and test splits (errors in cycles).

## 5.3 Monotonic SOH constraint

We extend the Week 5 GRU with a **dual-head** architecture that predicts both **EOL** and a **per-cycle SOH trajectory**, then compare **unconstrained** training to training with a **monotonic SOH penalty**—a light physics-informed regularizer, not a full physics-informed neural network (PINN).

**Notebook:** `notebooks/09_monotonic_soh.ipynb`. Index: `docs/week06/README.md`.

**Split and preprocessing:** identical to §5.2 (`cell_split.csv`, 94 / 20 / 20; input and EOL target scaling as in §5.2). True SOH trajectories (unscaled, capacity ÷ initial capacity) supervise the SOH head.

### Dual-head model

The backbone is the same unidirectional GRU as §5.2 (hidden size 64, 2 layers, dropout 0.2, learning rate 0.0003—fixed at Week 5 best settings). Two linear heads read GRU hidden states:

1. **EOL head** — final timestep hidden state → scaled EOL (scalar per cell).
2. **SOH head** — hidden state at **each** timestep → predicted SOH at cycles 1–100.

### Loss functions

**Unconstrained** (λ = 0): mean squared error (MSE) on scaled EOL plus **α = 0.1** times MSE on the SOH trajectory. The SOH term teaches the second head to match observed health curves; EOL remains the primary objective.

**Constrained** (λ > 0): add **λ** times a **monotonic penalty**—the batch mean of ReLU(predicted SOH at *t*+1 minus predicted SOH at *t*). The penalty is non-zero only when predicted SOH **increases** from one cycle to the next.

| Setting | Value |
|---------|-------|
| Optimizer | Adam |
| Batch size | 16 |
| Early stopping | Validation **EOL MAE**, patience 20, max 200 epochs |
| SOH loss weight α | 0.1 |
| Monotonic weight λ | Grid {0.01, 0.1, 1.0}; select by validation EOL MAE |

### Hyperparameter selection

We grid-search **λ** on validation EOL MAE while holding GRU architecture and α fixed. Test-set metrics and SOH violation rates are reported once using the best λ; test cells are not used during tuning.

### Evaluation metrics

**EOL:** same as §5.1 — MAE, RMSE, MAPE in cycles on train, validation, and test.

**SOH plausibility:** count and rate of **monotonic violations**—consecutive cycle pairs where predicted SOH increases. Reported per split as violations ÷ (cells × 99 cycle pairs).

Example SOH trajectories (true vs unconstrained vs constrained) are plotted for test cells with the highest unconstrained violation counts.

## 5.4 Early-cycle window ablation

We ask how much early-cycle data is required for stable EOL prediction by retraining at window lengths **N ∈ {20, 50, 100}** with the same cell-level split as §5.1–§5.3.

**Notebook:** `notebooks/10_early_cycle_ablation.ipynb`. Index: `docs/week07/README.md`.

**Split:** `data/processed/cell_split.csv` (94 / 20 / 20, `random_state=42`).

### Tabular model (XGBoost)

For each *N*, we subset `cell_features.csv` to columns computable from cycles 1…*N* only (`features_for_window`):

| N | Feature count | ΔV(Q) included |
|---|---------------|----------------|
| 20 | 12 | No |
| 50 | 28 | c10→c50 pair |
| 100 | 44 | c10→c50 and c10→c100 (Week 4 full set) |

Hyperparameter grid and evaluation match §5.1 (validation MAE for `max_depth` and `learning_rate`; test metrics once per *N*).

### Sequence model (GRU)

For each *N*, we build tensors (*n* cells, *N* timesteps, 4 channels) from `cycle_summary.csv`—same four channels as §5.2 (SOH, resistance, energy efficiency, temperature). Hyperparameter grid (16 combinations) and early stopping match §5.2; best combo selected on validation MAE per window.

GRU training runs via `scripts/run_gru_ablation.py` in a fresh Python subprocess to avoid Jupyter kernel stale definitions and Mac PyTorch/OpenMP threading issues (documented in the notebook).

Week 6 dual-head monotonic GRU is **not** included; this ablation varies input window only.

### Evaluation metrics

Same as §5.1: **MAE**, **RMSE**, **MAPE** on train, validation, and test. Primary comparison uses **test-set** MAE across *N* and model type. At *N* = 100, results should align with Week 4 XGBoost and Week 5 GRU baselines within rounding.
