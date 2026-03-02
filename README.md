# 🏗️ Urban Infrastructure Health & Anomaly Analysis System

A scalable system that evaluates the operational condition of urban infrastructure assets using defined rules, thresholds, and statistical patterns. It identifies abnormal conditions, classifies asset health states, and presents health information in a clear, structured, and explainable manner.

---

## Project Structure

```
urban_infra/
├── backend/
│   ├── main.py          # FastAPI application + endpoints
│   ├── models.py        # InfrastructureAsset & BridgeAsset classes
│   ├── simulation.py    # Crack detection + sensor data simulation
│   ├── anomaly.py       # Z-score / threshold / trend anomaly detection
│   └── scoring.py       # Weighted health scoring engine
├── frontend/
│   └── app.py           # Streamlit dashboard
└── requirements.txt
```

---

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Start the Backend (FastAPI)

```bash
cd backend
uvicorn main:app --reload --port 8000
```

API docs available at: http://localhost:8000/docs

### 3. Start the Frontend (Streamlit)

In a **separate terminal**:

```bash
cd frontend
streamlit run app.py
```

Dashboard opens at: http://localhost:8501

---

## API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/simulate-asset` | GET | Full health report for a given asset |
| `/sensor-data` | GET | Raw time-series sensor readings |
| `/crack-analysis` | GET | Crack detection simulation result |
| `/assets` | GET | List all registered assets |

### Example Response (`/simulate-asset?asset_id=INF-001`)

```json
{
  "AssetID": "INF-001",
  "AssetType": "Bridge",
  "HealthScore": 52.4,
  "Status": "Critical",
  "Anomalies": [
    "HIGH-risk crack detected: 14.2 mm, confidence 87.30%",
    "Vibration Z-score anomaly: 3 spike(s) detected (max |Z| = 4.12, threshold = 3.0)",
    "CRITICAL: Stress overload detected — 12 reading(s) exceeded 100% safe load (max = 118.4%)"
  ],
  "ScoreBreakdown": {
    "crack_contribution": 16.2,
    "vibration_contribution": 24.6,
    "stress_contribution": 8.4,
    "temperature_contribution": 9.8,
    "raw_crack_score": 40.5,
    "raw_vibration_score": 82.0,
    "raw_stress_score": 42.0,
    "raw_temperature_score": 98.4
  },
  "CrackAnalysis": {
    "crack_confirmed": true,
    "crack_length": 14.2,
    "crack_orientation": 73.4,
    "cnn_confidence": 0.873,
    "crack_risk_label": "HIGH"
  }
}
```

---

## Health Score Formula

```
HealthScore = 0.40 × CrackScore
            + 0.30 × VibrationScore
            + 0.20 × StressScore
            + 0.10 × TemperatureScore
```

| Range | Status |
|-------|--------|
| 80–100 | ✅ Healthy |
| 60–79 | ⚠️ Warning |
| 40–59 | 🔶 Critical |
| < 40 | ❌ Failure |

---

## Anomaly Detection Methods

| Sensor | Method | Threshold |
|--------|--------|-----------|
| Vibration | Z-score | \|Z\| > 3.0 |
| Stress | Ratio threshold | > 100% safe load |
| Temperature | Rolling mean trend | Δ > 5°C over window |

---

## Assets in Registry

| ID | Name | Material |
|----|------|----------|
| INF-001 | Millbrook Crossing | Reinforced Concrete |
| INF-002 | Northgate Viaduct | Pre-stressed Concrete |
| INF-003 | Riverside Steel Arch | Steel |
| INF-004 | Eastside Overpass | Composite |
