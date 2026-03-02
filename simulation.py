"""
simulation.py — Physics-aware sensor simulation and crack detection
"""

import numpy as np
import pandas as pd
from typing import Optional


# ─────────────────────────────────────────────
# CRACK DETECTION SIMULATION
# ─────────────────────────────────────────────

RISK_LABEL_SCORES = {
    "LOW": 90.0,
    "MONITOR": 65.0,
    "MODERATE": 40.0,
    "HIGH": 10.0,
}


def simulate_crack_detection(seed: Optional[int] = None) -> dict:
    """
    Simulate output of a physics-aware visual crack detection system.
    Models a CNN pipeline that classifies crack geometry and risk.
    """
    rng = np.random.default_rng(seed)

    # Randomly decide whether a crack is present
    crack_confirmed = bool(rng.random() > 0.35)

    if crack_confirmed:
        crack_length = float(rng.uniform(0.5, 18.0))       # mm
        crack_orientation = float(rng.uniform(0.0, 180.0)) # degrees
        cnn_confidence = float(rng.uniform(0.55, 0.99))

        # Risk label driven by crack length + confidence heuristic
        severity = crack_length * cnn_confidence
        if severity < 3.0:
            risk_label = "LOW"
        elif severity < 7.0:
            risk_label = "MONITOR"
        elif severity < 12.0:
            risk_label = "MODERATE"
        else:
            risk_label = "HIGH"
    else:
        crack_length = float(rng.uniform(0.0, 0.4))
        crack_orientation = float(rng.uniform(0.0, 180.0))
        cnn_confidence = float(rng.uniform(0.10, 0.45))
        risk_label = "LOW"

    return {
        "crack_confirmed": crack_confirmed,
        "crack_length": round(crack_length, 3),
        "crack_orientation": round(crack_orientation, 2),
        "cnn_confidence": round(cnn_confidence, 4),
        "crack_risk_label": risk_label,
    }


def compute_crack_score(crack_data: dict) -> float:
    """
    Convert crack detection output to 0-100 health score.

    Weights:
      - crack_length    → 0.40  (longer crack = lower score)
      - cnn_confidence  → 0.30  (high confidence crack = lower score)
      - risk_label      → 0.30  (map label to score)
    """
    MAX_LENGTH = 20.0

    # Invert: longer crack → lower health contribution
    length_score = max(0.0, 100.0 - (crack_data["crack_length"] / MAX_LENGTH) * 100.0)

    # If crack confirmed, high confidence lowers health; else confidence irrelevant
    if crack_data["crack_confirmed"]:
        confidence_score = max(0.0, 100.0 - crack_data["cnn_confidence"] * 100.0)
    else:
        confidence_score = 100.0

    label_score = RISK_LABEL_SCORES.get(crack_data["crack_risk_label"], 50.0)

    composite = (
        0.40 * length_score
        + 0.30 * confidence_score
        + 0.30 * label_score
    )
    return round(float(composite), 2)


# ─────────────────────────────────────────────
# SENSOR DATA SIMULATION
# ─────────────────────────────────────────────

def simulate_sensor_data(
    n: int = 200,
    inject_vibration_spike: bool = False,
    inject_stress_overload: bool = False,
    inject_temp_trend: bool = False,
    seed: Optional[int] = None,
) -> pd.DataFrame:
    """
    Simulate time-series sensor readings for bridge infrastructure.

    Returns a DataFrame with columns:
      timestamp, vibration_mm_s, stress_pct, temperature_c
    """
    rng = np.random.default_rng(seed)
    timestamps = pd.date_range("2024-01-01", periods=n, freq="5min")

    # ── Vibration (mm/s) — normally distributed around 3.5 mm/s
    vibration = rng.normal(loc=3.5, scale=0.6, size=n)
    if inject_vibration_spike:
        spike_indices = rng.choice(n, size=int(n * 0.05), replace=False)
        vibration[spike_indices] += rng.uniform(8, 18, size=len(spike_indices))

    # ── Stress (% of safe load) — normally around 55%
    stress = rng.normal(loc=55.0, scale=8.0, size=n) / 100.0
    if inject_stress_overload:
        overload_indices = rng.choice(n, size=int(n * 0.08), replace=False)
        stress[overload_indices] = rng.uniform(1.05, 1.35, size=len(overload_indices))

    # ── Temperature (°C) — baseline with diurnal pattern
    diurnal = 6.0 * np.sin(np.linspace(0, 4 * np.pi, n))
    temperature = 18.0 + diurnal + rng.normal(0, 1.5, size=n)
    if inject_temp_trend:
        trend = np.linspace(0, 15, n)  # rising 15°C over window
        temperature += trend

    vibration = np.clip(vibration, 0, None)
    stress = np.clip(stress, 0, None)

    df = pd.DataFrame(
        {
            "timestamp": timestamps,
            "vibration_mm_s": np.round(vibration, 4),
            "stress_pct": np.round(stress * 100, 2),   # store as % for readability
            "stress_ratio": np.round(stress, 4),        # ratio for threshold checks
            "temperature_c": np.round(temperature, 2),
        }
    )
    return df
