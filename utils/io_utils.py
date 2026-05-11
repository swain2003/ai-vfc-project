"""
I/O Utilities — Saving results, printing the formatted report, generating plots.
"""

import os
import json
import textwrap
import pandas as pd
import matplotlib
matplotlib.use("Agg")  # non-interactive backend
import matplotlib.pyplot as plt

from config.settings import RESULTS_DIR, TARGET_RANGES, PLOT_DPI, PLOT_STYLE


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def _ensure_results_dir():
    os.makedirs(RESULTS_DIR, exist_ok=True)


def _pass_fail(value: float, lo: float, hi: float) -> str:
    return "PASS" if lo <= value <= hi else "FAIL"


# ─────────────────────────────────────────────────────────────────────────────
# Console report
# ─────────────────────────────────────────────────────────────────────────────

def print_report(metrics: dict) -> str:
    """Print and return the formatted performance report."""

    tr = TARGET_RANGES

    rows = [
        ("Latency (ms)",          metrics["latency_ms"],
         f"[{tr['latency_ms'][0]} – {tr['latency_ms'][1]}]",
         _pass_fail(metrics["latency_ms"], *tr["latency_ms"])),

        ("Energy (J)",            metrics["energy_J"],
         f"[{tr['energy_J'][0]} – {tr['energy_J'][1]}]",
         _pass_fail(metrics["energy_J"], *tr["energy_J"])),

        ("Utilization (%)",       metrics["utilization_pct"],
         f"[{tr['utilization_pct'][0]} – {tr['utilization_pct'][1]}]",
         _pass_fail(metrics["utilization_pct"], *tr["utilization_pct"])),

        ("Offload Success (%)",   metrics["offload_success_pct"],
         f"[{tr['offload_success_pct'][0]} – {tr['offload_success_pct'][1]}]",
         _pass_fail(metrics["offload_success_pct"], *tr["offload_success_pct"])),

        ("Handover Latency (ms)", metrics["handover_latency_ms"],
         f"[{tr['handover_latency_ms'][0]} – {tr['handover_latency_ms'][1]}]",
         _pass_fail(metrics["handover_latency_ms"], *tr["handover_latency_ms"])),

        ("Queue Length",          metrics["queue_length"],
         f"[~{tr['queue_length'][0]}–{tr['queue_length'][1]}]",
         _pass_fail(metrics["queue_length"], *tr["queue_length"])),

        ("Offline Success (%)",   metrics["offline_success_pct"],
         f"[{tr['offline_success_pct'][0]} – {tr['offline_success_pct'][1]}]",
         _pass_fail(metrics["offline_success_pct"], *tr["offline_success_pct"])),
    ]

    passes = sum(1 for r in rows if r[3] == "PASS")
    overall = "PASS" if passes == len(rows) else "FAIL"

    sep   = "=" * 65
    title = "AI-VFC PERFORMANCE METRICS"
    hdr   = f"{'Metric':<28}{'Value':>10}  {'Target Range':<22}{'Status'}"

    lines = [sep, title, sep, hdr, "-" * 65]
    for name, val, rng, status in rows:
        lines.append(f"{name:<28}{val:>10.3f}  {rng:<22}{status}")

    lines += [
        "-" * 65,
        f"Overall: {overall}  ({passes}/{len(rows)} metrics passing)",
        sep,
        "",
        "Execution Target Distribution:",
        f"  {metrics['target_distribution']}",
        f"  Total tasks : {metrics['n_tasks']:,}",
        f"  Offline tasks: {metrics['n_offline']:,}",
    ]

    report = "\n".join(lines)
    print("\n" + report + "\n")
    return report


# ─────────────────────────────────────────────────────────────────────────────
# File savers
# ─────────────────────────────────────────────────────────────────────────────

def save_metrics_txt(metrics: dict, report: str):
    _ensure_results_dir()
    path = os.path.join(RESULTS_DIR, "metrics.txt")
    with open(path, "w") as f:
        f.write(report)
    print(f"[IO] Saved: {path}")


