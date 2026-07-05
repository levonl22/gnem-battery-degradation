"""Poster-sized correlation heatmap — top features + EOL only."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
FEATURES_PATH = ROOT / "data/processed/cell_features.csv"
OUT = ROOT / "results/figures/feature_correlation_poster.png"

LABEL_COLS = ("file_id", "cell_id", "EOL", "initial_capacity")
TOP_N = 12


def main() -> None:
    df = pd.read_csv(FEATURES_PATH)
    feature_cols = [c for c in df.columns if c not in LABEL_COLS]

    rows = []
    for col in feature_cols:
        r = df[col].corr(df["EOL"], method="pearson")
        rows.append({"feature": col, "pearson": r, "abs_pearson": abs(r)})
    ranked = pd.DataFrame(rows).sort_values("abs_pearson", ascending=False)
    top = ranked.head(TOP_N)["feature"].tolist()
    cols = top + ["EOL"]
    matrix = df[cols].corr(method="pearson")

    fig, ax = plt.subplots(figsize=(10, 8))
    im = ax.imshow(matrix.values, cmap="RdBu_r", vmin=-1, vmax=1, aspect="auto")
    ax.set_xticks(range(len(cols)))
    ax.set_yticks(range(len(cols)))
    ax.set_xticklabels(cols, rotation=45, ha="right", fontsize=13)
    ax.set_yticklabels(cols, fontsize=13)
    ax.set_title(
        f"Which early-cycle signals track battery lifetime?\n"
        f"Top {TOP_N} features + EOL · Pearson r · n = 134 cells",
        fontsize=16,
        pad=12,
    )
    cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label("Pearson r", fontsize=12)
    cbar.ax.tick_params(labelsize=11)

    fig.tight_layout()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
