"""Merge cell_targets (EOL labels) into cycle_summary (per-cycle metrics)."""
import pandas as pd

SUMMARY_PATH = "data/processed/cycle_summary.csv"
TARGETS_PATH = "data/cell_targets.csv"
OUTPUT_PATH = "data/processed/cycle_summary_labeled.csv"


def main():
    summary = pd.read_csv(SUMMARY_PATH)
    targets = pd.read_csv(TARGETS_PATH)

    n_dup = targets["cell_id"].duplicated().sum()
    if n_dup:
        print(f"Warning: {n_dup} duplicate cell_id rows in targets — keeping first row per cell_id.")
        targets = targets.drop_duplicates(subset="cell_id", keep="first")

    merged = summary.merge(targets, on="cell_id", how="left")
    merged.to_csv(OUTPUT_PATH, index=False)
    print(f"Saved {OUTPUT_PATH} ({len(merged):,} rows, {len(merged.columns)} cols)")


if __name__ == "__main__":
    main()
