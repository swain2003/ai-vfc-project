"""
AI-VFC Simulation — Main Entry Point
=====================================
Run with:   python main.py

Pipeline
--------
1. Load dataset (data/ai_vfc_offline_extended.csv)
2. Run DRL-inspired cost-based task offloading simulation
3. Compute performance metrics
4. Print formatted report
5. Save results/metrics.txt, results/metrics.json,
         results/simulation_output.csv, results/plots/

Results are fully computed at runtime — the results/ folder is
empty until this script executes.
"""

import sys
import time

# ── Make sure project root is on PYTHONPATH ───────────────────────────────────
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.simulator   import load_dataset, run_simulation
from evaluation       import compute_metrics
from utils            import (
    print_report, save_metrics_txt, save_metrics_json,
    save_simulation_csv, generate_plots,
)


def main():
    print("\n" + "=" * 65)
    print(" AI-Integrated Vehicular Fog Computing (AI-VFC) Simulation")
    print("=" * 65 + "\n")

    t0 = time.time()

    # ── Step 1: Load ──────────────────────────────────────────────────────────
    df = load_dataset()

    # ── Step 2: Simulate ─────────────────────────────────────────────────────
    sim_df = run_simulation(df)

    # ── Step 3: Metrics ───────────────────────────────────────────────────────
    print("[Main] Computing performance metrics …")
    metrics = compute_metrics(sim_df)

    # ── Step 4: Report ───────────────────────────────────────────────────────
    report = print_report(metrics)

    # ── Step 5: Save ─────────────────────────────────────────────────────────
    print("[Main] Saving results …")
    save_metrics_txt(report=report, metrics=metrics)
    save_metrics_json(metrics=metrics)
    save_simulation_csv(sim_df=sim_df)
    generate_plots(sim_df=sim_df, metrics=metrics)

    elapsed = time.time() - t0
    print(f"\n[Main] Done in {elapsed:.2f}s — all outputs in results/\n")


if __name__ == "__main__":
    main()
