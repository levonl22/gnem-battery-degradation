# Duplicate barcode policy (Week 2)

**Purpose:** Decide what counts as “one cell” before EDA stats and ML.  
**Status:** **Approved** — longest-run-wins dedupe → 134 cells (May 2026).

---

## Counting (140 files → 134 cells)

| Piece | Count |
|-------|------:|
| Total JSON test files | 140 |
| Partial test (no lifespan label) | −1 |
| Labeled files | 139 |
| Barcodes tested **twice** (5 pairs) | 5 **extra** files (not 10) |
| **Unique barcodes** | **134** |

Each duplicate pair = 2 files, 1 barcode → only **one** file is extra.  
`140 − 1 partial − 5 extra = 134` unique barcodes. After dedupe we keep **134 rows** in `cell_targets.csv`.

---

## Plain-language summary

- We have **140 test files** but only **134 different battery barcodes**.
- **5 barcodes were tested twice** (two files each). Those pairs disagree on lifespan (EOL).
- **`cell_targets.csv`** has **one row per file** (139 rows) — correct at the file level.
- **`cycle_summary.csv`** labels rows by barcode only and **stacks both tests on top of each other**, so cycle numbers repeat for those 5 barcodes. Do **not** use those rows as-is for fade curves or features.
- One barcode (**`el150800737381`**) has almost no data (formation cycle only) and is **not** in `cell_targets`.

---

## The five duplicate pairs

Each row is one JSON file. **Keep** = file we retain under the recommended rule below.

| Barcode | File (drop) | EOL | File (keep) | EOL |
|---------|-------------|-----|-------------|-----|
| `el150800460486` | `FastCharge_000004_CH2_structure.json` | 982 | `FastCharge_000045_CH2_structure.json` | **1,178** |
| `el150800460514` | `FastCharge_000004_CH1_structure.json` | 663 | `FastCharge_000045_CH1_structure.json` | **1,189** |
| `el150800460623` | `FastCharge_000004_CH3_structure.json` | 1,061 | `FastCharge_000045_CH3_structure.json` | **1,176** |
| `el150800464865` | `FastCharge_000026_CH6_structure.json` | 483 | `FastCharge_000063_CH6_structure.json` | **1,226** |
| `el150800464977` | `FastCharge_000026_CH5_structure.json` | 209 | `FastCharge_000063_CH5_structure.json` | **1,226** |

Pattern: the **`000045`** and **`000063`** files are the longer, complete runs; the **`000004`** / **`000026`** files are shorter or failed early.

---

## Partial cell

| Barcode | File | Issue | Action |
|---------|------|-------|--------|
| `el150800737381` | `FastCharge_000002_CH26_structure.json` | Only cycle 0 in summary; no `cycle_index ≥ 1` → no EOL label | **Exclude** from targets, EDA, and modeling |

---

## Approved policy

### 1. Unit of analysis = **one barcode, one test run**

For this project, treat **134 physical cells** as the modeling population:

- **Rule:** When the same barcode appears in two files, **keep the file with the higher EOL** (longer test). Drop the other file from all downstream tables.
- **Rationale:** Matches “one cell, one lifespan” in Severson et al.; avoids train/test leakage if two runs of the same barcode were split across folds; the kept run is always the more informative one here.

### 2. Add **`file_id`** when we rebuild tables (Week 2 follow-up)

- `file_id` = JSON filename (e.g. `FastCharge_000045_CH2_structure.json`).
- `cell_id` = barcode (may repeat in raw data; unique after dedupe).
- Re-export `cycle_summary` **per file**, not merged by barcode alone, so cycle indices never collide.

### 3. Counts after dedupe

| Dataset | Before | After policy |
|---------|--------|----------------|
| Labeled cells (`cell_targets`) | 139 rows, 134 unique barcodes | **134 rows**, 134 unique barcodes |
| Per-cycle summary | 114,314 rows (5 barcodes corrupted) | Rebuild from **134 kept files** only |
| EDA / ML | — | **134 cells**; exclude `el150800737381` |

### 4. EOL distribution for slides/report

Recompute min / median / max / mean on **134 deduped rows**, not 139. Expect similar shape; max may shift slightly because we drop one very short run (EOL 209).

---

## Alternative (not recommended for Week 2)

**Keep all 139 files** as separate samples with `file_id`, and when splitting data, **never put two files with the same barcode in different folds**. More data, but harder to explain and easy to leak if grouping is forgotten.

---

## Implementation

| Step | Status |
|------|--------|
| `cell_targets.csv` with `file_id`, 134 rows | `scripts/rebuild_processed_data.py` |
| `cycle_summary.csv` with `file_id`, kept files only | same script |
| Notebooks `01` / `03` aligned with policy | patched |
| EOL figures on deduped targets | `scripts/generate_week12_figures.py` |
| Report §3.2 + slide notes | Done |

*Author: Week 2 audit, May 2026*
