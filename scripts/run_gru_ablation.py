#!/usr/bin/env python3
"""Week 7 GRU ablation — run from terminal or notebook (!python scripts/run_gru_ablation.py).

Usage:
    python scripts/run_gru_ablation.py --smoke-test   # 1 combo, 1 epoch, N=20 (~5s)
    python scripts/run_gru_ablation.py              # full 3×16 grid
"""
from __future__ import annotations

import argparse
import json
import os
import time
from pathlib import Path

os.environ.setdefault("OMP_NUM_THREADS", "4")
os.environ.setdefault("MKL_NUM_THREADS", "4")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "4")

import numpy as np
import pandas as pd
import torch
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.preprocessing import StandardScaler
from torch import nn
from torch.utils.data import DataLoader, TensorDataset

ROOT = Path(__file__).resolve().parents[1]

RANDOM_STATE = 42
CYCLE_MIN = 1
TARGET = "EOL"
WINDOW_CYCLES = (20, 50, 100)
SEQUENCE_COLS = (
    "soh",
    "dc_internal_resistance",
    "energy_efficiency",
    "temperature_average",
)
N_CHANNELS = len(SEQUENCE_COLS)
GRU_BATCH_SIZE = 16
GRU_MAX_EPOCHS = 200
GRU_PATIENCE = 20
GRU_PARAM_GRID = [
    {"hidden_size": h, "num_layers": l, "dropout": d, "learning_rate": lr}
    for h in (32, 64)
    for l in (1, 2)
    for d in (0.1, 0.2)
    for lr in (1e-3, 3e-4)
]


def regression_metrics(y_true, y_pred) -> dict[str, float]:
    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)
    return {
        "mae": float(mean_absolute_error(y_true, y_pred)),
        "rmse": float(np.sqrt(mean_squared_error(y_true, y_pred))),
        "mape": float(np.mean(np.abs((y_true - y_pred) / y_true)) * 100),
    }


class GRUEOLRegressor(nn.Module):
    def __init__(self, hidden_size: int, num_layers: int, dropout: float) -> None:
        super().__init__()
        gru_dropout = dropout if num_layers > 1 else 0.0
        self.gru = nn.GRU(
            N_CHANNELS, hidden_size, num_layers=num_layers,
            batch_first=True, dropout=gru_dropout,
        )
        self.dropout = nn.Dropout(dropout)
        self.head = nn.Linear(hidden_size, 1)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        out, _ = self.gru(x)
        return self.head(self.dropout(out[:, -1, :])).squeeze(-1)


def build_tensors(data: pd.DataFrame, summary: pd.DataFrame, seq_len: int) -> np.ndarray:
    cycle_max = CYCLE_MIN + seq_len - 1
    sequences = []
    for row in data.itertuples(index=False):
        g = summary[
            (summary["file_id"] == row.file_id) & (summary["cycle_index"] <= cycle_max)
        ].sort_values("cycle_index")
        expected = np.arange(CYCLE_MIN, cycle_max + 1)
        if not np.array_equal(g["cycle_index"].to_numpy(), expected):
            raise ValueError(f"{row.file_id}: missing cycles for N={seq_len}")
        soh = g["discharge_capacity"].to_numpy(float) / row.initial_capacity
        sequences.append(np.column_stack([
            soh,
            g["dc_internal_resistance"].to_numpy(float),
            g["energy_efficiency"].to_numpy(float),
            g["temperature_average"].to_numpy(float),
        ]))
    return np.stack(sequences)


def train_gru_model(
    X_train, y_train_scaled, y_train_raw, X_val, y_val_raw,
    y_mean, y_std, hidden_size, num_layers, dropout, learning_rate,
    combo_label: str = "", max_epochs: int | None = None,
) -> tuple[GRUEOLRegressor, float]:
    torch.manual_seed(RANDOM_STATE)
    model = GRUEOLRegressor(hidden_size, num_layers, dropout)
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
    loss_fn = nn.MSELoss()
    ds = TensorDataset(
        torch.tensor(X_train, dtype=torch.float32),
        torch.tensor(y_train_scaled, dtype=torch.float32),
    )
    loader = DataLoader(ds, batch_size=GRU_BATCH_SIZE, shuffle=True, num_workers=0)
    n_epochs = GRU_MAX_EPOCHS if max_epochs is None else max_epochs
    prefix = f"    {combo_label} " if combo_label else "    "
    t0 = time.perf_counter()
    best_val_mae = float("inf")
    best_state = None
    epochs_no_improve = 0

    for epoch in range(1, n_epochs + 1):
        model.train()
        for xb, yb in loader:
            optimizer.zero_grad()
            loss_fn(model(xb), yb).backward()
            optimizer.step()

        model.eval()
        with torch.no_grad():
            pred = model(torch.tensor(X_val, dtype=torch.float32)).numpy()
        val_mae = float(np.abs(pred * y_std + y_mean - y_val_raw).mean())

        improved = val_mae < best_val_mae - 1e-4
        if improved:
            best_val_mae = val_mae
            best_state = {k: v.clone() for k, v in model.state_dict().items()}
            epochs_no_improve = 0
        else:
            epochs_no_improve += 1

        flag = " *best" if improved else ""
        print(
            f"{prefix}epoch {epoch:3d}/{n_epochs}  val {val_mae:6.1f}  "
            f"patience {epochs_no_improve}/{GRU_PATIENCE}{flag}",
            flush=True,
        )

        if max_epochs is None and epochs_no_improve >= GRU_PATIENCE:
            break

    total = time.perf_counter() - t0
    print(f"{prefix}done — {epoch} epochs, best val {best_val_mae:.1f}, {total:.0f}s", flush=True)
    model.load_state_dict(best_state)
    return model, best_val_mae


