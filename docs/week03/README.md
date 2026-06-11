# Week 3 deliverables (complete)

Hand-crafted early-cycle features → `cell_features.csv`, correlation vs EOL, heatmap.

| File | Status |
|------|--------|
| `notebooks/04_extract_voltage_features.ipynb` | Done → `voltage_features.csv` |
| `notebooks/05_build_cell_features.ipynb` | Done → `cell_features.csv` |
| `notebooks/06_feature_correlation.ipynb` | Done → `feature_correlation.png` |
| Report `04_features.md` | Done |
| `docs/slides/week03_notes.md` | Done |

---

## Data artifacts

| Artifact | Rows | Columns | Notes |
|----------|------|---------|--------|
| `data/processed/voltage_features.csv` | 134 | 10 ΔV(Q) features | From raw `cycles_interpolated` |
| `data/processed/cell_features.csv` | 134 | 4 labels + **44** features | Merged matrix for Week 4 ML |

**Labels** (in `cell_features.csv`): `file_id`, `cell_id`, `EOL`, `initial_capacity`

**Policy:** 134 kept cells after Week 2 dedupe — `docs/week02/duplicate_barcode_policy.md`

**Regenerate features:**

1. `notebooks/04_extract_voltage_features.ipynb` (requires `data/raw/`, ~5–10 min for all cells)
2. `notebooks/05_build_cell_features.ipynb`

Optional full rebuild of inputs first: `python scripts/rebuild_processed_data.py`

**Correlation figure:** `results/figures/feature_correlation.png` — run `notebooks/06_feature_correlation.ipynb`

---

## Feature groups (44 columns)

Early windows use cycles with `cycle_index ≥ 1` (cycle 0 excluded).

### 1. Summary features from `cycle_summary.csv` (34)

Built in `notebooks/05_build_cell_features.ipynb`.

| Group | Count | Description |
|-------|-------|-------------|
| **Resistance** | 7 | `resistance_initial` (cycle 1); mean + slope over w20 / w50 / w100 |
| **Capacity snapshots** | 6 | `capacity_c10/c50/c100`, `soh_c10/c50/c100` |
| **Capacity window stats** | 9 | slope, mean, std over w20 / w50 / w100 |
| **SOH window** | 3 | `soh_w20`, `soh_w50`, `soh_w100` (capacity at window end ÷ initial) |
| **Efficiency** | 6 | mean + std of `energy_efficiency` over w20 / w50 / w100 |
| **Temperature** | 3 | mean `temperature_average` over w20 / w50 / w100 |

Window suffix **`w20` / `w50` / `w100`** = statistics over cycles **1–20**, **1–50**, **1–100**.

### 2. Voltage ΔV(Q) features from raw JSON (10)

Built in `notebooks/04_extract_voltage_features.ipynb` (Severson-style).

**ΔV(Q) = V_late(Q) − V_early(Q)** on overlapping discharge capacity, summarized as mean / std / var / min / max.

| Cycle pair | Features |
|------------|----------|
| 10 → 50 | `delta_v_mean_c10_c50`, `delta_v_std_c10_c50`, `delta_v_var_c10_c50`, `delta_v_min_c10_c50`, `delta_v_max_c10_c50` |
| 10 → 100 | `delta_v_mean_c10_c100`, `delta_v_std_c10_c100`, `delta_v_var_c10_c100`, `delta_v_min_c10_c100`, `delta_v_max_c10_c100` |

---

## Correlation vs EOL (exploratory)

Univariate Pearson correlation on all 134 cells (`notebooks/06_feature_correlation.ipynb`).

**Strongest |r| with EOL (examples):**

| Feature | Pearson r | Direction |
|---------|-----------|-----------|
| `delta_v_std_c10_c100` | −0.81 | Higher spread in voltage-curve change → shorter life |
| `delta_v_min_c10_c100` | +0.80 | Higher min ΔV → longer life |
| `efficiency_mean_w100` | +0.78 | Higher mean energy efficiency → longer life |

**Weaker linear links:** raw capacity snapshots and capacity slopes alone (e.g. `capacity_c100` |r| ≈ 0.07).

**Takeaway:** ΔV(Q) and early efficiency track EOL more strongly than simple capacity fade in the first ~100 cycles — consistent with Severson et al. (2019). Many ΔV and windowed features are highly correlated with each other (see heatmap); Week 4 models should use regularization or feature selection.

**Figure:** `results/figures/feature_correlation.png` — 45×45 Pearson matrix (44 features + EOL). Read the **EOL** row/column for feature–lifetime links.

---

## Notebook map

| Notebook | Input | Output |
|----------|-------|--------|
| `04_extract_voltage_features.ipynb` | `data/raw/FastCharge*.json` | `data/processed/voltage_features.csv` |
| `05_build_cell_features.ipynb` | `cycle_summary.csv`, `voltage_features.csv`, `cell_targets.csv` | `data/processed/cell_features.csv` |
| `06_feature_correlation.ipynb` | `cell_features.csv` | `results/figures/feature_correlation.png` |

---

## Next

- [x] Report §4 — `docs/report/04_features.md`
- [x] Slides — `docs/slides/week03_notes.md`
- [x] Update `docs/PROJECT_CONTEXT.md` and root `README.md`
- **Week 4:** ML baselines on `cell_features.csv` (linear, ElasticNet, RF, XGBoost)
