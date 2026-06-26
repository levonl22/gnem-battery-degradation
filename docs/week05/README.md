# Week 5 deliverables (complete)

GRU sequence model on early per-cycle trajectories from `cycle_summary.csv` — predict EOL from the first 100 cycles.

| File | Status |
|------|--------|
| `notebooks/08_sequence_model.ipynb` | Done |
| `data/processed/cell_split.csv` | Reused — 94 / 20 / 20 (`random_state=42`) |
| `results/metrics/gru_sequence.json` | Done |
| `results/figures/pred_vs_true_eol_sequence.png` | Done |
| Report `05_methods.md` §5.2, `06_results.md` §6.2 | Done |
| `docs/slides/week05_notes.md` | Done |

---

## Setup

```bash
pip install -r requirements.txt   # includes torch, scikit-learn, xgboost
```

**Run:** `notebooks/08_sequence_model.ipynb` (top to bottom). Step C grid search (about 16 runs) takes several minutes on CPU.

**Clear outputs before commit:**

```bash
jupyter nbconvert --clear-output --inplace notebooks/08_sequence_model.ipynb
```

---

## Input

Per cell: **100 cycles** (`cycle_index` 1–100, cycle 0 excluded) × **4 channels** from `cycle_summary.csv`:

| Channel | Source |
|---------|--------|
| SOH | `discharge_capacity / initial_capacity` |
| Resistance | `dc_internal_resistance` |
| Energy efficiency | `energy_efficiency` |
| Temperature | `temperature_average` |

Tensor shape: `(134, 100, 4)`. Target: `EOL` (cycles).

**Scaling:** `StandardScaler` on input channels (fit on train timesteps only). EOL target scaled for training (train mean/std); metrics reported in raw cycles.

**Not included:** ΔV(Q) voltage-curve features (from raw JSON in Week 3). XGBoost baseline used those; comparison is not apples-to-apples on features.

---

## Model

**GRU (Gated Recurrent Unit)** in PyTorch — unidirectional, reads cycles in order, predicts EOL from the final hidden state.

| Setting | Value |
|---------|-------|
| Loss | Mean squared error (MSE) on scaled EOL |
| Optimizer | Adam |
| Early stopping | Validation MAE, patience 20, max 200 epochs |
| Batch size | 16 |

**Hyperparameter grid (validation MAE):** hidden size {32, 64}, layers {1, 2}, dropout {0.1, 0.2}, learning rate {0.001, 0.0003} — 16 combinations.

**Best validation params:** hidden size 64, 2 layers, dropout 0.2, learning rate 0.0003.

---

## Test-set results (holdout)

| Model | MAE (cycles) | RMSE | MAPE (%) |
|-------|-------------|------|----------|
| **XGBoost (Week 4)** | **85** | **108** | **11.0** |
| GRU sequence (Week 5) | 111 | 134 | 15.4 |

GRU **underperforms** the XGBoost tabular baseline on test. Plausible reasons: small training set (94 cells), no ΔV(Q) in the sequence input, and limited signal in capacity/resistance over only the first 100 cycles.

**Caveat:** 20 test cells → metrics have high variance; treat as indicative, not definitive.

---

## Outputs

| Path | Description |
|------|-------------|
| `results/metrics/gru_sequence.json` | GRU metrics + best hyperparameters |
| `results/figures/pred_vs_true_eol_sequence.png` | Test-set predicted vs true EOL |

---

## Next

- **Week 6:** Monotonic SOH constraint — compare constrained vs unconstrained trajectories
