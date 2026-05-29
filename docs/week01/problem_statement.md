# Problem Statement — Early Prediction of Lithium-Ion Battery End-of-Life

**Project:** AI-Based Battery Degradation & Remaining Useful Life  
**Organization:** Georgia Network for Electric Mobility (GNEM)  
**Author:** Levon Lau  
**Date:** May 2026  

---

## 1. Background

Lithium-ion batteries lose capacity with cycling. In product development and grid/EV applications, it is valuable to estimate **how long a cell will last** without waiting for full life testing (often hundreds or thousands of cycles). Prior work has shown that signals from **early cycles**—before capacity has visibly faded—can predict long-term **cycle life** using machine learning (Severson et al., *Nature Energy*, 2019).

This project builds a reproducible pipeline on a public fast-charging dataset to predict **end-of-life (EOL)** from early-cycle measurements, compare feature-based and sequence models, and later add a simple physics-inspired constraint on predicted state-of-health (SOH) trajectories.

---

## 2. Problem Definition

**Given:** Per-cycle measurements from the first *N* cycles of a cell (e.g. *N* = 20, 50, or 100), including capacity, temperature, internal resistance, and related summary statistics.

**Predict:** The **EOL cycle**—the cycle index at which the cell’s discharge capacity falls below a fixed fraction of its initial capacity.

**EOL rule used in this project:**  
First cycle (with `cycle_index ≥ 1`) where  

`discharge_capacity < 0.8 × initial_discharge_capacity`,  

where **initial** is taken from the first qualifying cycle (formation / cycle 0 excluded from the baseline).

**Derived quantity (later):** **Remaining useful life (RUL)** at current cycle *k*:  

`RUL = predicted_EOL − k`.

---

## 3. Motivation

- **Testing cost and time:** Full cycle-life experiments are slow; early prediction can prioritize cells or protocols sooner.  
- **Design and safety:** Better forecasts support pack design, warranty, and degradation monitoring.  
- **Research goal:** Reproduce a published data-driven approach on an open dataset and extend it with standard ML baselines, one sequence model, and a light monotonic SOH regularizer within an eight-week plan.

---

## 4. Data (current status — Week 2)


| Artifact                | Description                                                                      |
| ----------------------- | -------------------------------------------------------------------------------- |
| **Source**              | MIT-Stanford-Toyota fast-charge dataset (Severson et al., 2019), 140 JSON files |
| `**cell_targets.csv`**  | 134 rows: `file_id`, `cell_id`, `EOL`, `initial_capacity`                        |
| `**cycle_summary.csv`** | 110,910 rows: `file_id`, `cell_id`, 16 summary fields per cycle                  |


Raw JSON also contains interpolated voltage/current curves (`cycles_interpolated`); reserved for later feature work.

**Cleaning (Week 2):** Longest-run dedupe for five duplicate barcodes; partial cell excluded. See `docs/week02/duplicate_barcode_policy.md`. Formation **cycle 0** excluded from EOL baseline.

---

## 5. Approach (eight-week plan)


| Phase     | Activity                                                        |
| --------- | --------------------------------------------------------------- |
| Weeks 1–2 | Data loading, EOL labeling, per-cycle tables, exploratory plots |
| Week 3    | Hand-crafted early-cycle features; correlation / importance     |
| Week 4    | Baselines: linear, ElasticNet, random forest, gradient boosting |
| Week 5    | One sequence model (LSTM or GRU) on early trajectories          |
| Week 6    | Simple monotonic SOH penalty vs unconstrained model             |
| Weeks 7–8 | Ablations (20 / 50 / 100 cycles), figures, report, slides       |


**Evaluation:** MAE, RMSE, MAPE on EOL; predicted vs true EOL plots; later SOH curve consistency checks.

---

## 6. Research Questions

1. Can early-cycle summary data predict EOL before significant capacity fade is visible?
2. Which features from the first 20, 50, and 100 cycles are most informative?
3. Does a sequence model (LSTM/GRU) outperform traditional ML on hand-crafted features?
4. Does a monotonic SOH constraint improve the physical plausibility of degradation curves?

---

## 7. Scope and Non-Goals

**In scope:** Public dataset; reproducible Python/Jupyter pipeline; interpretable features; one deep sequence model; simple monotonic regularization; quantitative comparison and report.

**Out of scope:** New cell testing; full electrochemical or physics-informed neural network (PINN) models; Transformer/foundation models (noted as future work); real-time BMS deployment.

---

## 8. Success Criteria (project end)

- Reproducible code from raw data → features → trained models → evaluation figures.  
- Clear comparison of ML baselines vs sequence model vs constrained SOH model.  
- Written report (~8–12 pages) and presentation (10–15 slides) suitable for a graduate research project.

---

## 9. Status

**Week 1:** Raw data ingested; EOL @ 80%; initial CSV export; literature summary; EDA figures started.  

**Week 2:** Duplicate-barcode policy; cleaned 134-cell dataset; report §3 and slide outlines updated.

---

*Primary reference:* K. A. Severson et al., “Data-driven prediction of battery cycle life before capacity degradation,” *Nature Energy*, vol. 4, pp. 383–391, 2019. [https://doi.org/10.1038/s41560-019-0356-8](https://doi.org/10.1038/s41560-019-0356-8)