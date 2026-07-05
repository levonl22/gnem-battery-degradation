# Final presentation (Week 8)

Target: **12 slides** trimmed from the 26-slide weekly deck. **No Week 8 check-in slide.**

| File | Purpose |
|------|---------|
| [`final_deck_notes.md`](final_deck_notes.md) | Full copy-paste outline + figure list + trim map |
| [`final_deck_pandoc.md`](final_deck_pandoc.md) | Pandoc source for PPTX regeneration |
| [`results/gnem_battery_slides.pptx`](../results/gnem_battery_slides.pptx) | **Canonical final deck** (hand-edited in PowerPoint) |

## Slide order

1. Title  
2. Problem & motivation  
3. Dataset & pipeline  
4. EOL distribution + example fade curve  
5. Feature engineering overview  
6. ML baselines — metrics  
7. ML — pred vs true EOL  
8. GRU — pred vs true EOL  
9. Monotonic SOH constraint  
10. Ablation (20 / 50 / 100 cycles)  
11. Limitations  
12. Conclusions & future work  

**Export PDF:** File → Download → PDF → `results/gnem_battery_slides.pdf`

**Regenerate PPTX** (12 slides, embedded figures):

```bash
source .venv/bin/activate
pip install python-pptx   # once
python scripts/generate_final_slides.py
```

Alternative (pandoc, may split overflow onto extra slides):

```bash
cd docs/slides
pandoc final_deck_pandoc.md -o ../../results/gnem_battery_slides.pptx --resource-path=.:../..
```

Weekly outlines (source material): [week01_notes.md](week01_notes.md) … [week07_notes.md](week07_notes.md)
