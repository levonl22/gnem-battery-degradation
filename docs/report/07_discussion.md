# 7. Discussion

*(Week 7 — draft; expand in Week 8.)*

## 7.1 Limitations

- **Single dataset and chemistry** (LFP/graphite, fast-charge only); generalization untested.
- **Duplicate barcodes** in raw files require explicit handling before ML.
- **Mechanism-agnostic features:** capacity fade alone may not identify degradation mode (Li et al., 2025).
- **EOL definition:** 80% of first measured capacity is one convention; industry definitions vary.

## 7.2 Future work

- Supplemental validation on NASA or CALCE data (dos Reis et al., 2021)
- Voltage-curve features (Severson ΔV(Q)); Transformer/GPT approaches (Chen 2022; Hu 2025)
- Full physics-informed or degradation-mode-aware modeling