def save_metrics_json(metrics: dict):
    _ensure_results_dir()
    path = os.path.join(RESULTS_DIR, "metrics.json")
    exportable = {k: v for k, v in metrics.items() if k != "target_distribution"}
    exportable["target_distribution"] = metrics["target_distribution"]
    with open(path, "w") as f:
        json.dump(exportable, f, indent=2)
    print(f"[IO] Saved: {path}")


def save_simulation_csv(sim_df: pd.DataFrame):
    _ensure_results_dir()
    path = os.path.join(RESULTS_DIR, "simulation_output.csv")
    sim_df.to_csv(path, index=False)
    print(f"[IO] Saved: {path}  ({len(sim_df):,} rows)")


# ─────────────────────────────────────────────────────────────────────────────
# Plots
# ─────────────────────────────────────────────────────────────────────────────

def _savefig(fig, filename: str):
    _ensure_results_dir()
    path = os.path.join(RESULTS_DIR, filename)
    fig.savefig(path, dpi=PLOT_DPI, bbox_inches="tight")
    plt.close(fig)
    print(f"[IO] Plot saved: {path}")


def generate_plots(sim_df: pd.DataFrame, metrics: dict):
    """Generate all summary plots and save to results/."""

    try:
        plt.style.use(PLOT_STYLE)
    except Exception:
        plt.style.use("ggplot")

    colors = {"vehicle": "#4C9BE8", "fog": "#F5A623", "cloud": "#7ED321"}

    # ── 1. Execution target distribution (bar) ─────────────────────────────
    fig, ax = plt.subplots(figsize=(6, 4))
    dist = metrics["target_distribution"]
    targets = list(dist.keys())
    counts  = [dist[t] for t in targets]
    bars = ax.bar(targets, counts, color=[colors.get(t, "grey") for t in targets],
                  edgecolor="white", linewidth=1.2)
    ax.bar_label(bars, fmt="%d", padding=4, fontsize=11)
    ax.set_title("Execution Target Distribution", fontsize=13, fontweight="bold")
    ax.set_ylabel("Number of Tasks")
    ax.set_xlabel("Execution Layer")
    _savefig(fig, "plot_target_distribution.png")

    # ── 2. Effective latency distribution by target ───────────────────────
    fig, ax = plt.subplots(figsize=(7, 4))
    for target in ("vehicle", "fog", "cloud"):
        subset = sim_df.loc[sim_df["chosen_target"] == target, "eff_latency_ms"]
        if len(subset) > 0:
            ax.hist(subset.values, bins=30, alpha=0.65, label=target,
                    color=colors.get(target, "grey"), edgecolor="none")
    ax.axvline(metrics["latency_ms"], color="red", linestyle="--",
               linewidth=1.5, label=f"Mean={metrics['latency_ms']:.1f} ms")
    ax.set_title("Effective Latency Distribution by Layer", fontsize=13, fontweight="bold")
    ax.set_xlabel("Effective Latency (ms)")
    ax.set_ylabel("Task Count")
    ax.legend()
    _savefig(fig, "plot_latency_distribution.png")

    # ── 3. Energy distribution by target ──────────────────────────────────
    fig, ax = plt.subplots(figsize=(7, 4))
    for target in ("vehicle", "fog", "cloud"):
        subset = sim_df.loc[sim_df["chosen_target"] == target, "eff_energy_J"]
        if len(subset) > 0:
            ax.hist(subset.values, bins=30, alpha=0.65, label=target,
                    color=colors.get(target, "grey"), edgecolor="none")
    ax.axvline(metrics["energy_J"], color="red", linestyle="--",
               linewidth=1.5, label=f"Mean={metrics['energy_J']:.4f} J")
    ax.set_title("Effective Energy Distribution by Layer", fontsize=13, fontweight="bold")
    ax.set_xlabel("Effective Energy (J)")
    ax.set_ylabel("Task Count")
    ax.legend()
    _savefig(fig, "plot_energy_distribution.png")

    # ── 4. Metrics summary bar chart ──────────────────────────────────────
    metric_labels = [
        "Latency\n(ms)", "Energy\n(J×100)", "Utilization\n(%)",
        "Offload\nSuccess (%)", "Handover\nLatency (ms)",
        "Queue\nLength", "Offline\nSuccess (%)"
    ]
    raw_vals = [
        metrics["latency_ms"],
        metrics["energy_J"] * 100,
        metrics["utilization_pct"],
        metrics["offload_success_pct"],
        metrics["handover_latency_ms"],
        metrics["queue_length"],
        metrics["offline_success_pct"],
    ]

    fig, ax = plt.subplots(figsize=(12, 5))
    bars = ax.bar(metric_labels, raw_vals, color="#4C9BE8", edgecolor="white", linewidth=1.2)
    ax.bar_label(bars, fmt="%.2f", padding=4, fontsize=9)
    ax.set_title("AI-VFC Simulation — Summary Metrics", fontsize=13, fontweight="bold")
    ax.set_ylabel("Value (see labels)")
    ax.set_ylim(0, max(raw_vals) * 1.15)
    _savefig(fig, "plot_metrics_summary.png")

    # ── 5. Queue length rolling average ───────────────────────────────────
    fig, ax = plt.subplots(figsize=(9, 4))
    rolling = sim_df["queue_length"].rolling(window=20, min_periods=1).mean()
    ax.plot(rolling.values, color="#4C9BE8", linewidth=1.2, alpha=0.9)
    ax.axhline(metrics["queue_length"], color="red", linestyle="--",
               linewidth=1.5, label=f"Mean={metrics['queue_length']:.2f}")
    ax.set_title("Queue Length — Rolling Mean (window=20)", fontsize=13, fontweight="bold")
    ax.set_xlabel("Task Index")
    ax.set_ylabel("Queue Length (tasks)")
    ax.legend()
    _savefig(fig, "plot_queue_length.png")

    # ── 6. Resource utilisation by priority ───────────────────────────────
    if "Vehicle_Priority" in sim_df.columns:
        fig, ax = plt.subplots(figsize=(6, 4))
        prio_util = (
            sim_df.groupby("Vehicle_Priority")["resource_utilization_pct"]
            .mean()
            .sort_index()
        )
        prio_util.plot(kind="bar", ax=ax, color="#F5A623", edgecolor="white")
        ax.set_title("Avg Resource Utilisation by Vehicle Priority",
                     fontsize=13, fontweight="bold")
        ax.set_xlabel("Vehicle Priority")
        ax.set_ylabel("Resource Utilisation (%)")
        ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
        _savefig(fig, "plot_utilisation_by_priority.png")

    # ── 7. Latency by chosen target (box plot) ─────────────────────────────
    fig, ax = plt.subplots(figsize=(7, 4))
    layer_latencies = [
        sim_df.loc[sim_df["chosen_target"] == t, "eff_latency_ms"].values
        for t in ("vehicle", "fog", "cloud")
    ]
    bp = ax.boxplot(
        [x for x in layer_latencies if len(x) > 0],
        labels=[t for t, x in zip(("vehicle", "fog", "cloud"), layer_latencies) if len(x) > 0],
        patch_artist=True,
        medianprops={"color": "red", "linewidth": 2},
    )
    for patch, color in zip(bp["boxes"], [colors["vehicle"], colors["fog"], colors["cloud"]]):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    ax.set_title("Effective Latency by Execution Layer (Box Plot)",
                 fontsize=13, fontweight="bold")
    ax.set_ylabel("Effective Latency (ms)")
    _savefig(fig, "plot_latency_boxplot.png")

    print("[IO] All plots generated.")
