# Dataset Description (Week 1)

**Author:** Levon Lau  
**Date:** May 2026  

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


| File                               | Rows    | Grain                | Columns                              |
| ---------------------------------- | ------- | -------------------- | ------------------------------------ |
| `data/cell_targets.csv`            | 139     | 1 row / test record  | `cell_id`, `EOL`, `initial_capacity` |
| `data/processed/cycle_summary.csv` | 114,314 | 1 row / cell / cycle | `cell_id` + 16 `summary` fields      |


**Unique barcodes:** 134 in `cell_targets`; 135 in `cycle_summary`.  
**Gap:** Five duplicate `cell_id` values in `cell_targets` (same barcode, two files, different EOL). One cell (`el150800737381`) appears only in `cycle_summary` with a single cycle (not in targets). These need a deduplication rule before ML.

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

- Long-format arrays: ~2,000 points per cycle per signal
- Used later for voltage–capacity curves and ΔV(Q)-style features
- Not included in `cycle_summary.csv` due to size (~millions of points per cell)

---

## 6. End-of-life (EOL) definition

- **Threshold:** 80% of initial discharge capacity  
- **Initial capacity:** `discharge_capacity` at the first row with `cycle_index >= 1`  
- **EOL cycle:** First `cycle_index >= 1` where `discharge_capacity < 0.8 × initial_capacity`  
- **Censored cells:** If threshold is never reached, EOL = last available cycle index

**Distribution (139 rows):** min 159, median 788, max 2,237 cycles  

Built in `notebooks/01_data_exploration.ipynb`.

---

## 7. Data quality notes


| Issue                  | Detail                                                                                                                                                     |
| ---------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Cycle 0**            | Formation / setup cycle; abnormal capacity and `charge_duration`. Exclude from EOL baseline and early-cycle windows (use cycle ≥ 1, or ≥ 10 for modeling). |
| **Duplicate barcodes** | 5 IDs appear twice in `cell_targets` with different EOL (two JSON files per barcode).                                                                      |
| **Partial cell**       | `el150800737381`: 1 cycle in `cycle_summary` only.                                                                                                         |
| **Missing values**     | `charge_duration` (1,215 rows); `time_temperature_integrated` (34 rows).                                                                                   |


---

## 8. Typical scale


| Metric                    | Value                  |
| ------------------------- | ---------------------- |
| JSON files                | 140                    |
| Cycles per cell (approx.) | 159–2,237; median ~788 |
| `cycle_summary` rows      | 114,314                |


---

## 9. Intended use in project

- `**cycle_summary.csv`:** Early-cycle feature extraction (cycles 1–20 / 50 / 100)  
- `**cell_targets.csv`:** Supervised labels (EOL) for regression models  
- **Raw JSON / `cycles_interpolated`:** Curve-based features in Week 3+

---

## 10. Limitations

- Single public dataset and chemistry; results may not transfer to all cell types or operating conditions.  
- EOL rule (80%) is a project choice; not the only industry definition.  
- Duplicate barcodes and cycle 0 must be handled explicitly in preprocessing.

