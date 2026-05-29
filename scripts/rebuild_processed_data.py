"""Rebuild cell_targets and cycle_summary using Week 2 dedupe policy."""
import glob
import json
import os
import time

import pandas as pd

from dedupe_policy import is_kept_file

TARGETS_PATH = "data/cell_targets.csv"
SUMMARY_PATH = "data/processed/cycle_summary.csv"


def compute_eol(summary: pd.DataFrame) -> tuple[int, float] | None:
    s = summary[summary["cycle_index"] >= 1]
    if len(s) == 0:
        return None
    initial_cap = s["discharge_capacity"].iloc[0]
    threshold = 0.8 * initial_cap
    below = s[s["discharge_capacity"] < threshold]
    eol = int(below.iloc[0]["cycle_index"]) if len(below) else int(s["cycle_index"].iloc[-1])
    return eol, float(initial_cap)


def main():
    files = sorted(glob.glob("data/raw/FastCharge*.json"))
    if not files:
        raise SystemExit("No JSON files in data/raw/")

    os.makedirs("data/processed", exist_ok=True)
    targets_rows = []
    summary_parts = []
    t0 = time.perf_counter()

    for i, path in enumerate(files):
        file_id = os.path.basename(path)
        kept = is_kept_file(file_id)

        with open(path, encoding="utf-8") as f:
            data = json.load(f)

        summary = pd.DataFrame(data["summary"])
        summary["file_id"] = file_id
        summary["cell_id"] = data["barcode"]

        eol_row = compute_eol(summary)
        if eol_row is not None and kept:
            eol, initial_cap = eol_row
            targets_rows.append(
                {
                    "file_id": file_id,
                    "cell_id": data["barcode"],
                    "EOL": eol,
                    "initial_capacity": initial_cap,
                }
            )

        if kept:
            summary_parts.append(summary)

        if (i + 1) % 20 == 0 or i + 1 == len(files):
            print(f"[{i + 1}/{len(files)}] {file_id} ({'keep' if kept else 'skip'})")

    targets = pd.DataFrame(targets_rows)
    cycle_summary = pd.concat(summary_parts, ignore_index=True)
    cols = ["file_id", "cell_id"] + [
        c for c in cycle_summary.columns if c not in ("file_id", "cell_id")
    ]
    cycle_summary = cycle_summary[cols]

    targets.to_csv(TARGETS_PATH, index=False)
    cycle_summary.to_csv(SUMMARY_PATH, index=False)

    elapsed = time.perf_counter() - t0
    print()
    print(f"Wrote {TARGETS_PATH}: {len(targets)} rows, {targets['cell_id'].nunique()} unique barcodes")
    print(f"Wrote {SUMMARY_PATH}: {len(cycle_summary):,} rows, {cycle_summary['file_id'].nunique()} files")
    print(f"Elapsed: {elapsed / 60:.1f} min")


if __name__ == "__main__":
    main()
