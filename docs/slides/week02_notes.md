# Week 2 — Google Slides outline

Add these slides to the same deck after Week 1 check-in.

---

## Slide 3 — Capacity fade example

**Title:** Example capacity degradation curve

**Bullets:**
- Single cell: discharge capacity vs cycle (`cycle_index ≥ 1`)
- Red dashed line: 80% EOL threshold
- Orange line: computed EOL cycle

**Figure:** `results/figures/capacity_fade_example.png`

---

## Slide 4 — Cycle-life distribution

**Title:** End-of-life distribution across cells

**Bullets:**
- 139 labeled records; median EOL ≈ 788 cycles
- Range: 159–2,237 cycles (matches Severson-scale variability)
- Informs train/test split and model error interpretation

**Figure:** `results/figures/eol_distribution.png` (same as Week 1 slide 2, or updated after dedup)

---

## Speaker notes (30 sec)

Visual confirmation that cells degrade at different rates. EOL spread motivates cell-level ML split and early-cycle prediction task.
