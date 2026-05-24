# Report (8–12 pages final)

Section files are written **week by week**. Week 8: merge into one PDF.

## Sections

| File | Status |
|------|--------|
| `01_introduction.md` | Week 1 |
| `02_related_work.md` | Week 1 |
| `03_data.md` | Week 1–2 (EDA added Week 2) |
| `04_features.md` | Week 3 |
| `05_methods.md` | Weeks 4–6 |
| `06_results.md` | Weeks 4–7 |
| `07_discussion.md` | Week 7 |
| `08_conclusion.md` | Week 8 |
| `09_references.md` | Ongoing |

## Export to PDF (Week 8)

**Option A — Pandoc (recommended):**

```bash
cd docs/report
pandoc 01_introduction.md 02_related_work.md 03_data.md 04_features.md 05_methods.md 06_results.md 07_discussion.md 08_conclusion.md 09_references.md -o ../../results/gnem_battery_report.pdf --resource-path=.:../..
```

**Option B — Word:** Paste sections in order into Google Docs / Word; export PDF.

**Option C — VS Code:** Markdown PDF extension on merged file.

Before export: replace `[Your name]`, fill placeholder sections (04–06, 08), verify figures in `results/figures/` render.

## Page budget (target 8–12)

| Section | ~Pages |
|---------|--------|
| 1 Introduction | 1–1.5 |
| 2 Related work | 1–1.5 |
| 3 Data + EDA | 1.5–2 |
| 4 Features | 1–1.5 |
| 5 Methods | 1.5–2 |
| 6 Results | 2–3 |
| 7 Discussion | 0.5–1 |
| 8 Conclusion | 0.5 |
| 9 References | 0.5 |
