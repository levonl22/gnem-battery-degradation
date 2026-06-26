# Week 6 — Google Slides outline

Add these slides to the same deck after Week 5.

---

## Slide 19 — Monotonic SOH motivation

**Title:** Week 6 — Physics-informed SOH constraint

**Bullets:**
- **SOH (state of health)** = current capacity ÷ initial capacity — should **not increase** cycle-to-cycle in a degrading cell
- Week 5 GRU predicts **EOL only** — no explicit health **curve** to inspect
- **Week 6 goal:** dual-head GRU predicts **EOL + SOH at each cycle**; add a **monotonic penalty** when predicted SOH goes up
- Light regularizer — **not** a full physics-informed neural network (PINN)
- Same split as Weeks 4–5: **94 / 20 / 20** (`cell_split.csv`)

**Report & docs:** `docs/week06/README.md` · GitHub `docs/week06`

---

## Slide 20 — Dual-head GRU + loss

**Title:** Model — unconstrained vs constrained

**Bullets:**
- **Input:** same as Week 5 — 100 cycles × 4 channels (SOH, resistance, efficiency, temperature)
- **Two outputs:** (1) **EOL** — one number per cell; (2) **SOH trajectory** — 100 values per cell
- **Unconstrained loss:** EOL error + **α × SOH reconstruction error** (α = 0.1)
- **Constrained loss:** add **λ × monotonic penalty** — penalize SOH(t+1) > SOH(t)
- **λ grid:** {0.01, 0.1, 1.0} — pick best **validation EOL MAE**
- GRU settings fixed at Week 5 best (hidden 64, 2 layers, dropout 0.2, lr 0.0003)

**Notebook:** `notebooks/09_monotonic_soh.ipynb`

---

## Slide 21 — Test-set results

**Title:** EOL error and SOH violations (test set, 20 cells)

| Model | Test MAE (cycles) | SOH violation rate (%) |
|-------|-------------------|------------------------|
| **XGBoost (Week 4)** | **85** | — |
| GRU unconstrained | 112 | 60.6 |
| GRU constrained (λ = 1.0) | 112 | 60.2 |

**Bullets:**
- **EOL MAE unchanged** — constrained ≈ unconstrained (about 112 cycles); penalty mainly shapes SOH head
- **Violations drop slightly** (about 0.4 pp on test) — weak penalty; curves still jagged
- **XGBoost still best** on EOL — no new features (no ΔV(Q)); constraint ≠ feature upgrade
- Small test set → indicative, not definitive

**Figures:** `soh_curves_constrained.png` · `model_comparison_soh_penalty.png`

---

## Slide 22 — Week 6 summary & next steps

**Title:** Week 6 complete → Week 7 ablations

**Bullets:**
- Built dual-head GRU pipeline; saved metrics (`gru_unconstrained.json`, `gru_monotonic.json`)
- Monotonic penalty **does not hurt EOL** but **barely improves** curve plausibility at tested λ
- **Best EOL model remains XGBoost** (about 85 cycles test MAE)
- **Week 7:** early-cycle window ablation — *N* = **20**, **50**, **100** cycles

---

## Speaker notes (45 sec)

Week 6 added a second output to the GRU: predicted state of health at every cycle, not just end-of-life. We trained an unconstrained model and a constrained model with a penalty when predicted health increases from one cycle to the next — a simple physics-inspired nudge. We tried three penalty strengths and picked the best on validation mean absolute error. On the test holdout, end-of-life error stayed around 112 cycles for both versions, almost the same as Week 5. The violation rate — how often the curve ticks upward — dropped only slightly, about half a percent. XGBoost at 85 cycles is still the best predictor because it uses richer features like voltage-curve statistics that the sequence model does not see. Next week we ablate how many early cycles are needed.

---

## Anticipated Q&A (short)

| Question | Answer |
|----------|--------|
| What is a monotonic constraint? | Predicted SOH should be non-increasing over time — no upward steps. |
| Why similar EOL for both GRUs? | Training optimizes EOL; penalty only lightly touches the SOH curve. |
| Why not beat XGBoost? | Same 4-channel input as Week 5; no ΔV(Q); 94 train cells; penalty adds no new signal. |
| What is λ? | Weight on the monotonic penalty term in the loss. |
| Was tuning pointless? | λ tuning was the point for Week 6; beating XGBoost was not. |
| What is a violation? | A consecutive cycle pair where predicted SOH increases. |
