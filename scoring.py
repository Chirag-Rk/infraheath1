"""
scoring.py — Health scoring engine for urban infrastructure assets
"""

from typing import Dict


# ─────────────────────────────────────────────
# SCORING WEIGHTS
# ─────────────────────────────────────────────

WEIGHTS = {
    "crack": 0.40,
    "vibration": 0.30,
    "stress": 0.20,
    "temperature": 0.10,
}

# Status thresholds
STATUS_THRESHOLDS = [
    (80.0, "Healthy"),
    (60.0, "Warning"),
    (40.0, "Critical"),
    (0.0,  "Failure"),
]


def compute_health_score(
    crack_score: float,
    vibration_score: float,
    stress_score: float,
    temperature_score: float,
) -> float:
    """
    Compute the composite infrastructure health score (0–100).

    HealthScore = 0.40 × CrackScore
                + 0.30 × VibrationScore
                + 0.20 × StressScore
                + 0.10 × TemperatureScore
    """
    score = (
        WEIGHTS["crack"] * crack_score
        + WEIGHTS["vibration"] * vibration_score
        + WEIGHTS["stress"] * stress_score
        + WEIGHTS["temperature"] * temperature_score
    )
    return round(float(score), 2)


def classify_status(health_score: float) -> str:
    """Map numeric health score to operational status label."""
    for threshold, label in STATUS_THRESHOLDS:
        if health_score >= threshold:
            return label
    return "Failure"


def score_breakdown(
    crack_score: float,
    vibration_score: float,
    stress_score: float,
    temperature_score: float,
) -> Dict[str, float]:
    """
    Return weighted contribution of each sub-score to the total health score.
    Useful for explainability / dashboard breakdowns.
    """
    return {
        "crack_contribution": round(WEIGHTS["crack"] * crack_score, 2),
        "vibration_contribution": round(WEIGHTS["vibration"] * vibration_score, 2),
        "stress_contribution": round(WEIGHTS["stress"] * stress_score, 2),
        "temperature_contribution": round(WEIGHTS["temperature"] * temperature_score, 2),
        "raw_crack_score": round(crack_score, 2),
        "raw_vibration_score": round(vibration_score, 2),
        "raw_stress_score": round(stress_score, 2),
        "raw_temperature_score": round(temperature_score, 2),
    }
