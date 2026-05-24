# 2. Related Work

## 2.1 Early cycle-life prediction

Severson et al. (2019) introduced the MIT-Stanford-Toyota fast-charging dataset and demonstrated **cycle-life prediction from early cycles** using hand-crafted features (including voltage–capacity curve differences) and a regularized linear model, achieving accurate ranking before substantial degradation. This work defines both our **primary dataset** and the core prediction task.

Fei et al. (2021) proposed a three-stage ML framework: **42 features** from the first 100 cycles, feature selection, and multiple regressors (SVM, elastic net, GPR), reporting strong early-lifetime accuracy. That framework informs our Week 3–4 feature engineering and baseline model choices.

## 2.2 Public battery data

dos Reis et al. (2021) surveyed **30+ public** lithium-ion datasets (NASA, CALCE, Oxford, etc.), cataloging test modes, variables (capacity, temperature, impedance), and ML use cases (SOH, SOC, RUL). We use this review to justify dataset selection and to note optional supplemental validation sets.

## 2.3 Deep learning and physics-informed approaches

Chen et al. (2022) applied a **Transformer** with a denoising autoencoder for RUL prediction—relevant as comparison context for our planned LSTM/GRU (Week 5). Wang et al. (2024) used a **physics-informed neural network** for SOH estimation across 387 cells, noting **80% SOH as first service life**—motivating our Week 6 monotonic SOH constraint without full PINN complexity.

Li et al. (2025) showed that models fit to capacity fade alone can be **non-unique** without degradation-mode analysis—a limitation we acknowledge for mechanism-agnostic ML. Hu et al. (2025) (BatteryGPT) represents state-of-the-art generative early prediction and is cited as **future work** outside our eight-week scope.

## 2.2 Summary

Our project sits between Severson-style **interpretable early prediction** and modern **sequence/physics-informed** methods: reproducible data pipeline, classical ML baselines, one sequence model, and a simple physical consistency check on SOH trajectories.

*Full reference list: see [09_references.md](09_references.md).*
