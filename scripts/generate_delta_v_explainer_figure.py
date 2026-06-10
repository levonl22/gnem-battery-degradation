"""Generate ΔV(Q) explainer figure for slides and report (Week 3)."""
import json
import os
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

CYCLE_EARLY = 10
CYCLE_LATE = 100
N_GRID = 500
OUTPUT = Path("results/figures/delta_v_q_explainer.png")


def discharge_qv(curves, cycle_index):
    ci = np.asarray(curves["cycle_index"])
    st = np.asarray(curves["step_type"])
    mask = (ci == cycle_index) & (st == "discharge")
    q = np.asarray(curves["discharge_capacity"], dtype=float)[mask]
    v = np.asarray(curves["voltage"], dtype=float)[mask]
    ok = np.isfinite(q) & np.isfinite(v)
    q, v = q[ok], v[ok]
    if len(q) < 2:
        return None, None
    order = np.argsort(q)
    return q[order], v[order]


def delta_v_curve(curves, cycle_early, cycle_late, n_grid=N_GRID):
    q_early, v_early = discharge_qv(curves, cycle_early)
    q_late, v_late = discharge_qv(curves, cycle_late)
    if q_early is None or q_late is None:
        return None

    q_hi = min(q_early.max(), q_late.max())
    q_lo = max(q_early.min(), q_late.min())
    if q_hi <= q_lo:
        return None

    grid = np.linspace(q_lo, q_hi, n_grid)
    v_early_i = np.interp(grid, q_early, v_early)
    v_late_i = np.interp(grid, q_late, v_late)
    return grid, v_early_i, v_late_i, v_late_i - v_early_i


def main():
    os.makedirs(OUTPUT.parent, exist_ok=True)
    targets = pd.read_csv("data/cell_targets.csv")
    row = targets.iloc[0]
    json_path = Path("data/raw") / row["file_id"]
    if not json_path.is_file():
        raise FileNotFoundError(
            f"Missing {json_path}. Place raw JSON under data/raw/ and retry."
        )

    with open(json_path) as f:
        payload = json.load(f)
    curves = payload["cycles_interpolated"]

    result = delta_v_curve(curves, CYCLE_EARLY, CYCLE_LATE)
    if result is None:
        raise RuntimeError("Could not build ΔV(Q) curves for the example cell.")

    grid, v_early, v_late, delta_v = result
    q_mark = float(np.median(grid))
    v10_mark = float(np.interp(q_mark, grid, v_early))
    v100_mark = float(np.interp(q_mark, grid, v_late))
    dv_mark = v100_mark - v10_mark

    fig, (ax_v, ax_dv) = plt.subplots(2, 1, figsize=(8, 7), sharex=True)

    ax_v.plot(grid, v_early, color="steelblue", linewidth=1.5, label=f"Cycle {CYCLE_EARLY}")
    ax_v.plot(grid, v_late, color="darkorange", linewidth=1.5, label=f"Cycle {CYCLE_LATE}")
    ax_v.axvline(q_mark, color="gray", linestyle=":", linewidth=1)
    ax_v.plot([q_mark, q_mark], [v10_mark, v100_mark], color="black", linewidth=2, marker="o", markersize=5)
    ax_v.annotate(
        f"ΔV = {dv_mark:+.3f} V\n(at Q = {q_mark:.2f} Ah)",
        xy=(q_mark, (v10_mark + v100_mark) / 2),
        xytext=(q_mark + 0.08, (v10_mark + v100_mark) / 2 + 0.04),
        arrowprops={"arrowstyle": "->", "color": "black"},
        fontsize=9,
    )
    ax_v.set_ylabel("Discharge voltage (V)")
    ax_v.set_title(
        f"ΔV(Q) example — {row['cell_id']}  (EOL = {int(row['EOL'])} cycles)\n"
        "Same discharge capacity Q on both cycles; compare voltage curve shape"
    )
    ax_v.legend(loc="upper right")
    ax_v.grid(True, alpha=0.3)

    ax_dv.axhline(0, color="gray", linewidth=0.8)
    ax_dv.plot(grid, delta_v, color="purple", linewidth=1.5, label=f"V{CYCLE_LATE}(Q) − V{CYCLE_EARLY}(Q)")
    ax_dv.axvline(q_mark, color="gray", linestyle=":", linewidth=1)
    ax_dv.scatter([q_mark], [dv_mark], color="black", s=30, zorder=5)
    ax_dv.set_xlabel("Discharge capacity Q (Ah)")
    ax_dv.set_ylabel("ΔV (V)")
    ax_dv.legend(loc="best")
    ax_dv.grid(True, alpha=0.3)

    fig.tight_layout()
    fig.savefig(OUTPUT, dpi=150)
    plt.close(fig)
    print(f"Saved {OUTPUT}")


if __name__ == "__main__":
    main()
