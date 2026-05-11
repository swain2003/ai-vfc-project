"""
Metrics — Computes all seven AI-VFC performance metrics from simulation output.

Every metric is derived purely from the simulation result DataFrame.
No values are hardcoded or clamped.

Column dependencies (all present in sim_df after run_decisions):
  eff_latency_ms        — computed in decision_engine (METRIC_LAYER_PARAMS)
  eff_energy_J          — computed in decision_engine (METRIC_LAYER_PARAMS)
  chosen_target         — layer selected by decision engine
  is_offline            — True when offline_mode == 1
  offload_success       — raw dataset column (measured ground truth)
  resource_utilization_pct — raw dataset column
  handover_latency_ms   — raw dataset column
  queue_length          — raw dataset column
  task_success_offline  — raw dataset column
"""

import pandas as pd


def compute_metrics(sim_df: pd.DataFrame) -> dict:
    """
    Compute all seven performance KPIs from the simulation output.

    Parameters
    ----------
    sim_df : DataFrame returned by core.simulator.run_simulation()

    Returns
    -------
    dict with metric names → float values
    """

    # ── 1 & 2. Effective task latency and energy ───────────────────────────
    #    eff_latency_ms and eff_energy_J were computed in the decision engine
    #    using METRIC_LAYER_PARAMS (factors close to 1.0).
    avg_latency = sim_df["eff_latency_ms"].mean()
    avg_energy  = sim_df["eff_energy_J"].mean()

    # ── 3. Resource utilisation ────────────────────────────────────────────
    #    Use the dataset's measured utilisation for vehicle and fog tasks
    #    (nodes that actually run computation). Cloud tasks consume cloud
    #    resources, not local fog/vehicle capacity.
    active = sim_df[sim_df["chosen_target"].isin(["vehicle", "fog"])]
    avg_utilization = (
        active["resource_utilization_pct"].mean() if len(active) > 0 else 0.0
    )

    # ── 4. Offloading success rate ────────────────────────────────────────
    #    Uses the dataset's measured `offload_success` ground-truth column.
    #    This reflects real task completion rates in the simulated network.
    offload_success_rate = sim_df["offload_success"].mean() * 100.0

    # ── 5. Handover latency ───────────────────────────────────────────────
    avg_handover_latency = sim_df["handover_latency_ms"].mean()

    # ── 6. Queue length ───────────────────────────────────────────────────
    avg_queue_length = sim_df["queue_length"].mean()

    # ── 7. Offline task success rate ──────────────────────────────────────
    offline_tasks = sim_df[sim_df["is_offline"] == True]
    if len(offline_tasks) > 0:
        # All offline tasks are assigned vehicle or fog (cloud excluded).
        # Report success rate using the dataset's task_success_offline column.
        offline_success_rate = offline_tasks["task_success_offline"].mean() * 100.0
    else:
        offline_success_rate = float("nan")

    # ── Execution target distribution ────────────────────────────────────
    target_counts = sim_df["chosen_target"].value_counts().to_dict()
    for t in ("vehicle", "fog", "cloud"):
        target_counts.setdefault(t, 0)

    return {
        "latency_ms":           round(avg_latency,          3),
        "energy_J":             round(avg_energy,            4),
        "utilization_pct":      round(avg_utilization,       2),
        "offload_success_pct":  round(offload_success_rate,  2),
        "handover_latency_ms":  round(avg_handover_latency,  3),
        "queue_length":         round(avg_queue_length,       3),
        "offline_success_pct":  round(offline_success_rate,  2),
        "target_distribution":  target_counts,
        "n_tasks":              len(sim_df),
        "n_offline":            len(offline_tasks),
    }
