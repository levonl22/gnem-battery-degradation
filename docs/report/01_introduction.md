# 1. Introduction

## 1.1 Background

Lithium-ion batteries lose capacity with cycling. In electric mobility and grid storage, estimating **how long a cell will last** without completing full life testing (often hundreds to thousands of cycles) reduces development time and cost. Severson et al. (2019) showed that **early-cycle** charge/discharge data can predict **cycle life** before visible capacity fade using machine learning on a large fast-charging dataset.

This project implements a reproducible pipeline on that public dataset: extract labels and per-cycle tables, engineer early-cycle features, train classical ML and one sequence model, and evaluate a simple monotonic state-of-health (SOH) constraint within an eight-week GNEM research plan.

## 1.2 Problem definition

**Input:** Per-cycle measurements from the first *N* cycles (*N* = 20, 50, or 100 in ablation studies), including discharge capacity, temperature, internal resistance, and related summary statistics.

**Output:** **End-of-life (EOL)** — the cycle index when discharge capacity first falls below **80%** of initial capacity (initial measured at the first cycle with `cycle_index ≥ 1`, excluding formation cycle 0).

**Derived target:** Remaining useful life at cycle *k*: RUL = EOL − *k*.

## 1.3 Research questions

1. Can early-cycle summary data predict EOL before significant fade?
2. Which features from the first 20, 50, and 100 cycles are most informative?
3. Does an LSTM/GRU on early sequences outperform ML on hand-crafted features?
4. Does a monotonic SOH penalty improve physical plausibility of predicted degradation curves?

## 1.4 Scope

**In scope:** Public MIT-Stanford-Toyota data; Jupyter/Python pipeline; interpretable features; sklearn baselines; one LSTM/GRU; light monotonic regularizer; quantitative evaluation and report.

**Out of scope:** New experiments; full electrochemical or PINN models; Transformer/foundation models; BMS deployment.

## 1.5 Report organization

Section 2 reviews related work. Section 3 describes data and exploratory analysis. Sections 4–6 (Weeks 3–7) cover features, methods, and results. Section 7 discusses limitations; Section 8 concludes.
