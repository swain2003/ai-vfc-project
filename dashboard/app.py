"""
AI-VFC Dashboard Server
=======================
Serves the dark-mode command-center dashboard and exposes REST endpoints.

Run with:   python dashboard/app.py
Then open:  http://localhost:5000
"""

import os
import sys
import json
import subprocess
import threading

import pandas as pd
from flask import Flask, jsonify, send_from_directory, render_template, request

# ── Make project root importable ──────────────────────────────────────────────
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from config.settings import RESULTS_DIR, DATA_PATH

app = Flask(__name__, template_folder="templates")

# ── Simulation run state ──────────────────────────────────────────────────────
_sim_lock   = threading.Lock()
_sim_running = False
_sim_log     = []


def _append_log(msg: str):
    global _sim_log
    _sim_log.append(msg)
    if len(_sim_log) > 200:
        _sim_log = _sim_log[-200:]


# ─────────────────────────────────────────────────────────────────────────────
# API endpoints
# ─────────────────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/status")
def api_status():
    """Check if simulation results exist."""
    metrics_path = os.path.join(RESULTS_DIR, "metrics.json")
    sim_path     = os.path.join(RESULTS_DIR, "simulation_output.csv")
    return jsonify({
        "has_results":  os.path.exists(metrics_path),
        "has_csv":      os.path.exists(sim_path),
        "sim_running":  _sim_running,
        "dataset_rows": 799,
    })


@app.route("/api/metrics")
def api_metrics():
    """Return the latest computed metrics as JSON."""
    path = os.path.join(RESULTS_DIR, "metrics.json")
    if not os.path.exists(path):
        return jsonify({"error": "No results yet. Run the simulation first."}), 404
    with open(path) as f:
        data = json.load(f)
    return jsonify(data)


@app.route("/api/simulation")
def api_simulation():
    """Return simulation_output.csv as JSON (sampled for performance)."""
    path = os.path.join(RESULTS_DIR, "simulation_output.csv")
    if not os.path.exists(path):
        return jsonify({"error": "No simulation output yet."}), 404

    df = pd.read_csv(path)

    # Columns needed by the dashboard
    keep = [
        "chosen_target", "eff_latency_ms", "eff_energy_J",
        "resource_utilization_pct", "handover_latency_ms",
        "queue_length", "is_offline", "offload_success",
        "task_success_offline", "Vehicle_Priority",
        "cost_vehicle", "cost_fog", "cost_cloud", "workload_scaled",
        "Slice_Type", "Vehicle_Type",
    ]
    keep = [c for c in keep if c in df.columns]
    df = df[keep]

    return jsonify({
        "rows":    len(df),
        "columns": list(df.columns),
        "data":    df.to_dict(orient="list"),
    })


@app.route("/api/run", methods=["POST"])
def api_run():
    """Trigger the simulation. Non-blocking — poll /api/run/status."""
    global _sim_running, _sim_log

    if _sim_running:
        return jsonify({"status": "already_running"}), 202

    _sim_running = True
    _sim_log = ["[Server] Starting simulation…"]

    def _run():
        global _sim_running
        try:
            proc = subprocess.Popen(
                [sys.executable, os.path.join(ROOT, "main.py")],
                cwd=ROOT,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
            )
            for line in proc.stdout:
                _append_log(line.rstrip())
            proc.wait()
            _append_log(f"[Server] Simulation finished (exit {proc.returncode}).")
        except Exception as e:
            _append_log(f"[Server] ERROR: {e}")
        finally:
            _sim_running = False

    threading.Thread(target=_run, daemon=True).start()
    return jsonify({"status": "started"})


@app.route("/api/run/status")
def api_run_status():
    return jsonify({
        "running": _sim_running,
        "log":     _sim_log[-50:],
    })


@app.route("/api/dataset/preview")
def api_dataset_preview():
    """Return first 10 rows of the raw dataset for inspection."""
    df = pd.read_csv(DATA_PATH).head(10)
    return jsonify(df.to_dict(orient="list"))


# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("\n" + "=" * 58)
    print("  AI-VFC Dashboard  →  http://localhost:5000")
    print("=" * 58 + "\n")
    app.run(debug=True, port=5000, use_reloader=False)
