# Future work (handoff)

Notes for anyone continuing this repo **after the Week 8 fellowship deliverables**. The Week 7 fellow is not planning further research; this file captures follow-up ideas that were discussed but not implemented.

**Current baselines (test set, 20 cells):** XGBoost at *N* = 100 → about **85** cycles MAE; single-head GRU at *N* = 100 → about **110** cycles MAE. See `docs/week07/README.md` and `results/metrics/`.

---

## 1. GRU with ΔV(Q) inputs (highest-impact modeling gap)

### Why it matters

XGBoost uses **44 hand-crafted features**, including **10 ΔV(Q) statistics** from discharge voltage curves (Severson-style). The GRU uses only **4 channels per timestep** from `cycle_summary.csv` (SOH, resistance, efficiency, temperature). Comparisons in Weeks 5–7 are therefore **not a controlled architecture study** — tabular models see richer inputs, especially at *N* ≥ 50.

ΔV(Q) today lives in `data/processed/voltage_features.csv`, built by `notebooks/04_extract_voltage_features.ipynb` from raw JSON `cycles_interpolated`. It is **not** in `cycle_summary.csv`.

### Three implementation paths (increasing effort)

| Approach | Idea | Rough effort | Tradeoff |
|----------|------|--------------|----------|
| **A. Broadcast scalars** | Merge existing 5–10 ΔV stats per cell; repeat as extra channels at every timestep (or concat before EOL head). | ~1–3 days | Fast sanity check; ΔV is constant across time — weak scientifically. |
| **B. Time-varying ΔV** | At timestep *t* ≥ 10, compute ΔV(Q) between cycle 10 and cycle *t*; cache per cell × cycle. | ~1–2 weeks | Best “sequence-native” fix; needs new preprocessing from raw JSON. |
| **C. Hybrid model** | GRU on 4-channel sequence + small MLP on 10 ΔV scalars → joint EOL head. | ~3–5 days | Common pattern for mixed static + sequence data; architecture differs from current single-head GRU. |

### Reusable code

- ΔV extraction: `notebooks/04_extract_voltage_features.ipynb` (`discharge_qv`, `delta_v_stats`)
- GRU training grid: `scripts/run_gru_ablation.py`, `notebooks/08_sequence_model.ipynb`
- Window ablation pattern: `notebooks/10_early_cycle_ablation.ipynb`
- Feature window rules (XGBoost): `features_for_window(n)` in notebook 10

### Window rules if re-running ablation

| N | ΔV(Q) available |
|---|-----------------|
| 20 | No |
| 50 | c10→c50 pair only |
| 100 | c10→c50 + c10→c100 |

Apply the same rules to any new GRU inputs for a fair comparison.

### Suggested success criteria

- GRU + ΔV at *N* = 100 should be compared to **both** current GRU (~110 MAE) and XGBoost (~85 MAE) on the same `cell_split.csv`.
- Document whether gains come from ΔV at short windows (*N* = 20–50) or only at *N* = 100.

---

## 2. Other modeling follow-ups

From `docs/report/07_discussion.md`:

- **External validation** — NASA / CALCE (dos Reis et al., 2021).
- **Stronger monotonic SOH** — larger λ grid, post-hoc monotonic projection, or dual-head GRU at shorter windows.
- **Alternative sequence models** — Transformers, pretrained time-series encoders (Chen 2022; Hu 2025).
- **Larger cohort / ensembling** — 94 train cells limits neural sequence fitting.

---

## 3. Data and pipeline

- **Missing values** — `charge_duration` (~1,209 rows), `time_temperature_integrated` (34 rows); not used in current features.
- **Duplicate barcodes** — resolved in Week 2; see `docs/week02/duplicate_barcode_policy.md`.
- **Raw JSON** — not in git; required for any new ΔV(Q) extraction.

---

## 4. References in-repo

| Topic | Location |
|-------|----------|
| Week 7 ablation results | `docs/week07/README.md`, `docs/report/06_results.md` §6.4 |
| Sequence model methods | `docs/report/05_methods.md` §5.2 |
| Feature definitions | `docs/report/04_features.md`, `docs/week03/README.md` |
| Slide trim target | `docs/slides/FINAL_DECK.md` |
