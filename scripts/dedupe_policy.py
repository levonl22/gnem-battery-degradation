"""Duplicate-barcode policy (Week 2). See docs/week02/duplicate_barcode_policy.md."""

import os

# Short / duplicate runs — keep the longer file in each barcode pair.
DROP_FILES = frozenset(
    {
        "FastCharge_000004_CH1_structure.json",
        "FastCharge_000004_CH2_structure.json",
        "FastCharge_000004_CH3_structure.json",
        "FastCharge_000026_CH5_structure.json",
        "FastCharge_000026_CH6_structure.json",
    }
)

# Formation-only partial test (no cycle_index >= 1).
PARTIAL_FILE = "FastCharge_000002_CH26_structure.json"


def file_basename(path_or_name: str) -> str:
    return os.path.basename(path_or_name)


def is_kept_file(path_or_name: str) -> bool:
    name = file_basename(path_or_name)
    return name not in DROP_FILES and name != PARTIAL_FILE
