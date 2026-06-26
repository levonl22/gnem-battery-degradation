# Dataset Description (Week 1)

**Author:** Levon Lau  
**Date:** May 2026  

> **Current processed data (Week 2):** 134 cells, 110,910 cycle rows, `file_id` column. See `docs/week02/duplicate_barcode_policy.md`. Tables below describe the initial Week 1 export where noted.

---

## 1. Source


| Item                 | Detail                                                                                                               |
| -------------------- | -------------------------------------------------------------------------------------------------------------------- |
| **Dataset**          | MIT-Stanford-Toyota fast-charging battery cycling data                                                               |
| **Reference**        | Severson et al. (2019), *Nature Energy*, 4, 383–391                                                                  |
| **DOI**              | [https://doi.org/10.1038/s41560-019-0356-8](https://doi.org/10.1038/s41560-019-0356-8)                               |
| **Download**         | [https://data.matr.io/1/projects/5c48dd2bc625d700019f3204](https://data.matr.io/1/projects/5c48dd2bc625d700019f3204) |
| **Chemistry / test** | Commercial LFP/graphite cells; fast-charging protocols (see per-file `protocol` field)                               |


---

## 2. Raw data layout

- **Format:** One JSON file per test record: `data/raw/FastCharge_*_structure.json`
- **Count:** 140 files (gitignored; large)
- **Main sections per file:**


| Section                  | Content                                                                               |
| ------------------------ | ------------------------------------------------------------------------------------- |
| `barcode`                | Cell identifier (`cell_id`)                                                           |
| `summary`                | Per-cycle table (16 fields, array-of-columns layout)                                  |
| `cycles_interpolated`    | Interpolated time-series (voltage, current, temperature, capacity, etc.) — very large |
| `protocol`, `channel_id` | Test metadata                                                                         |


**Notebook 02** inspects one file; **01** builds targets; **03** builds `cycle_summary.csv`.

---

## 3. Processed outputs (this repo)


| File                               | Rows (Week 1 → Week 2) | Grain                | Columns                              |
| ---------------------------------- | ---------------------- | -------------------- | ------------------------------------ |
| `data/cell_targets.csv`            | 139 → **134**          | 1 row / cell         | `file_id`, `cell_id`, `EOL`, `initial_capacity` |
| `data/processed/cycle_summary.csv` | 114,314 → **110,910**  | 1 row / cell / cycle | `file_id`, `cell_id` + 16 `summary` fields      |


**Week 1 gap (resolved Week 2):** Five barcodes had two JSON files each; one partial file had no EOL. Longest-run-wins dedupe → 134 unique cells.

---

## 4. `summary` fields (per cycle)


| Column                                                              | Description                                                |
| ------------------------------------------------------------------- | ---------------------------------------------------------- |
| `cycle_index`                                                       | Cycle number (0 = formation / non-protocol step)           |
| `discharge_capacity`                                                | Discharge capacity (Ah)                                    |
| `charge_capacity`                                                   | Charge capacity (Ah)                                       |
| `discharge_energy`, `charge_energy`                                 | Energy (Wh-scale per file units)                           |
| `dc_internal_resistance`                                            | DC internal resistance                                     |
| `temperature_maximum`, `temperature_average`, `temperature_minimum` | Temperature (°C)                                           |
| `date_time_iso`                                                     | Timestamp                                                  |
| `energy_efficiency`                                                 | Energy efficiency                                          |
| `charge_throughput`, `energy_throughput`                            | Throughput metrics                                         |
| `charge_duration`                                                   | Charge step duration (cycler units; missing on 1,215 rows) |
| `time_temperature_integrated`                                       | ∫T·dt-style thermal exposure (likely °C·s; 34 missing)     |
| `paused`                                                            | Pause flag (mostly 0; occasional sentinel e.g. −128)       |


**Performance-oriented fields for modeling:** 15 (exclude `paused` and optionally `date_time_iso` as metadata).

---

## 5. `cycles_interpolated` (not exported to CSV)

- Long-format arrays: about 2,000 points per cycle per signal
- Used later for voltage–capacity curves and ΔV(Q)-style features
- Not included in `cycle_summary.csv` due to size (about millions of points per cell)

---

## 6. End-of-life (EOL) definition

- **Threshold:** 80% of initial discharge capacity  
- **Initial capacity:** `discharge_capacity` at the first row with `cycle_index >= 1`  
- **EOL cycle:** First `cycle_index >= 1` where `discharge_capacity < 0.8 × initial_capacity`  
- **Censored cells:** If threshold is never reached, EOL = last available cycle index

**Distribution (134 cells, Week 2):** min 159, median 792, max 2,237 cycles  

Built in `notebooks/01_data_exploration.ipynb`.

---

## 7. Data quality notes


| Issue                  | Detail                                                                                                                                                     |
| ---------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Cycle 0**            | Formation / setup cycle; abnormal capacity and `charge_duration`. Exclude from EOL baseline and early-cycle windows (use cycle ≥ 1, or ≥ 10 for modeling). |
| **Duplicate barcodes** | Resolved Week 2 (longest run per barcode).                                                                                                               |
| **Partial cell**       | `el150800737381` excluded.                                                                                                                                 |
| **Missing values**     | `charge_duration` (about 1,209 rows); `time_temperature_integrated` (34 rows).                                                                                  |


---

## 8. Typical scale


| Metric                    | Value                  |
| ------------------------- | ---------------------- |
| JSON files                | 140                    |
| Cycles per cell (approx.) | 159–2,237; median about 792 |
| `cycle_summary` rows      | 110,910 (134 cells)    |


---

## 9. Intended use in project

- `**cycle_summary.csv`:** Early-cycle feature extraction (cycles 1–20 / 50 / 100)  
- `**cell_targets.csv`:** Supervised labels (EOL) for regression models  
- **Raw JSON / `cycles_interpolated`:** Curve-based features in Week 3+

---

## 10. Limitations

- Single public dataset and chemistry; results may not transfer to all cell types or operating conditions.  
- EOL rule (80%) is a project choice; not the only industry definition.  
- Cycle 0 must be excluded from EOL baseline and early-cycle windows; duplicate barcodes handled in Week 2.

