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
- **Scale:** 140 raw files → **134 cells** after Week 2 cleaning · ~111k cycle rows
- **Note:** Formation cycle 0 excluded; duplicate barcodes resolved (Week 2)

**Figure:** `results/figures/eol_distribution.png`

**Pipeline (optional diagram):**

```
Raw JSON → notebook 01 → cell_targets (EOL)
         → notebook 03 → cycle_summary (per-cycle metrics)
```

---

## Speaker notes (30 sec)

Loaded Severson fast-charge data, defined EOL at 80%, exported labels and per-cycle table. Week 2 added cleaning and EDA figures before feature engineering.