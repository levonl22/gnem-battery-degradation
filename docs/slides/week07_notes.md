# Week 7 — Google Slides outline

Add these slides to the same deck after Week 6.

---

## Slide 23 — Ablation motivation

**Title:** Week 7 — How many early cycles do we need?

**Bullets:**
- **Question:** if you only observe the first **N** cycles, how well can you predict **EOL**?
- **Windows:** *N* = **20**, **50**, **100** (same split: **94 / 20 / 20**, `cell_split.csv`)
- **Two models:** **XGBoost** (tabular features valid at *N*) and **GRU** (first *N* cycles × 4 channels)
- **Fair comparison:** feature subsets exclude columns that need future cycles (e.g. no ΔV(Q) at *N* = 20)
- Week 6 monotonic GRU **not** repeated — focus on data window, not architecture tweak

**Report & docs:** `docs/week07/README.md` · GitHub `docs/week07`

---

## Slide 24 — Feature / sequence setup

**Title:** What changes at each N?

| N | XGBoost features | GRU input | ΔV(Q) |
|---|------------------|-----------|-------|
| 20 | 12 | 20 × 4 channels | No |
| 50 | 28 | 50 × 4 channels | c10→c50 |
| 100 | 44 | 100 × 4 channels | c10→c50 + c10→c100 |

**Bullets:**
- XGBoost: subset of `cell_features.csv` via `features_for_window(N)`
- GRU: same 16-combo hyperparameter grid as Week 5; best on **validation MAE**
- *N* = 100 should **reproduce** Week 4 XGBoost (about **85** MAE) and Week 5 GRU (about **111** MAE)

**Notebook:** `notebooks/10_early_cycle_ablation.ipynb` · GRU script: `scripts/run_gru_ablation.py`

---

## Slide 25 — Test-set results

**Title:** Early-cycle ablation — test MAE (20 cells)

| N | XGBoost MAE | GRU MAE |
|---|-------------|---------|
| 20 | 167 | **144** |
| 50 | **107** | 143 |
| 100 | **85** | 110 |

**Bullets:**
- **XGBoost** improves sharply with *N* — ΔV(Q) and longer windows matter (167 → 85 cycles)
- **GRU** flat at 20–50, then drops at 100 — may need longer sequences on 94 train cells
- **N = 20:** GRU beats XGBoost (no voltage-curve features for tabular model)
- **N = 100:** XGBoost still best (about **85** vs about **110** cycles) — same story as Weeks 4–5
- Small test set → indicative, not definitive

**Figure:** `ablation_early_cycles.png`

---

## Slide 26 — Week 7 summary & next steps

**Title:** Week 7 complete → Week 8 final deliverables

**Bullets:**
- Ran 3-window ablation; saved six metrics JSON files + comparison figure
- **Headline:** more early cycles help XGBoost most; GRU needs about 100 cycles to match prior Week 5 performance
- **Week 8:** merge report PDF (8–12 pages), trim slides to **10–15** total (`FINAL_DECK.md`), repo polish

---

## Speaker notes (45 sec)

Week 7 asked a practical question: how much early data do you need before EOL prediction stabilizes? We trained the same two model families at twenty, fifty, and one hundred cycles, carefully dropping features that would require seeing the future. XGBoost improved a lot as we added cycles and voltage-curve statistics—test error fell from about 167 cycles at twenty cycles to about 85 at one hundred, matching our Week 4 baseline. The GRU was surprisingly stable between twenty and fifty cycles, then improved at one hundred. At the shortest window, the sequence model actually beat XGBoost because the tree model lost its voltage features entirely. But at one hundred cycles, XGBoost is still the champion. Next we wrap the report and slides for the final presentation.

---

## Anticipated Q&A (short)

| Question | Answer |
|----------|--------|
| Why not monotonic GRU? | Week 7 isolates **window length**, not Week 6’s SOH constraint. |
| Is N=100 a sanity check? | Yes — should match Week 4/5 metrics within rounding. |
| Why subprocess for GRU? | Jupyter kernel stale-code / Mac thread issues; see notebook Step C notes. |
| Best model overall? | XGBoost at N=100 (about 85 cycles test MAE). |
| Minimum viable window? | Depends on model: XGBoost needs about 50+ cycles and ΔV(Q) for under about 110 MAE. |