def tune_and_eval_gru(seq_len: int, X: np.ndarray, y: np.ndarray, split_arr: np.ndarray, grid) -> dict:
    train_mask = split_arr == "train"
    val_mask = split_arr == "val"
    test_mask = split_arr == "test"
    scaler = StandardScaler()
    scaler.fit(X[train_mask].reshape(-1, N_CHANNELS))
    Xs = scaler.transform(X.reshape(-1, N_CHANNELS)).reshape(X.shape)
    y_mean, y_std = y[train_mask].mean(), y[train_mask].std()
    y_scaled = (y - y_mean) / y_std

    best_val_mae = float("inf")
    best_params = None
    best_model = None
    window_t0 = time.perf_counter()

    for i, params in enumerate(grid, start=1):
        label = f"[{i}/{len(grid)}]"
        print(f"  {label} h={params['hidden_size']} layers={params['num_layers']} "
              f"dropout={params['dropout']} lr={params['learning_rate']}", flush=True)
        model, val_mae = train_gru_model(
            Xs[train_mask], y_scaled[train_mask], y[train_mask],
            Xs[val_mask], y[val_mask], y_mean, y_std,
            combo_label=label, **params,
        )
        if val_mae < best_val_mae:
            best_val_mae = val_mae
            best_params = params
            best_model = model

    def predict(model, X_part):
        model.eval()
        with torch.no_grad():
            p = model(torch.tensor(X_part, dtype=torch.float32)).numpy()
        return p * y_std + y_mean

    y_pred_train = predict(best_model, Xs[train_mask])
    y_pred_val = predict(best_model, Xs[val_mask])
    y_pred_test = predict(best_model, Xs[test_mask])

    print(f"  window N={seq_len}: done in {time.perf_counter() - window_t0:.0f}s", flush=True)
    return {
        "model": "gru_sequence",
        "window_cycles": seq_len,
        "sequence_len": seq_len,
        "channels": list(SEQUENCE_COLS),
        "best_params": best_params,
        "split": {"train": int(train_mask.sum()), "val": int(val_mask.sum()), "test": int(test_mask.sum()), "random_state": RANDOM_STATE},
        "train": regression_metrics(y[train_mask], y_pred_train),
        "val": regression_metrics(y[val_mask], y_pred_val),
        "test": regression_metrics(y[test_mask], y_pred_test),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke-test", action="store_true", help="1 combo, 1 epoch, N=20 only")
    args = parser.parse_args()

    torch.manual_seed(RANDOM_STATE)
    torch.set_num_threads(4)

    cell_features = pd.read_csv(ROOT / "data/processed/cell_features.csv")
    split_df = pd.read_csv(ROOT / "data/processed/cell_split.csv")
    data = cell_features.merge(split_df[["file_id", "split"]], on="file_id")
    y = data[TARGET].to_numpy(float)
    split_arr = data["split"].to_numpy()
    summary = pd.read_csv(
        ROOT / "data/processed/cycle_summary.csv",
        usecols=["file_id", "cycle_index", "discharge_capacity",
                 "dc_internal_resistance", "energy_efficiency", "temperature_average"],
    )
    summary = summary[summary["cycle_index"] >= CYCLE_MIN]

    metrics_dir = ROOT / "results/metrics"
    metrics_dir.mkdir(parents=True, exist_ok=True)

    if args.smoke_test:
        n = 20
        print(f"=== SMOKE TEST N={n} ===", flush=True)
        X = build_tensors(data, summary, n)
        X_tr, y_tr_s, y_tr, X_va, y_va, y_mean, y_std = _scale_split(X, y, split_arr)
        _, val_mae = train_gru_model(
            X_tr, y_tr_s, y_tr, X_va, y_va, y_mean, y_std,
            combo_label="[smoke]",
            max_epochs=1,
            **GRU_PARAM_GRID[0],
        )
        print(f"Smoke test OK — val MAE {val_mae:.1f}", flush=True)
        return 0

    total_t0 = time.perf_counter()
    for wi, n in enumerate(WINDOW_CYCLES, start=1):
        print(f"\n=== GRU window {wi}/{len(WINDOW_CYCLES)}  N={n} ===", flush=True)
        X = build_tensors(data, summary, n)
        grid = GRU_PARAM_GRID
        metrics = tune_and_eval_gru(n, X, y, split_arr, grid)
        out = metrics_dir / f"gru_sequence_n{n}.json"
        out.write_text(json.dumps(metrics, indent=2))
        print(f"N={n}: test MAE {metrics['test']['mae']:.1f} — saved {out}", flush=True)

    print(f"\nAll windows done in {time.perf_counter() - total_t0:.0f}s", flush=True)
    return 0


def _scale_split(X, y, split_arr):
    train_mask = split_arr == "train"
    val_mask = split_arr == "val"
    scaler = StandardScaler()
    scaler.fit(X[train_mask].reshape(-1, N_CHANNELS))
    Xs = scaler.transform(X.reshape(-1, N_CHANNELS)).reshape(X.shape)
    y_mean, y_std = y[train_mask].mean(), y[train_mask].std()
    y_scaled = (y - y_mean) / y_std
    return (
        Xs[train_mask], y_scaled[train_mask], y[train_mask],
        Xs[val_mask], y[val_mask], y_mean, y_std,
    )


if __name__ == "__main__":
    raise SystemExit(main())
