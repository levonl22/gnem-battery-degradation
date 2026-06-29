# 7. Discussion

## 7.1 Main findings

Across Weeks 4–7, **XGBoost on the full 44-feature matrix at *N* = 100 cycles** remains the strongest holdout model (test MAE about **85 cycles**, about **11% MAPE** on 20 test cells). A single-head **GRU** on 100-cycle × 4-channel trajectories achieves about **110 cycles** MAE—competitive but consistently worse on this dataset size.

The **Week 7 ablation** (§6.4) shows that **tabular performance depends strongly on window length and ΔV(Q) features**: XGBoost test MAE falls from about 167 cycles at *N* = 20 to about 85 at *N* = 100. The **GRU is less sensitive to moderate window changes** (about 144–143 cycles at *N* = 20–50) and only approaches Week 5 levels at *N* = 100. At the shortest window, the sequence model outperforms XGBoost because voltage-curve summaries are unavailable to the tree model—a reminder that “best model” is **context-dependent** on how much early data and which feature types are available.

The **Week 6 monotonic SOH penalty** did not materially change EOL error (about 112 cycles test MAE constrained vs unconstrained) and only slightly reduced SOH violation rates. Physics-inspired regularization without richer inputs or a larger training set has limited impact here.

## 7.2 Limitations

- **Small dataset and holdout** — 134 cells total; 94 train / 20 val / 20 test. Metrics on 20 test batteries have high variance; a single outlier cell can move MAPE noticeably.
- **Single dataset and chemistry** — LFP/graphite, fast-charge protocol only (Severson et al., 2019); generalization to other chemistries or cycling conditions is untested.
- **Duplicate barcodes** — raw files contained duplicate cell IDs; we kept the longest continuous run per barcode (134 cells). See `docs/week02/duplicate_barcode_policy.md`. Residual protocol heterogeneity may remain.
- **Missing values** — `charge_duration` missing on about 1,209 cycle rows; `time_temperature_integrated` on 34 rows. These columns were not used in the Week 3 feature matrix or sequence channels.
- **Feature mismatch across model classes** — XGBoost uses hand-crafted summaries including ΔV(Q) from raw JSON; the GRU uses four channels from `cycle_summary.csv` only. Comparisons are informative but not a controlled architecture-only study.
- **Mechanism-agnostic features** — capacity fade and summary statistics do not identify degradation mode (Li et al., 2025).
- **EOL definition** — 80% of first measured capacity (`cycle_index ≥ 1`) is one convention; industry definitions vary.

## 7.3 Future work

- **External validation** — NASA or CALCE datasets (dos Reis et al., 2021) to test transfer beyond the MIT-Stanford-Toyota cohort.
- **Richer sequence inputs** — incorporate ΔV(Q) or other voltage-curve channels into recurrent models for a fairer comparison with XGBoost.
- **Larger cohorts / ensembling** — more cells would stabilize neural sequence training and ablation trends.
- **Stronger physics-informed constraints** — larger λ grids, post-hoc monotonic projection, or full PINN-style formulations if SOH curve plausibility is a deployment requirement.
- **Alternative sequence architectures** — Transformers or pretrained time-series models (Chen 2022; Hu 2025) on longer or multi-resolution windows.

*(Week 8 — merge sections, conclusion, and references into final PDF.)*
