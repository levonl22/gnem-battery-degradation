# Literature Summary (Week 1)

**Author:** Levon Lau  
**Date:** May 2026  

Summary of mentor-provided references for the GNEM early battery lifetime prediction project. Abstracts/first pages were used to populate this table.

---

## Summary table


| Paper                                    | Year | Dataset / data                                                                                                                                       | Method                                                                                                                        | What they predict                                                                                                                                              | Relevance to this project                                                                                                                                                              |
| ---------------------------------------- | ---- | ---------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Severson et al.,** *Nature Energy*     | 2019 | MIT-Stanford-Toyota fast-charge cells (124 commercial LFP/graphite in paper; **140 JSON files** in our repo)                                         | Early-cycle **hand-crafted features** (e.g. ΔV capacity curves) + **regularized linear model** (elastic net)                  | **Cycle life** before obvious capacity fade                                                                                                                    | **Primary reference and dataset.** Defines the problem we reproduce: EOL/cycle life from early cycles.                                                                                 |
| **Fei et al.,** *Energy*                 | 2021 | Multiple Li-ion cycling datasets; features from **first 100 cycles**                                                                                 | **42 manual features** → feature selection (wrapper, etc.) → ML (SVM, elastic net, GPR, …)                                    | **Battery lifetime** in early cycles (reported RMSE ~115 cycles, R² 0.90)                                                                                      | Direct template for **Week 3 feature engineering** and **Week 4 sklearn baselines** on our `cycle_summary` windows.                                                                    |
| **dos Reis et al.,** *Energy and AI*     | 2021 | **Review of 30+ public** Li-ion datasets (NASA, CALCE, Oxford, RWTH, etc.); organized by test mode (cycle aging, calendar, drive cycles, EIS, abuse) | **Survey / catalog** — tables of chemistry, # cells, test variables, measured signals (capacity, IR, V/I/T), links & licenses | **Does not train a model.** Documents what public cycling data supports: **SOH, SOC, RUL, capacity fade, knee/elbow points**, fault detection, BMS calibration | **Dataset selection rationale** for this project; shows which variables (capacity, temperature, IR) are standard in public aging data and cites NASA/CALCE as optional validation sets |
| **Chen et al.,** *IEEE Access*           | 2022 | Two public battery aging datasets (capacity sequences)                                                                                               | **Denoising autoencoder** + **Transformer** for temporal modeling                                                             | **RUL**                                                                                                                                                        | **Future work / stretch:** deep sequence model beyond planned LSTM/GRU; shows Transformer use for RUL.                                                                                 |
| **Wang et al.,** *Nature Communications* | 2024 | 387 NCM cells (own + three manufacturers); short pre-full-charge segments                                                                            | **Physics-informed neural network (PINN)** + statistical features from charge data                                            | **SOH** (MAPE ~0.87%); notes **80% SOH = first life**                                                                                                          | Motivates **Week 6 monotonic SOH constraint** and physics-informed thinking—not full PINN scope for us.                                                                                |
| **Li et al.,** *Nature Communications*   | 2025 | Cells aged at multiple temperatures; degradation-mode measurements                                                                                   | Physics-based models with **5 degradation mechanisms** vs simpler fits                                                        | **Capacity, resistance, and degradation modes**                                                                                                                | Reminder that capacity fade alone is **ambiguous**; supports interpreting our features cautiously (mechanism-agnostic ML).                                                             |
| **Hu et al.,** *Nature Communications*   | 2025 | LIB charging data (early lifecycle %)                                                                                                                | **BatteryGPT**: generative pre-trained Transformer predicts future charging; SOH / knee / **EOL**                             | **SOH, knee point, EOL** from early charging (e.g. first 5–30% of life)                                                                                        | **Out of scope** for 8-week build; cited as state-of-the-art early prediction beyond our LSTM/GRU plan.                                                                                |


---

## How these map to the 8-week plan


| Project phase                    | Main papers                                  |
| -------------------------------- | -------------------------------------------- |
| Week 1–2 (data, EOL)             | Severson 2019; dos Reis 2021                 |
| Week 3–4 (features, ML)          | Severson 2019; Fei 2021                      |
| Week 5 (sequence model)          | Chen 2022 (comparison context)               |
| Week 6 (physics-lite constraint) | Wang 2024                                    |
| Week 7–8 (report)                | Li 2025 (limitations); Hu 2025 (future work) |


---

## References

1. K. A. Severson et al., “Data-driven prediction of battery cycle life before capacity degradation,” *Nature Energy*, vol. 4, pp. 383–391, 2019. [https://doi.org/10.1038/s41560-019-0356-8](https://doi.org/10.1038/s41560-019-0356-8)
2. Z. Fei et al., “Early prediction of battery lifetime via a machine learning based framework,” *Energy*, vol. 225, 120205, 2021. [https://doi.org/10.1016/j.energy.2021.120205](https://doi.org/10.1016/j.energy.2021.120205)
3. G. dos Reis et al., “Lithium-ion battery data and where to find it,” *Energy and AI*, vol. 5, 100081, 2021. [https://doi.org/10.1016/j.egyai.2021.100081](https://doi.org/10.1016/j.egyai.2021.100081)
4. D. Chen, W.-C. Hong, and X. Zhou, “Transformer Network for Remaining Useful Life Prediction of Lithium-Ion Batteries,” *IEEE Access*, vol. 10, pp. 19621–19628, 2022. [https://doi.org/10.1109/ACCESS.2022.3151975](https://doi.org/10.1109/ACCESS.2022.3151975)
5. F. Wang et al., “Physics-informed neural network for lithium-ion battery degradation stable modeling and prognosis,” *Nature Communications*, vol. 15, 4332, 2024. [https://doi.org/10.1038/s41467-024-48779-z](https://doi.org/10.1038/s41467-024-48779-z)
6. R. Li et al., “The importance of degradation mode analysis in parameterising lifetime prediction models of lithium-ion battery degradation,” *Nature Communications*, vol. 16, 2776, 2025. [https://doi.org/10.1038/s41467-025-57968-3](https://doi.org/10.1038/s41467-025-57968-3)
7. J. Hu et al., “Early prediction of lithium-ion battery degradation with a generative pre-trained transformer,” *Nature Communications*, 2025. [https://doi.org/10.1038/s41467-025-66819-0](https://doi.org/10.1038/s41467-025-66819-0)

---

*Source PDFs: `literature/` folder in this repository.*