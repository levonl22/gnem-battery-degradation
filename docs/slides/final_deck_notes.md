# Final deck — copy-paste outline (12 slides)

Trimmed from the 26-slide weekly deck. **No Week 8 check-in slide.** Export: Google Slides or edit `results/gnem_battery_slides.pptx` → PDF → `results/gnem_battery_slides.pdf`.

Figure paths are relative to repo root: `results/figures/...`

---

## Slide 1 — Title

**Title:** Early Prediction of Lithium-Ion Battery End-of-Life

**Subtitle:** GNEM Research Fellow · Levon Lau · July 2026

**Optional footer:** github.com/levonl22/gnem-battery-degradation

---

## Slide 2 — Problem & motivation

**Title:** Problem & motivation

**Bullets:**
- Lithium-ion cells lose capacity over cycling; full life tests can run **hundreds to thousands of cycles**
- **Goal:** predict **end-of-life (EOL)** from **early-cycle** measurements before obvious fade
- **EOL definition:** first cycle where discharge capacity &lt; **80%** of initial capacity (`cycle_index ≥ 1`)
- **Dataset:** MIT-Stanford-Toyota fast-charging cohort (Severson et al., 2019)
- **Approach:** reproducible Python pipeline → hand-crafted features + tree models vs GRU sequence model → monotonic SOH check → early-cycle window ablation

---

## Slide 3 — Dataset & pipeline

**Title:** Dataset & pipeline

**Bullets:**
- **Raw:** 140 JSON files (`FastCharge_*_structure.json`) from MATR.io
- **Cleaned:** **134 unique cells** (duplicate barcodes → longest run kept; one partial cell dropped)
- **Grain:** about **111k** per-cycle rows in `cycle_summary.csv`; **44** cell-level features in `cell_features.csv`
- **Split:** cell-level **94 / 20 / 20** train · val · test (`random_state = 42`) — never random row splits
- **Pipeline:** notebooks `01`–`10` · processed CSVs · metrics JSON · figures in `results/`

---

## Slide 4 — EOL distribution & capacity fade

**Title:** Labels — capacity fade & cycle-life spread

**Left / top — capacity fade example**
- Single cell: discharge capacity vs cycle
- Red dashed: 80% threshold · orange: computed EOL
- **Figure:** `results/figures/capacity_fade_example.png`

**Right / bottom — EOL distribution**
- **134** cells · median EOL about **792** cycles · range **159–2,237**
- Wide spread motivates cell-level modeling and cautious test metrics
- **Figure:** `results/figures/eol_distribution.png`

---

## Slide 5 — Feature engineering

**Title:** Early-cycle features (Week 3)

**Bullets:**
- **Input windows:** first **20 / 50 / 100** cycles per cell
- **44 features per cell:** capacity, SOH, resistance, **energy efficiency**, temperature summaries + **Severson-style ΔV(Q)** (voltage-curve change between cycles 10→50 and 10→100)
- **Exploratory screening:** Pearson correlation vs EOL on all 134 cells
- **Strongest linear signals:** ΔV(Q) spread (`delta_v_std_c10_c100`, |r| about 0.8) · efficiency (`efficiency_mean_w100`, r about 0.78)
- **Weaker alone:** raw capacity at cycle 100 — curve shape and efficiency shift before obvious fade

**Figure:** `results/figures/feature_correlation.png`

---

## Slide 6 — ML baselines — test error

**Title:** Classical ML baselines (20-cell test set)

**Bullets:**
- **Input:** `cell_features.csv` — 44 features · **Target:** EOL
- **Models:** linear regression · ElasticNet · random forest · **XGBoost**
- **Tuning:** validation MAE · **Test set untouched** during hyperparameter search

**Table — test MAE (cycles):**

| Model | MAE | MAPE (about) |
|-------|-----|--------------|
| Linear | 133 | 18% |
| ElasticNet | 132 | 19% |
| Random forest | 101 | 13% |
| **XGBoost** | **85** | **11%** |

**Figure:** `results/figures/model_comparison_baselines.png`

---

## Slide 7 — ML — predicted vs true EOL

**Title:** Tabular models — predicted vs true EOL (test)

**Bullets:**
- Tree ensembles clearly beat linear models on holdout
- **XGBoost best:** about **85 cycles** MAE (about **11%** MAPE)
- RF / XGBoost importance: **ΔV(Q)** and **energy efficiency** rank highest (consistent with correlation)
- **Caveat:** only **20** test cells → indicative metrics

