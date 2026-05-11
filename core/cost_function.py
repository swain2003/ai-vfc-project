"""
Cost Function: C = αL + βE + γW
Computes cost for each execution layer given task parameters.

Key design decisions
--------------------
* workload_scaled is normalised to [0,1] using the dataset max (45.74) so
  layer workload_cap thresholds are on a consistent 0–1 scale.
* An overload compute_delay (ms) is added to effective latency when workload
  exceeds a layer's capacity cap, modelling ECU/fog queue slowdown.  This
  ensures high-workload tasks are routed toward fog/cloud rather than always
  choosing the local ECU.
* Cloud is NEVER penalised for workload (unlimited compute assumption).
"""

from config.settings import COST_LAYER_PARAMS, WORKLOAD_SCALE_MAX


def compute_layer_cost(
    latency_ms: float,
    energy_J: float,
    workload_scaled: float,
    layer: str,
    alpha: float,
    beta: float,
    gamma: float,
) -> float:
    """
    Compute cost C = αL + βE + γW for one execution layer.

    Parameters
    ----------
    latency_ms      : raw dataset latency (ms)
    energy_J        : raw dataset energy (J)
    workload_scaled : raw workload value (un-normalised from dataset)
    layer           : 'vehicle' | 'fog' | 'cloud'
    alpha, beta, gamma : adaptive cost-function weights

    Returns
    -------
    float : composite cost (lower = better)
    """
    p = COST_LAYER_PARAMS[layer]

    # Normalise workload to [0, 1]
    ws_norm = min(workload_scaled / WORKLOAD_SCALE_MAX, 1.0)

    # Overload: workload that exceeds the layer's compute capacity
    overload = max(0.0, ws_norm - p["workload_cap"])

    # Effective latency: base latency × layer factor + compute-queue delay
    eff_L = latency_ms * p["latency_factor"] + overload * p["compute_delay_coeff"]

    # Effective energy: base energy × layer factor
    eff_E = energy_J * p["energy_factor"]

    # Effective workload: base + penalty for overload
    eff_W = ws_norm + overload * p["workload_penalty"]

    cost = alpha * eff_L + beta * eff_E + gamma * eff_W
    return cost


def batch_costs(df_slice, alpha: float, beta: float, gamma: float) -> dict:
    """
    Compute costs for all three layers for a single dataset row.

    Parameters
    ----------
    df_slice : pandas Series (one row of the simulation dataset)
    alpha, beta, gamma : adaptive weights

    Returns
    -------
    dict : {'vehicle': cost_v, 'fog': cost_f, 'cloud': cost_c}
    """
    L = df_slice["latency_ms"]
    E = df_slice["energy_J"]
    W = df_slice["workload_scaled"]

    return {
        layer: compute_layer_cost(L, E, W, layer, alpha, beta, gamma)
        for layer in ("vehicle", "fog", "cloud")
    }
