from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import random

from models import BridgeAsset
from simulation import simulate_sensor_data, simulate_crack_detection, compute_crack_score
from anomaly import run_anomaly_analysis
from scoring import score_breakdown
from crack_inference import run_crack_inference

app = FastAPI(
    title="Urban Infrastructure Health & Anomaly Analysis System",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─────────────────────────────────────────────
# ASSET PROFILES (Now selection actually matters)
# ─────────────────────────────────────────────

ASSET_PROFILES = {
    "INF-001": {
        "bridge_name": "Millbrook Crossing",
        "material": "Steel",
        "fatigue_factor": 1.2,
        "stress_bias": 1.1,
        "temperature_sensitivity": 1.0,
        "age_factor": 0.9,
    },
    "INF-002": {
        "bridge_name": "Northgate Viaduct",
        "material": "Reinforced Concrete",
        "fatigue_factor": 0.9,
        "stress_bias": 1.0,
        "temperature_sensitivity": 1.2,
        "age_factor": 1.1,
    },
    "INF-003": {
        "bridge_name": "Riverside Steel Arch",
        "material": "Steel Arch",
        "fatigue_factor": 1.3,
        "stress_bias": 1.2,
        "temperature_sensitivity": 0.8,
        "age_factor": 1.2,
    },
    "INF-004": {
        "bridge_name": "Eastside Overpass",
        "material": "Concrete",
        "fatigue_factor": 1.0,
        "stress_bias": 0.9,
        "temperature_sensitivity": 1.1,
        "age_factor": 0.8,
    },
}


def get_profile(asset_id: str):
    return ASSET_PROFILES.get(asset_id, ASSET_PROFILES["INF-001"])


# ─────────────────────────────────────────────
# SIMULATION MODE (Asset-aware)
# ─────────────────────────────────────────────

@app.get("/simulate-asset")
def simulate_asset(asset_id: str = "INF-001"):

    profile = get_profile(asset_id)

    # Crack simulation (material affects severity)
    crack_data = simulate_crack_detection()
    crack_data["crack_length"] *= profile["fatigue_factor"]
    crack_data["cnn_confidence"] *= profile["age_factor"]

    crack_score = compute_crack_score(crack_data)

    # Sensor simulation (asset dependent scaling)
    df = simulate_sensor_data(n=200)

    df["vibration_mm_s"] *= profile["fatigue_factor"]
    df["stress_pct"] *= profile["stress_bias"]
    df["temperature_c"] *= profile["temperature_sensitivity"]

    anomaly_result = run_anomaly_analysis(df)

    vibration_score = anomaly_result["vibration_score"]
    stress_score = anomaly_result["stress_score"]
    temperature_score = anomaly_result["temperature_score"]

    asset = BridgeAsset(
        asset_id=asset_id,
        bridge_name=profile["bridge_name"],
    )

    asset.evaluate_health(
        crack_score,
        vibration_score,
        stress_score,
        temperature_score,
        anomaly_result["anomaly_messages"],
    )

    report = asset.generate_structured_report()

    report["Material"] = profile["material"]

    report["ScoreBreakdown"] = score_breakdown(
        crack_score,
        vibration_score,
        stress_score,
        temperature_score,
    )

    report["CrackAnalysis"] = crack_data

    return report


# ─────────────────────────────────────────────
# REAL CNN MODE (Asset-aware)
# ─────────────────────────────────────────────

@app.post("/analyze-full-health")
async def analyze_full_health(
    image: UploadFile = File(...),
    asset_id: Optional[str] = "INF-001",
):

    profile = get_profile(asset_id)

    contents = await image.read()

    crack_data = run_crack_inference(contents)

    crack_data["crack_length"] *= profile["fatigue_factor"]
    crack_data["cnn_confidence"] *= profile["age_factor"]

    crack_score = compute_crack_score(crack_data)

    df = simulate_sensor_data(n=200)

    df["vibration_mm_s"] *= profile["fatigue_factor"]
    df["stress_pct"] *= profile["stress_bias"]
    df["temperature_c"] *= profile["temperature_sensitivity"]

    anomaly_result = run_anomaly_analysis(df)

    vibration_score = anomaly_result["vibration_score"]
    stress_score = anomaly_result["stress_score"]
    temperature_score = anomaly_result["temperature_score"]

    asset = BridgeAsset(
        asset_id=asset_id,
        bridge_name=profile["bridge_name"],
    )

    asset.evaluate_health(
        crack_score,
        vibration_score,
        stress_score,
        temperature_score,
        anomaly_result["anomaly_messages"],
    )

    report = asset.generate_structured_report()

    report["Material"] = profile["material"]

    report["ScoreBreakdown"] = score_breakdown(
        crack_score,
        vibration_score,
        stress_score,
        temperature_score,
    )

    report["CrackAnalysis"] = crack_data

    return report


# ─────────────────────────────────────────────
# SENSOR DATA (Now asset dependent)
# ─────────────────────────────────────────────

@app.get("/sensor-data")
def get_sensor_data(asset_id: str = "INF-001", n: int = 200):

    profile = get_profile(asset_id)

    df = simulate_sensor_data(n=n)

    df["vibration_mm_s"] *= profile["fatigue_factor"]
    df["stress_pct"] *= profile["stress_bias"]
    df["temperature_c"] *= profile["temperature_sensitivity"]

    df["timestamp"] = df["timestamp"].dt.strftime("%Y-%m-%dT%H:%M:%S")

    return {"data": df.to_dict(orient="records")}


# ─────────────────────────────────────────────
# ASSET LIST
# ─────────────────────────────────────────────

@app.get("/assets")
def list_assets():
    return [
        {
            "asset_id": asset_id,
            "bridge_name": profile["bridge_name"],
        }
        for asset_id, profile in ASSET_PROFILES.items()
    ]


@app.get("/health")
def health():
    return {"status": "ok"}