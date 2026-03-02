# 🏗️ INFRA-HEALTH  
## Urban Infrastructure Health & Anomaly Analysis System

---

## 📌 Overview

**INFRA-HEALTH** is a rule-driven infrastructure monitoring system designed to evaluate the operational condition of urban infrastructure assets such as bridges.

The system integrates:

- Sensor-based anomaly detection  
- Operational threshold validation  
- Weighted health scoring  
- ML-assisted crack inspection  
- Structured health state classification  
- Interactive dashboard visualization  

It detects abnormal operational behavior, classifies asset health states, and presents structured, interpretable outputs for engineering decision-making.

---

## 🎯 Problem Statement

Urban infrastructure deteriorates due to:

- Structural stress  
- Environmental exposure  
- Dynamic loading  
- Material fatigue  

An effective monitoring system must:

1. Detect abnormal operational behavior  
2. Apply statistical or rule-based thresholds  
3. Classify asset health states  
4. Provide interpretable, structured outputs  

Most existing systems treat sensor analytics and image-based inspection separately.  
**INFRA-HEALTH integrates both into a unified evaluation framework.**

---

## 🏗️ System Architecture

### Frontend (Streamlit)

- Interactive dashboard  
- Asset selection interface  
- Health score visualization  
- Sensor time-series plots  
- Anomaly log display  
- Crack image upload interface  

### Backend (FastAPI)

- REST API service  
- Sensor simulation engine  
- Anomaly detection module  
- Health scoring engine  
- Crack inference endpoint  

### Machine Learning Layer

- ResNet18 binary crack classifier  
- Softmax probability extraction  
- Crack mask generation  
- Crack length estimation  
- Dominant orientation analysis  
- Physics-aware validation logic  

---

## 📊 Health Evaluation Framework

### 1️⃣ Sensor-Based Anomaly Detection

**Monitored Parameters**
- Vibration  
- Stress load  
- Temperature  

**Methodology**
- Z-score based anomaly detection  
- Threshold-based rule validation  
- Spike identification  
- Structured anomaly logging  

An anomaly is flagged when:

---

### 2️⃣ Weighted Health Scoring

Final health score range: **0 – 100**

| Component   | Weight |
|-------------|--------|
| Crack Score | 40%    |
| Vibration   | 30%    |
| Stress      | 20%    |
| Temperature | 10%    |

### Health State Categories

- **Healthy**
- **Warning**
- **Critical**
- **Failure**

Classification is rule-derived, not purely predictive.

---

### 3️⃣ ML-Assisted Crack Analysis

The crack inspection module performs:

- Modified ResNet18 inference  
- Softmax confidence scoring  
- Binary crack mask generation  
- Crack length computation  
- Orientation estimation  
- Severity calculation (length × confidence)  
- Risk label assignment  

This module enhances structural evaluation while remaining integrated within the rule-based scoring pipeline.

---

## ⚙️ Operational Modes

### Simulation Mode

- Synthetic sensor data generation  
- Rule-based anomaly detection  
- Health score computation  
- Demonstration without real hardware  

### Real Inference Mode

- Crack image upload  
- CNN-based crack detection  
- Physics-aware validation  
- Integrated health evaluation  

---

## 📤 System Output

For each infrastructure asset, the system provides:

- Detected abnormal conditions  
- Structured anomaly logs  
- Crack detection results (if image provided)  
- Crack geometry metrics  
- Risk classification  
- Weighted health score  
- Health state category  

The output aligns with core infrastructure monitoring requirements:
- Evaluate operational condition  
- Identify anomalies  
- Classify health states  
- Present structured health information  

---

##🧰 Technology Stack
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

## 🧠 Core Methodology: Dual-Approach Evaluation Framework

INFRA-HEALTH is built on a **two-approach evaluation strategy** that combines deterministic engineering logic with machine learning–based structural inspection.

---

### 🔹 Approach 1: Rule-Based Sensor Intelligence (Deterministic Layer)

This approach focuses on operational behavior using statistical and physics-aware rules.

**Key Components**

- Z-score based anomaly detection  
- Threshold-based rule validation  
- Structured anomaly logging  
- Weighted health score computation  
- Deterministic health state classification  

**Why this matters**

- Fully interpretable  
- Transparent decision boundaries  
- Engineering-aligned logic  
- Suitable for safety-critical systems  
- No black-box dependence  

This layer ensures that abnormal operational conditions (vibration, stress, temperature) are detected using statistically validated and rule-defined criteria.

It provides stability, interpretability, and explainability.

---

### 🔹 Approach 2: ML-Assisted Structural Inspection (Vision Layer)

This approach focuses on physical defect detection using deep learning.

**Key Components**

- ResNet18-based crack classifier  
- Softmax confidence extraction  
- Crack mask generation  
- Crack geometry estimation (length & orientation)  
- Severity scoring (length × confidence)  
- Risk label assignment  

**Why this matters**

- Captures visual structural damage  
- Detects defects invisible to sensor-only systems  
- Quantifies crack geometry  
- Adds structural context to health evaluation  

This layer enhances the system by identifying material-level defects that may not yet manifest in sensor anomalies.

---

## 🔄 Unified Integration Strategy

The two approaches are not independent.

They are integrated through a **weighted health scoring framework**:

| Component Contribution | Weight |
|------------------------|--------|
| Crack Severity         | 40%    |
| Vibration              | 30%    |
| Stress                 | 20%    |
| Temperature            | 10%    |

Final health classification is derived using combined outputs from both approaches.

This hybrid design ensures:

- Interpretability (rule-based logic)
- Structural insight (ML inspection)
- Balanced risk assessment
- Reduced false positives
- Engineering-aligned decision output

---

## 🎯 Why Two Approaches?

Relying only on sensors misses visual defects.  
Relying only on ML ignores operational physics.

INFRA-HEALTH deliberately combines:

> Deterministic engineering validation  
> +  
> Data-driven structural intelligence  

to create a robust and explainable infrastructure monitoring framework.

## 🏁 Conclusion

INFRA-HEALTH demonstrates a structured, rule-driven approach to infrastructure health evaluation by integrating:

Statistical anomaly detection
Rule-based classification
ML-assisted crack inspection
Structured health scoring
