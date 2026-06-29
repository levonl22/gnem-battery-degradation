# Week 7 deliverables (complete)

**Early-cycle window ablation** — how much data from the first *N* cycles is needed for stable EOL prediction?

| File | Status |
|------|--------|
| `notebooks/10_early_cycle_ablation.ipynb` | Done |
| `scripts/run_gru_ablation.py` | Done — GRU grid runs in subprocess (see Step C notes in notebook) |
| `data/processed/cell_split.csv` | Reused — 94 / 20 / 20 (`random_state=42`) |
| `results/metrics/xgboost_n{20,50,100}.json` | Done |
| `results/metrics/gru_sequence_n{20,50,100}.json` | Done |
| `results/figures/ablation_early_cycles.png` | Done |
| Report `05_methods.md` §5.4, `06_results.md` §6.4, `07_discussion.md` | Done |
| `docs/slides/week07_notes.md` | Done |

---

## Setup

```bash
pip install -r requirements.txt   # includes torch, scikit-learn, xgboost
```

**Run:** `notebooks/10_early_cycle_ablation.ipynb` (top to bottom).

- **Step B** — XGBoost loop in notebook (~1 min on CPU).
- **Step C** — GRU via `scripts/run_gru_ablation.py` subprocess (48 training jobs; several minutes on CPU). Smoke test first: `python scripts/run_gru_ablation.py --smoke-test`.
- **Step D** — combined summary table + `ablation_early_cycles.png`.

**Clear outputs before commit:**

```bash
python -c "
import nbformat
from nbformat.validator import normalize
p = 'notebooks/10_early_cycle_ablation.ipynb'
nb = nbformat.read(p, as_version=4)
for c in nb.cells:
    c.outputs = []
    c.execution_count = None
normalize(nb)
nbformat.write(nb, open(p, 'w'))
"
```

(`jupyter nbconvert --clear-output` may fail on stream outputs missing a `name` field.)

---

## Question

If you can only observe the first **N** cycles, how well can you predict EOL?

We repeat training at **N ∈ {20, 50, 100}** with the same split and metrics as Weeks 4–6.

---

## Feature rules (XGBoost)

From `features_for_window(n)` in the notebook — only columns computable from cycles 1…*N*:

| N | Features | ΔV(Q) |
|---|----------|-------|
| 20 | 12 | No |
| 50 | 28 | c10→c50 pair only |
| 100 | 44 | c10→c50 + c10→c100 (same as Week 4) |

At **N = 100**, XGBoost should match Week 4 (about **85** cycles test MAE).

---

## Models

| Model | Input at window *N* | Tuning |
|-------|---------------------|--------|
| **XGBoost** | Subset of `cell_features.csv` | Same grid as Week 4 (`max_depth`, `learning_rate`) on **validation MAE** |
| **GRU** (Week 5 single-head) | First *N* cycles × 4 channels from `cycle_summary.csv` | Same 16-combo grid as Week 5 on **validation MAE** |

Week 6 monotonic dual-head GRU is **out of scope**.

GRU training runs in **`scripts/run_gru_ablation.py`** (subprocess) to avoid Jupyter kernel stale-code / thread issues on Mac — see notebook Step C troubleshooting.

---

## Test-set results (holdout, *n* = 20 cells)

### EOL prediction (MAE in cycles)

| N | XGBoost MAE | GRU MAE |
|---|-------------|---------|
| 20 | 167 | 144 |
| 50 | 107 | 143 |
| 100 | **85** | 110 |

Full metrics (RMSE, MAPE) in `results/metrics/*.json` and notebook Step D.

At **N = 100**: XGBoost **85** matches Week 4; GRU **110** matches Week 5 (about **111**).

---

## Interpretation

- **XGBoost gains a lot from longer windows** — especially ΔV(Q) features at *N* ≥ 50. Test MAE drops from about 167 → 107 → 85 cycles.
- **GRU is flat from 20 → 50** (about 144 → 143 MAE), then improves at 100 (about 110). The sequence model may need more timesteps before the recurrent structure pays off on this small dataset.
- **At N = 20 only**, GRU beats XGBoost (about 144 vs 167) — tabular model loses voltage-curve summaries entirely; GRU still sees per-cycle SOH/resistance/efficiency/temperature.
- **At N = 100**, XGBoost remains best (about 85 vs about 110 cycles) — same gap as Weeks 4–5.

**Caveat:** 20 test cells → metrics have high variance.

---

## Outputs

| Path | Description |
|------|-------------|
| `results/metrics/xgboost_n20.json` | XGBoost, 12 features |
| `results/metrics/xgboost_n50.json` | XGBoost, 28 features |
| `results/metrics/xgboost_n100.json` | XGBoost, 44 features (Week 4 equivalent) |
| `results/metrics/gru_sequence_n20.json` | GRU, sequence length 20 |
| `results/metrics/gru_sequence_n50.json` | GRU, sequence length 50 |
| `results/metrics/gru_sequence_n100.json` | GRU, sequence length 100 |
| `results/figures/ablation_early_cycles.png` | Grouped bar chart — test MAE vs *N* |

---

## Next

- **Week 8:** merge report PDF, final slides deck (10–15 slides), repo polish
