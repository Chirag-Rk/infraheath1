"""
anomaly.py — Multi-modal anomaly detection for infrastructure sensor streams
"""

import numpy as np
import pandas as pd
from typing import Tuple


# ─────────────────────────────────────────────
# A. VIBRATION — Z-Score Anomaly
# ─────────────────────────────────────────────

def detect_vibration_anomalies(
    vibration: np.ndarray,
    z_threshold: float = 3.0,
) -> Tuple[float, list]:
    """
    Detect vibration anomalies using Z-score method.
    Points where |Z| > z_threshold are flagged as anomalies.

    Returns:
        vibration_score (0–100): Higher = healthier
        messages: list of anomaly message strings
    """
    messages = []
    if len(vibration) < 2:
        return 100.0, messages

    mean = np.mean(vibration)
    std = np.std(vibration)
    if std == 0:
        return 100.0, messages

    z_scores = np.abs((vibration - mean) / std)
    anomaly_count = int(np.sum(z_scores > z_threshold))
    anomaly_pct = anomaly_count / len(vibration)

    if anomaly_count > 0:
        max_z = float(np.max(z_scores))
        messages.append(
            f"Vibration Z-score anomaly: {anomaly_count} spike(s) detected "
            f"(max |Z| = {max_z:.2f}, threshold = {z_threshold})"
        )

    # Score degrades linearly: 0 anomalies → 100, ≥20% anomalies → 0
    score = max(0.0, 100.0 - (anomaly_pct / 0.20) * 100.0)
    return round(score, 2), messages


# ─────────────────────────────────────────────
# B. STRESS — Ratio Threshold Check
# ─────────────────────────────────────────────

def detect_stress_anomalies(
    stress_ratio: np.ndarray,
    critical_threshold: float = 1.0,
    warning_threshold: float = 0.85,
) -> Tuple[float, list]:
    """
    Flag stress overload when stress_ratio > 1.0 (exceeds 100% safe load).

    Returns:
        stress_score (0–100)
        messages: list of anomaly message strings
    """
    messages = []
    critical_count = int(np.sum(stress_ratio > critical_threshold))
    warning_count = int(np.sum((stress_ratio > warning_threshold) & (stress_ratio <= critical_threshold)))

    if critical_count > 0:
        max_stress = float(np.max(stress_ratio)) * 100
        messages.append(
            f"CRITICAL: Stress overload detected — {critical_count} reading(s) "
            f"exceeded 100% safe load (max = {max_stress:.1f}%)"
        )
    if warning_count > 0:
        messages.append(
            f"WARNING: {warning_count} stress reading(s) exceeded 85% safe load threshold"
        )

    # Penalise by proportion of critical readings
    critical_pct = critical_count / len(stress_ratio)
    warning_pct = warning_count / len(stress_ratio)
    score = max(0.0, 100.0 - critical_pct * 150.0 - warning_pct * 40.0)
    return round(score, 2), messages


# ─────────────────────────────────────────────
# C. TEMPERATURE — Rolling Mean Trend Detection
# ─────────────────────────────────────────────

def detect_temperature_trend(
    temperature: np.ndarray,
    window: int = 20,
    trend_threshold: float = 5.0,
) -> Tuple[float, list]:
    """
    Detect increasing temperature trends using rolling mean comparison.
    Compares early-window mean vs late-window mean to identify sustained rise.

    Returns:
        temperature_score (0–100)
        messages: list of anomaly message strings
    """
    messages = []
    n = len(temperature)

    if n < window * 2:
        return 100.0, messages

    series = pd.Series(temperature)
    rolling = series.rolling(window=window, center=False).mean().dropna().values

    # Compare first quarter vs last quarter of rolling means
    split = len(rolling) // 4
    if split == 0:
        return 100.0, messages

    early_mean = float(np.mean(rolling[:split]))
    late_mean = float(np.mean(rolling[-split:]))
    delta = late_mean - early_mean

    if delta > trend_threshold:
        messages.append(
            f"Increasing temperature trend detected: rolling mean rose "
            f"{delta:.1f}°C over observation window (threshold = {trend_threshold}°C)"
        )

    # Score: 100 if no trend; degrades if delta exceeds threshold
    score = max(0.0, 100.0 - max(0.0, (delta - trend_threshold) / trend_threshold) * 50.0)

    # Also penalise absolute extremes (>40°C or <-10°C)
    max_temp = float(np.max(temperature))
    min_temp = float(np.min(temperature))
    if max_temp > 40.0:
        messages.append(f"High temperature extreme: {max_temp:.1f}°C recorded")
        score = max(0.0, score - 15.0)
    if min_temp < -10.0:
        messages.append(f"Low temperature extreme: {min_temp:.1f}°C recorded")
        score = max(0.0, score - 10.0)

    return round(score, 2), messages


# ─────────────────────────────────────────────
# COMBINED ANALYSIS ENTRY POINT
# ─────────────────────────────────────────────

def run_anomaly_analysis(df: pd.DataFrame) -> dict:
    """
    Run all anomaly detectors on sensor DataFrame.

    Returns:
        vibration_score, stress_score, temperature_score (each 0–100)
        anomaly_messages: combined list across all detectors
    """
    vib_score, vib_msgs = detect_vibration_anomalies(df["vibration_mm_s"].values)
    str_score, str_msgs = detect_stress_anomalies(df["stress_ratio"].values)
    tmp_score, tmp_msgs = detect_temperature_trend(df["temperature_c"].values)

    all_messages = vib_msgs + str_msgs + tmp_msgs

    return {
        "vibration_score": vib_score,
        "stress_score": str_score,
        "temperature_score": tmp_score,
        "anomaly_messages": all_messages,
    }
