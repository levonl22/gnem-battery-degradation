# Week 6 deliverables (complete)

Dual-head GRU with a **monotonic SOH (state of health) penalty** — compare unconstrained vs constrained predicted health curves and EOL error.

| File | Status |
|------|--------|
| `notebooks/09_monotonic_soh.ipynb` | Done |
| `data/processed/cell_split.csv` | Reused — 94 / 20 / 20 (`random_state=42`) |
| `results/metrics/gru_unconstrained.json` | Done |
| `results/metrics/gru_monotonic.json` | Done |
| `results/figures/soh_curves_constrained.png` | Done |
| `results/figures/model_comparison_soh_penalty.png` | Done |
| Report `05_methods.md` §5.3, `06_results.md` §6.3 | Done |
| `docs/slides/week06_notes.md` | Done |

---

## Setup

```bash
pip install -r requirements.txt   # includes torch, scikit-learn, xgboost
```

**Run:** `notebooks/09_monotonic_soh.ipynb` (top to bottom). Steps B–C train several GRU models (about 1–2 min on CPU).

**Clear outputs before commit:**

```bash
jupyter nbconvert --clear-output --inplace notebooks/09_monotonic_soh.ipynb
```

---

## Input

Same as Week 5: per cell **100 cycles** (`cycle_index` 1–100) × **4 channels** from `cycle_summary.csv` (SOH, resistance, energy efficiency, temperature). Target: **EOL** (cycles).

Additionally, **true SOH trajectories** (unscaled, 0–1) train the SOH output head.

---

## Model

**Dual-head GRU** — extends Week 5 with a second output:

| Head | Output |
|------|--------|
| EOL | One number per cell (from final timestep) |
| SOH | One health value per cycle (100 values per cell) |

**GRU hyperparameters:** fixed at Week 5 best — hidden 64, 2 layers, dropout 0.2, learning rate 0.0003.

| Setting | Value |
|---------|-------|
| EOL loss | MSE on scaled EOL |
| SOH loss | MSE on true SOH (weight **α = 0.1**) |
| Monotonic penalty | Average ReLU(SOH(t+1) − SOH(t)); weight **λ** |
| Early stopping | Validation **EOL MAE**, patience 20, max 200 epochs |
| Batch size | 16 |

**λ grid (validation EOL MAE):** {0.01, 0.1, 1.0}. Best: **λ = 1.0**.

**Unconstrained:** λ = 0 (EOL + SOH losses only).

---

## Test-set results (holdout)

### EOL prediction (MAE in cycles)

| Model | MAE | RMSE | MAPE (%) |
|-------|-----|------|----------|
| **XGBoost (Week 4)** | **85** | **108** | **11.0** |
| GRU unconstrained (Week 6) | 112 | 134 | 15.9 |
| GRU constrained (λ = 1.0) | 112 | 134 | 15.9 |

### SOH monotonic violations (test set)

Fraction of consecutive cycle pairs where **predicted SOH increases**:

| Model | Violation rate (%) |
|-------|-------------------|
| Unconstrained | 60.6 |
| Constrained (λ = 1.0) | 60.2 |

---

## Interpretation

- **EOL barely changes** between unconstrained and constrained models (about 112 cycles test MAE both). Training and early stopping prioritize EOL; the monotonic penalty only lightly shapes the SOH curve.
- **Violations drop slightly** at λ = 1.0 (about 0.4 percentage points on test) — the penalty is too weak to produce clearly smoother trajectories.
- **XGBoost still best** on EOL (about 85 vs about 112 cycles). Week 6 did not add new input features (no ΔV(Q)); the constraint is a regularizer, not a feature upgrade.

**Caveat:** 20 test cells → metrics have high variance.

---

## Outputs

| Path | Description |
|------|-------------|
| `results/metrics/gru_unconstrained.json` | Dual-head GRU, λ = 0 |
| `results/metrics/gru_monotonic.json` | Dual-head GRU, best λ + grid results |
| `results/figures/soh_curves_constrained.png` | Example test-set SOH curves (true vs both models) |
| `results/figures/model_comparison_soh_penalty.png` | Test MAE — XGBoost vs unconstrained vs constrained |

---

## Next

- **Week 7:** Early-cycle window ablations (*N* = 20, 50, 100 cycles)
