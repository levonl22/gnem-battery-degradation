# Week 2 — Google Slides outline

Add these slides to the same deck after Week 1 check-in.

---

## Slide 3 — Data cleaning

**Title:** Week 2 — Cleaned dataset

**Bullets:**
- **140 raw test files** → **134 unique cells** (five barcodes tested twice; one partial run dropped)
- **Rule:** keep longest test per barcode; each row has `file_id` + `cell_id`
- **Outputs:** `cell_targets.csv` (134 rows) · `cycle_summary.csv` (110,910 cycle rows)

---

## Slide 4 — Capacity fade example

**Title:** Example capacity degradation curve

**Bullets:**
- Single cell: discharge capacity vs cycle (`cycle_index ≥ 1`)
- Red dashed line: 80% EOL threshold
- Orange line: computed EOL cycle

**Figure:** `results/figures/capacity_fade_example.png`

---

## Slide 5 — Cycle-life distribution

**Title:** End-of-life distribution across cells

**Bullets:**
- **134** labeled cells; median EOL ≈ **792** cycles
- Range: 159–2,237 cycles (matches Severson-scale variability)
- Informs cell-level train/test split and model error interpretation

**Figure:** `results/figures/eol_distribution.png`

---

## Speaker notes (30 sec)

Week 2: cleaned duplicate barcodes so one row = one cell, then confirmed EOL spread and example fade curves. That variability is why we predict cycle life from early cycles rather than assuming a single degradation rate.