**Figures:**
- `results/figures/pred_vs_true_eol_baselines.png`
- Optional smaller: `feature_importance_xgb.png`

---

## Slide 8 — GRU sequence model

**Title:** GRU on early per-cycle trajectories

**Bullets:**
- **Input:** first **100 cycles × 4 channels** — SOH, resistance, energy efficiency, temperature (`cycle_summary.csv`)
- **Model:** PyTorch **GRU** · 16-combo hyperparameter grid on validation MAE
- **Not in sequence input:** ΔV(Q) features (live in raw JSON only)
- **Test MAE:** about **110 cycles** — competitive but **behind XGBoost** (about **85**)
- Plausible reasons: **94** training cells · no voltage-curve channels · little capacity fade in first 100 cycles

**Figure:** `results/figures/pred_vs_true_eol_sequence.png`

---

## Slide 9 — Monotonic SOH constraint

**Title:** Physics-inspired SOH regularization (Week 6)

**Bullets:**
- **Dual-head GRU:** predicts **EOL** + **SOH trajectory** (100 values per cell)
- **Monotonic penalty:** discourage SOH increasing cycle-to-cycle (λ ∈ {0.01, 0.1, 1.0})
- **EOL test MAE:** about **112 cycles** constrained vs unconstrained — **essentially unchanged**
- Violation rate drops only slightly; XGBoost still best for EOL
- Light regularizer — **not** a full physics-informed neural network

**Figures:**
- `results/figures/soh_curves_constrained.png`
- `results/figures/model_comparison_soh_penalty.png`

---

## Slide 10 — Early-cycle ablation

**Title:** How many early cycles are needed? (*N* = 20, 50, 100)

**Bullets:**
- **Question:** if you only observe the first **N** cycles, how well can you predict EOL?
- **Same split & metrics** · XGBoost uses valid feature subset at each *N* · GRU uses first *N* timesteps

**Table — test MAE (cycles):**

| N | XGBoost | GRU |
|---|---------|-----|
| 20 | 167 | **144** |
| 50 | 107 | 143 |
| 100 | **85** | 110 |

- XGBoost gains sharply with *N* (ΔV(Q) from *N* ≥ 50)
- GRU flat at 20–50, improves at 100
- **Best model is context-dependent** on window length

**Figure:** `results/figures/ablation_early_cycles.png`

---

## Slide 11 — Limitations

**Title:** Limitations

**Bullets:**
- **Small cohort:** 134 cells · **20-cell** test holdout → high metric variance
- **Single dataset:** LFP/graphite · fast-charge protocol only; transfer untested
- **Asymmetric inputs:** XGBoost uses ΔV(Q) from raw JSON; GRU uses four summary channels only
- **Duplicate barcodes** in raw files (longest run kept); residual protocol heterogeneity possible
- **Mechanism-agnostic features** — capacity summaries do not identify degradation mode
- **EOL definition** — 80% of first measured capacity is one convention among many

---

## Slide 12 — Conclusions & future work

**Title:** Conclusions & future work

**Bullets:**
- Built a **reproducible pipeline** from raw JSON to ML-ready tables, models, and figures
- **Best overall:** XGBoost at *N* = 100 — test MAE about **85 cycles** (about **11%** MAPE)
- **Early screening:** about **50–100 cycles** + voltage-curve / efficiency features support useful lifetime estimates
- **Sequence model:** GRU viable but does not beat tabular model at full window on this dataset size
- **Monotonic SOH penalty:** small curve-shape effect; does not improve EOL error

**Future work:**
- External validation (NASA / CALCE) · ΔV(Q) channels in sequence models · larger cohorts

**Deliverables:** 8–12 page report · GitHub repo · `docs/future_work.md`

---

## Slides removed from weekly deck (26 → 12)

| Weekly slide | Reason dropped |
|--------------|----------------|
| Week 1–7 “complete → next week” transitions (9, 14, 18, 22, 26) | Progress narration, not final story |
| Week 1–7 header slides (2, 3, 6, 10, 15, 19, 23) | Merged into problem / pipeline / model slides |
| ΔV(Q) explainer (7) | Detail trimmed; ΔV summarized on slide 5 |
| Models trained list (11) | Folded into slide 6 |
| Feature importance standalone (13) | Optional on slide 7 |
| Ablation setup (24) | Folded into slide 10 |
| GRU architecture detail (16) | Folded into slide 8 |
| Monotonic architecture detail (20) | Folded into slide 9 |
