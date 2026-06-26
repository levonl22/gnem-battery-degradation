# Week 3 — Google Slides outline

Add these slides to the same deck after Week 2.

---

## Slide 6 — Feature engineering

**Title:** Week 3 — Early-cycle features

**Bullets:**
- **Input:** first 20 / 50 / 100 cycles per cell (`cycle_index ≥ 1`)
- **Output:** `cell_features.csv` — **134 cells × 44 features** (+ EOL labels)
- **Two sources:**
  - **34 summary features** — capacity, SOH, resistance, energy efficiency, temperature (`cycle_summary.csv`)
  - **10 ΔV(Q) features** — voltage-curve change between cycles 10→50 and 10→100 (Severson-style; raw JSON)
- **Next:** ML baselines on this matrix (Week 4)

**Pipeline (optional diagram):**

```
cycle_summary → notebook 05 ─┐
                             ├→ cell_features.csv (134 × 44)
raw JSON → notebook 04 ──────┘
```

---

## Slide 7 — What is ΔV(Q)? (optional explainer)

**Title:** Voltage-curve change at the same charge removed

**Bullets:**
- **Q:** charge removed during one discharge (about 0–1 Ah per cell ≈ 0–1000 mAh)
- **Y-axis:** voltage **while discharging** (not “voltage discharged”)
- Compare **cycle 10 vs cycle 100** at the **same Q** → shift in curve shape before obvious capacity fade
- **ΔV(Q) = V₁₀₀(Q) − V₁₀(Q)**; we summarize with mean / std / min / max → 10 features

**Figure:** `results/figures/delta_v_q_explainer.png`

**Speaker hint:** One research pouch cell (about 1 Ah). Not pack-level mAh like a 10,000 mAh power bank — same physics, smaller scale.

---

## Slide 8 — Correlation with cycle life

**Title:** Which early features track EOL?

**Bullets:**
- Pearson correlation vs **EOL** on all **134** cells (exploratory; not a trained model yet)
- **Read the EOL row/column** on the heatmap — red = higher feature → longer life; blue → shorter life
- **Strongest links:** ΔV(Q) spread (`delta_v_std_c10_c100`, |r| ≈ 0.8) · energy efficiency (`efficiency_mean_w100`, r ≈ 0.78)
- **Weaker alone:** raw capacity at cycle 100 (|r| ≈ 0.07) — fade is subtle early; curve shape matters more (Severson 2019)
- Many features are **redundant** (bright blocks) → regularization / selection in Week 4

**Figure:** `results/figures/feature_correlation.png`

---

## Slide 9 — Week 3 summary & next steps

**Title:** Week 3 complete → Week 4 ML baselines

**Bullets:**
- Delivered reproducible feature pipeline (notebooks `04`–`06`) and `cell_features.csv`
- Early **efficiency** and **voltage-curve** signals correlate with lifetime more than capacity alone
- **Week 4:** cell-level train/val/test split · Linear · ElasticNet · RF · XGBoost · MAE · pred vs true EOL

---

## Speaker notes (45 sec)

Week 3: built 44 hand-crafted features from the first 100 cycles — summary stats plus Severson-style ΔV(Q) from discharge voltage curves. Correlation screening shows efficiency and voltage-curve change line up with cycle life more than raw capacity fade in the first hundred cycles, which matches the original paper. The heatmap also shows overlapping features, so Week 4 will use regularized models rather than treating every column as independent. Next: train baselines on `cell_features.csv` and report holdout error.

---

## Anticipated Q&A (short)

| Question | Answer |
|----------|--------|
| What is Q? | Charge removed during discharge (Ah); 1 Ah = 1000 mAh. Full cell discharge ≈ 1 Ah here. |
| Why not just capacity? | Capacity fade is weak in first about 100 cycles; curve shape and efficiency shift earlier. |
| Is this an EV pack? | No — single about 1 Ah lab cells; same cell-level idea scales to packs. |
| Can you predict EOL yet? | Not until Week 4 — this slide is univariate screening only. |
