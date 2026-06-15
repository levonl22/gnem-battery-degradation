# Week 4 — Google Slides outline

Add these slides to the same deck after Week 3.

---

## Slide 10 — ML baseline setup

**Title:** Week 4 — Predicting EOL from early features

**Bullets:**
- **Input:** `cell_features.csv` — 134 cells × **44 features** (Week 3)
- **Target:** **EOL** (cycle at 80% capacity)
- **Split:** cell-level **~70 / 15 / 15** (**94 / 20 / 20** train · val · test, `random_state=42`) — not row-level
- **Val** = pick model settings · **Test** = final score (untouched during tuning)
- **Metrics:** MAE, RMSE, MAPE (cycles)

**Report & docs:** `docs/week04/README.md` · GitHub `docs/week04`

---

## Slide 11 — Four baseline models

**Title:** Models trained

**Bullets:**
- **Linear regression** — simple reference
- **ElasticNet** — regularized linear (correlated ΔV features)
- **Random forest** — nonlinear trees + feature importance
- **XGBoost** — gradient-boosted trees (strong tabular baseline)

**Notebook:** `notebooks/07_ml_baselines.ipynb`

---

## Slide 12 — Test-set results

**Title:** Test-set EOL error (20 cells) — MAE in cycles

| Model | Test MAE (cycles) |
|-------|-------------------|
| Linear | 133 |
| ElasticNet | 132 |
| Random forest | 101 |
| **XGBoost** | **85** |

**Bullets:**
- Tree models beat linear baselines on holdout
- Typical error **~85–130 cycles** (~11–19% MAPE) depending on model
- Small test set → treat as early baseline, not final word

**Figures:** `model_comparison_baselines.png`, `pred_vs_true_eol_baselines.png`

*(Figure axes already labeled in cycles; title above states the unit.)*

---

## Slide 13 — What drives predictions?

**Title:** Feature importance (trees)

**Bullets:**
- **Green** = random forest · **Red** = XGBoost
- Both rank **ΔV(Q)** and **energy efficiency** highest — not raw capacity
- Consistent with Week 3 correlation (Severson 2019)

**Figures:** `feature_importance_rf.png`, `feature_importance_xgb.png`

**Captions (under figures):**
- Random forest — bar length = relative importance (Gini)
- XGBoost — same idea, different scoring (gain)

---

## Slide 14 — Week 4 summary & next steps

**Title:** Week 4 complete → Week 5 sequence model

**Bullets:**
- Reproducible baselines + saved split (`cell_split.csv`) for fair comparison later
- **Best baseline so far:** XGBoost, test MAE **~85 cycles**
- **Week 5:** LSTM or GRU on early per-cycle trajectories (`cycle_summary.csv`) — same split, same metrics

---

## Speaker notes (45 sec)

Week 4: trained four ML models to predict end-of-life from our 44 early-cycle features. We split by cell — about seventy-fifteen-fifteen, ninety-four twenty twenty — so the model never sees the same battery in train and test. Validation picks hyperparameters; test is the honest score. XGBoost did best on holdout — about 85 cycles average error on 20 test cells. Tree importance plots — green is random forest, red is XGBoost — both highlight voltage-curve change and energy efficiency, matching Week 3. Next week: a sequence model on per-cycle data to see if trajectories beat hand-crafted features.

---

## Anticipated Q&A (short)

| Question | Answer |
|----------|--------|
| What is val vs test? | Val = tune settings; test = final evaluation once. |
| Why is test only 20 cells? | ~15% of 134; cell-level split keeps whole batteries separate. |
| Is 85 cycles good? | Reasonable first baseline; Severson et al. report lower error with curated features + larger effective sample — we compare in the report. |
| Why not use capacity only? | Week 3 showed weak solo correlation; trees still lean on ΔV and efficiency. |
| Green vs red bars? | Green = random forest; red = XGBoost. Same story, different importance scores. |
