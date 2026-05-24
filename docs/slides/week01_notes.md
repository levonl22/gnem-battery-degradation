# Week 1 — Google Slides outline

Copy into your deck: **GNEM Battery Degradation — Weekly Progress**

---

## Slide 1 — Title

**Title:** Early Prediction of Lithium-Ion Battery End-of-Life  
**Subtitle:** GNEM Research Fellow · Levon Lau · May 2026  
**Footer:** MIT-Stanford-Toyota dataset (Severson et al., 2019)

---

## Slide 2 — Week 1 progress

**Title:** Week 1 — Data pipeline & EOL labels

**Bullets:**

- **Goal:** Predict EOL from early cycles (80% capacity threshold)
- **Built:** `JSON → cell_targets.csv` + `cycle_summary.csv`
- **Scale:** 140 files · 114,314 cycle rows · 134 unique cell IDs
- **Note:** Formation cycle 0 excluded; duplicate barcodes flagged for Week 2

**Figure:** `results/figures/eol_distribution.png`

**Pipeline (optional diagram):**

```
Raw JSON → notebook 01 → cell_targets (EOL)
         → notebook 03 → cycle_summary (per-cycle metrics)
```

---

## Speaker notes (30 sec)

Loaded Severson fast-charge data, defined EOL at 80% initial capacity, exported per-cell labels and a 114k-row per-cycle table. Next: EDA plots and duplicate-barcode policy before feature engineering.