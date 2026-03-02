# 🏗️ Urban Infrastructure Health & Anomaly Analysis System


🏗️ INFRA-HEALTH
Urban Infrastructure Health & Anomaly Analysis System
1. Overview

INFRA-HEALTH is a structured, rule-driven infrastructure monitoring system designed to evaluate the operational condition of urban infrastructure assets such as bridges.

The system integrates:

Sensor-based anomaly detection

Defined operational thresholds

Weighted health scoring

ML-assisted crack inspection

Structured health state classification

Dashboard-based visualization

It detects abnormal operational behavior, classifies asset health states, and presents interpretable, structured health information for decision-making.

2. Problem Context

Urban infrastructure degrades over time due to:

Structural stress

Environmental exposure

Dynamic loading

Material fatigue

Monitoring systems must:

Detect abnormal operational behavior

Apply predefined rules or statistical thresholds

Classify asset health states

Provide interpretable outputs

Most existing systems focus on either sensor analytics or image-based inspection independently.
INFRA-HEALTH integrates both into a unified evaluation framework.

3. System Architecture
Frontend

Streamlit-based interactive dashboard

Asset selection interface

Health score visualization

Sensor time-series plots

Anomaly log display

Crack image upload module

Backend

FastAPI REST API

Sensor simulation engine

Anomaly detection module

Health scoring engine

Crack inference endpoint

Machine Learning Layer

ResNet18 binary crack classifier

Softmax confidence scoring

OpenCV-based crack geometry analysis

Physics-aware validation logic

4. Health Evaluation Framework
4.1 Sensor-Based Anomaly Detection

Monitored Parameters:

Vibration

Stress load

Temperature

Methodology:

Z-score based anomaly detection

Threshold-based rule evaluation

Spike identification

Structured anomaly logging

An abnormal condition is flagged when:

|Z| > predefined threshold
4.2 Weighted Health Scoring

The final health score (0–100) is computed using weighted contributions:

Component	Weight
Crack Score	40%
Vibration	30%
Stress	20%
Temperature	10%
Health State Classification

Healthy

Warning

Critical

Failure

Classification is rule-derived, not purely predictive.

4.3 ML-Assisted Crack Analysis

Optional crack inspection module includes:

Modified ResNet18 (custom fully connected layer)

Softmax probability extraction

Binary crack mask generation

Crack length estimation

Dominant orientation analysis

Severity computation (length × confidence)

Risk label assignment

This module enhances structural evaluation while remaining integrated within the rule-based scoring system.

5. Operational Modes
Simulation Mode

Synthetic sensor data generation

Rule-based anomaly detection

Health score computation

Demonstration without real hardware

Real Inference Mode

Crack image upload

CNN-based crack detection

Physics-aware validation

Integration into overall health evaluation

6. System Output

For each infrastructure asset, the system provides:

Detected abnormal conditions

Structured anomaly logs

Crack detection results (if image provided)

Crack geometry metrics

Risk classification

Weighted health score

Health state category

The output aligns with infrastructure monitoring requirements:

Evaluate operational condition

Identify anomalies

Classify health states

Present structured health information

7. Project Structure
INFRA-HEALTH/
│
├── backend/
│   ├── main.py
│   ├── anomaly.py
│   ├── scoring.py
│   ├── simulation.py
│   ├── crack_inference.py
│   └── physics_filters/
│
├── frontend/
│   └── app.py
│
├── models/
│   └── baseline_resnet/
│       └── resnet18_sdnet_baseline.pth
│
└── README.md
8. Installation & Usage
Clone Repository
git clone https://github.com/your-username/INFRA-HEALTH.git
cd INFRA-HEALTH
Create Virtual Environment
python -m venv venv

Activate:

Mac/Linux

source venv/bin/activate

Windows

venv\Scripts\activate
Install Dependencies
pip install -r requirements.txt
Run Backend (FastAPI)
cd backend
uvicorn main:app --reload --port 8000

API runs at:

http://localhost:8000
Run Frontend (Streamlit)
cd frontend
streamlit run app.py

Dashboard runs at:

http://localhost:8501
9. Technology Stack
Backend

Python

FastAPI

Frontend

Streamlit

Machine Learning

PyTorch

Torchvision (ResNet18)

Image Processing

OpenCV

NumPy

PIL

Data Processing

Pandas

Statistical Analysis

Z-score anomaly detection

10. Limitations

Sensor data is simulated

Binary crack classification only

No real-time IoT integration

No temporal crack progression modeling

Designed for research and demonstration purposes

11. Future Improvements

Real sensor integration

Predictive maintenance modeling

Multi-class structural defect classification

Cloud deployment

Real-time monitoring pipeline

12. Conclusion

INFRA-HEALTH is a structured, rule-driven infrastructure health evaluation system that:

Identifies abnormal operational conditions

Applies defined rules and statistical thresholds

Classifies asset health states

Presents interpretable health information

It demonstrates integration of anomaly detection, rule-based evaluation, and ML-assisted inspection within a unified infrastructure monitoring framework.
