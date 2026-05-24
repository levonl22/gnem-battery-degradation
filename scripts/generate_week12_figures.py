"""Generate Week 1-2 EDA figures for slides and report."""
import os

import matplotlib.pyplot as plt
import pandas as pd

os.makedirs("results/figures", exist_ok=True)

targets = pd.read_csv("data/cell_targets.csv")
summary = pd.read_csv("data/processed/cycle_summary.csv")

fig, ax = plt.subplots(figsize=(8, 4))
ax.hist(targets["EOL"], bins=30, edgecolor="white", color="steelblue")
ax.axvline(
    targets["EOL"].median(),
    color="red",
    linestyle="--",
    label=f"median={targets['EOL'].median():.0f}",
)
ax.set_xlabel("EOL cycle (80% threshold)")
ax.set_ylabel("Number of cells")
ax.set_title("End-of-life distribution (cell_targets.csv)")
ax.legend()
fig.tight_layout()
fig.savefig("results/figures/eol_distribution.png", dpi=150)
plt.close()

cid = targets["cell_id"].iloc[0]
s = summary[(summary["cell_id"] == cid) & (summary["cycle_index"] >= 1)].sort_values(
    "cycle_index"
)
ic = s["discharge_capacity"].iloc[0]
thr = 0.8 * ic
eol = targets.loc[targets["cell_id"] == cid, "EOL"].iloc[0]

fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(s["cycle_index"], s["discharge_capacity"], linewidth=1)
ax.axhline(thr, color="red", linestyle="--", label="80% threshold")
ax.axvline(eol, color="orange", linestyle=":", label=f"EOL={eol:.0f}")
ax.set_xlabel("Cycle index")
ax.set_ylabel("Discharge capacity (Ah)")
ax.set_title(f"Capacity fade — {cid}")
ax.legend()
ax.grid(True, alpha=0.3)
fig.tight_layout()
fig.savefig("results/figures/capacity_fade_example.png", dpi=150)
plt.close()

print("Saved results/figures/eol_distribution.png")
print("Saved results/figures/capacity_fade_example.png")
