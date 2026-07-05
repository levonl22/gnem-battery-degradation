# 8. Conclusion

This eight-week GNEM project built a **reproducible Python pipeline** on the public MIT-Stanford-Toyota fast-charging dataset (Severson et al., 2019): 140 raw JSON files were cleaned to **134 unique cells**, per-cycle summaries and **44 early-cycle features** (including Severson-style ΔV(Q) voltage curves) were exported, and models were trained on a fixed **94 / 20 / 20** train/validation/test split (`random_state = 42`). Notebooks `01`–`10`, committed processed tables, metrics JSON, and figures support rerunning the full analysis.

## Answers to the research questions

1. **Can early-cycle data predict EOL before obvious fade?** Yes. The best holdout model (XGBoost at *N* = 100 cycles) achieves test MAE about **85 cycles** (about **11% MAPE**) predicting end-of-life on 20 unseen cells, using only measurements from the first 100 cycles.

2. **Which early-cycle features matter?** Exploratory correlation and tree importance consistently highlight **ΔV(Q)** statistics and **energy efficiency** summaries. The Week 7 ablation shows that tabular error drops sharply when ΔV(Q) features become available (*N* ≥ 50) and when the window reaches 100 cycles (test MAE about **167** → **107** → **85** cycles).

3. **Does a GRU outperform hand-crafted features?** **Not at the full window.** A single-head GRU on 100-cycle × 4-channel trajectories reaches about **110 cycles** test MAE, behind XGBoost (about **85**). At *N* = 20 only, the GRU (about **144** cycles) beats XGBoost (about **167**) because voltage-curve summaries are unavailable to the tree model. The strongest model is **context-dependent** on window length and feature type.

4. **Does a monotonic SOH penalty help?** **Marginally for curve shape, not for EOL error.** A dual-head GRU with monotonic regularization leaves test EOL MAE near the unconstrained model (about **112** cycles) and only slightly lowers SOH violation rates. Physics-inspired regularization without richer inputs or more training data has limited impact here.

## Summary

**XGBoost on the full 44-feature matrix at *N* = 100 cycles** is the best overall predictor in this study. Classical ensembles outperform linear baselines; the sequence model is competitive but does not close the gap on this cohort size. Early-cycle window length matters most for tabular models, while the GRU needs the full 100-cycle horizon to match its Week 5 performance.

## Limitations

Results are bounded by a **small dataset** (134 cells, 20-cell test holdout), a **single chemistry and fast-charge protocol**, and **asymmetric inputs** (XGBoost uses ΔV(Q) from raw JSON; the GRU uses four summary channels only). Duplicate barcodes, missing fields in some cycle rows, and a fixed 80% EOL definition add further uncertainty. See §7.2 for detail.

## Implications and future work

For **fast-charge cell screening**, observing about **50–100 early cycles** and extracting voltage-curve and efficiency features supports useful lifetime estimates before full degradation is visible, though metrics on 20 test cells should be treated as indicative rather than definitive. **External validation** on NASA or CALCE data, **richer sequence inputs** (e.g. ΔV(Q) channels), and **larger cohorts** are the most direct extensions; see §7.3 and `docs/future_work.md`.
