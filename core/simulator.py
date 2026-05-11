"""
Simulator — Orchestrates data loading and decision execution.
"""

import pandas as pd
from config.settings import DATA_PATH
from core.decision_engine import run_decisions


REQUIRED_COLUMNS = [
    "latency_ms", "energy_J", "workload_scaled",
    "resource_utilization_pct", "Vehicle_Priority",
    "offline_mode", "handover_latency_ms", "queue_length",
    "task_success_offline",
]


def load_dataset() -> pd.DataFrame:
    """Load and validate the simulation dataset."""
    print(f"[Simulator] Loading dataset: {DATA_PATH}")
    df = pd.read_csv(DATA_PATH)

    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Dataset missing required columns: {missing}")

    print(f"[Simulator] Loaded {len(df):,} records | {df.shape[1]} columns")
    return df


def run_simulation(df: pd.DataFrame) -> pd.DataFrame:
    """
    Execute the full AI-VFC simulation over all dataset rows.

    Steps:
      1. Apply decision engine (cost-based target selection).
      2. Annotate results with per-row metadata.
    """
    print("[Simulator] Running task-offloading simulation …")
    result = run_decisions(df)
    print(f"[Simulator] Simulation complete — {len(result):,} tasks decided.")
    return result
