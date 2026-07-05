# Week 8 deliverables (complete)

**Fellowship wrap-up** — final report, slides, showcase poster, repo polish. No new modeling.

| File | Status |
|------|--------|
| `docs/report/08_conclusion.md` | Done |
| `docs/report/09_references.md` | Verified |
| `results/gnem_battery_report.pdf` | Done (from `docs/report/` §01–09) |
| `results/gnem_battery_slides.pdf` + `.pptx` | Done (12-slide final deck) |
| `results/LAU_gnem_battery_poster.pdf` | Done (GNEM showcase poster, July 24) |
| `results/figures/feature_correlation_poster.png` | Done — poster heatmap (top 12 features) |
| `results/figures/github_qr.png` | Done |
| `requirements.txt` | `xgboost>=2.0,<3` for metric reproduction |
| `.gitignore` | `.venv/` added |
| `docs/slides/final_deck_notes.md`, `FINAL_DECK.md` | Done |

---

## Headline result

**XGBoost** at *N* = 100 early cycles — about **85 cycles** test MAE (about **11%** MAPE, 20-cell holdout). Week 7 ablation: tabular error **167 → 107 → 85** as the window grows; GRU about **144 → 143 → 110**.

---

## Final deliverables

| Artifact | Path |
|----------|------|
| Report PDF | `results/gnem_battery_report.pdf` |
| Slides PDF | `results/gnem_battery_slides.pdf` |
| Showcase poster PDF | `results/LAU_gnem_battery_poster.pdf` |
| Report source | `docs/report/01_introduction.md` … `09_references.md` |
| Slide outline | `docs/slides/final_deck_notes.md` |

**Report merge (regenerate):**

```bash
cd docs/report
pandoc 01_introduction.md … 09_references.md -o ../../results/gnem_battery_report.docx --resource-path=.:../..
# Export PDF from Word, or install LaTeX for direct pandoc PDF
```

**Poster assets:**

```bash
source .venv/bin/activate
python scripts/generate_poster_heatmap.py   # feature_correlation_poster.png
# Poster layout: edit GNEM template in PowerPoint; export LAU_gnem_battery_poster.pdf
```

---

## Showcase (external)

- **GNEM Summer Fellowship Showcase** — Friday, July 24, 2026 · Georgia Center, Athens · poster session 11:30 a.m.
- Submit poster PDF to GNEM about **one week before** the event (target ~July 17).
- Week 8 mentor email: fellowship complete + links to report, slides, repo (see `docs/PROJECT_CONTEXT.md` §Week 8 if local).

---

## Repo polish (this week)

- Reproducibility: pin xgboost 2.x; smoke test `scripts/run_gru_ablation.py --smoke-test`
- `scripts/generate_final_slides.py`, `generate_poster.py`, `generate_poster_heatmap.py` (optional regeneration helpers)
- `docs/future_work.md` — post-fellowship ideas (not required for Week 8 plan)
