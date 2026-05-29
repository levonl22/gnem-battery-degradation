"""Merge cell_targets (EOL labels) into cycle_summary (per-cycle metrics)."""
import pandas as pd

SUMMARY_PATH = "data/processed/cycle_summary.csv"
TARGETS_PATH = "data/cell_targets.csv"
OUTPUT_PATH = "data/processed/cycle_summary_labeled.csv"


def main():
    summary = pd.read_csv(SUMMARY_PATH)
    targets = pd.read_csv(TARGETS_PATH)

    merge_key = "file_id" if "file_id" in summary.columns and "file_id" in targets.columns else "cell_id"
    if merge_key == "cell_id" and targets["cell_id"].duplicated().any():
        raise SystemExit("Duplicate cell_id in targets — rebuild with Week 2 dedupe policy.")

    merged = summary.merge(targets, on=merge_key, how="left")
    merged.to_csv(OUTPUT_PATH, index=False)
    print(f"Saved {OUTPUT_PATH} ({len(merged):,} rows, {len(merged.columns)} cols)")


if __name__ == "__main__":
    main()
