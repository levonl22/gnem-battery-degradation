# Week 5 — Google Slides outline

Add these slides to the same deck after Week 4.

---

## Slide 15 — Sequence model setup

**Title:** Week 5 — Predicting EOL from early trajectories

**Bullets:**
- **Input:** `cycle_summary.csv` — first **100 cycles** per cell (`cycle_index` 1–100)
- **Format:** sequence, not a feature table — **100 timesteps × 4 channels** per cell
- **Channels:** SOH (state of health), resistance, energy efficiency, temperature
- **Target:** **EOL** (end of life — cycle at 80% capacity)
- **Split:** same as Week 4 — **94 / 20 / 20** train · val · test (`cell_split.csv`)
- **Metrics:** **MAE** (mean absolute error), **RMSE** (root mean squared error), **MAPE** (mean absolute percentage error) in cycles

**Report & docs:** `docs/week05/README.md` · GitHub `docs/week05`

---

## Slide 16 — GRU sequence model

**Title:** Model — GRU (Gated Recurrent Unit)

**Bullets:**
- **PyTorch** — reads cycles **in order** (1 → 100), updates memory each step, predicts one EOL number
- **Why GRU not LSTM?** Simpler recurrent network; enough for 100 steps and 94 training cells
- **Scaling:** input channels + EOL target (train-only stats); metrics reported in raw cycles
- **Tuning:** 16 hyperparameter combos on **validation MAE** — hidden size, layers, dropout, learning rate
- **Best val settings:** hidden 64, 2 layers, dropout 0.2, learning rate 0.0003

**Notebook:** `notebooks/08_sequence_model.ipynb`

**Not in sequence input:** ΔV(Q) voltage-curve features (Week 3) — those live in raw JSON, not `cycle_summary.csv`

---

## Slide 17 — Test-set results vs XGBoost

**Title:** Test-set EOL error (20 cells) — MAE in cycles

| Model | Test MAE (cycles) |
|-------|-------------------|
| **XGBoost (Week 4)** | **85** |
| GRU sequence (Week 5) | 111 |

**Bullets:**
- GRU **underperforms** best tabular baseline on holdout
- Plausible reasons: only **94** train cells; no ΔV(Q); capacity barely fades in first 100 cycles
- Still a fair **sequence baseline** for Week 6–7 comparisons
- Small test set → indicative, not definitive

**Figure:** `pred_vs_true_eol_sequence.png`

---

## Slide 18 — Week 5 summary & next steps

**Title:** Week 5 complete → Week 6 monotonic SOH

**Bullets:**
- Built reproducible GRU pipeline on per-cycle data; saved metrics (`gru_sequence.json`)
- **Best Week 4 baseline still wins:** XGBoost test MAE **about 85** vs GRU **about 111** cycles
- **Week 6:** monotonic SOH (state of health) constraint — penalize predictions that increase across cycles; compare constrained vs unconstrained curves

---

## Speaker notes (45 sec)

Week 5: instead of 44 summary features, we fed the model the first 100 cycles directly — four signals per cycle: state of health, resistance, energy efficiency, and temperature. We used a GRU, a gated recurrent unit in PyTorch, with the same cell split as Week 4. We tuned 16 hyperparameter combinations on validation mean absolute error. On the 20-cell test holdout, the GRU scored about 111 cycles average error versus 85 for XGBoost. The sequence model doesn't include the voltage-curve features that helped XGBoost, and we only have 94 training batteries, so this is a useful baseline rather than a new best model. Next week: a simple physics-inspired constraint so predicted state of health doesn't increase over time.

---

## Anticipated Q&A (short)

| Question | Answer |
|----------|--------|
| What is a GRU? | A recurrent network that reads a time-ordered sequence and remembers earlier steps. |
| Why worse than XGBoost? | Smaller effective features (4 channels vs 44); no ΔV(Q); small dataset; early cycles have weak capacity fade. |
| Is the comparison fair? | Same split and metrics; not same features — note that in the report. |
| What is SOH? | State of health — current capacity divided by initial capacity. |
| Why scale EOL for training? | Raw EOL is hundreds–thousands; scaling lets the network learn patterns instead of struggling with number size. |
| What is a hyperparameter? | A setting you choose before training (e.g. learning rate), not learned from data. |
