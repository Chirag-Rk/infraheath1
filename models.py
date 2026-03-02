"""
Urban Infrastructure Health & Anomaly Analysis System
models.py — Asset data models and health classification
"""

from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime


class InfrastructureAsset:
    """Base class for all infrastructure assets."""

    def __init__(self, asset_id: str, asset_type: str):
        self.asset_id = asset_id
        self.asset_type = asset_type
        self.health_score: float = 0.0
        self.status: str = "Unknown"
        self.anomalies: List[str] = []
        self.last_evaluated: Optional[str] = None

    def evaluate_health(
        self,
        crack_score: float,
        vibration_score: float,
        stress_score: float,
        temperature_score: float,
        anomaly_messages: List[str],
    ) -> float:
        """Compute composite health score using weighted formula."""
        self.health_score = (
            0.40 * crack_score
            + 0.30 * vibration_score
            + 0.20 * stress_score
            + 0.10 * temperature_score
        )
        self.anomalies = anomaly_messages
        self.last_evaluated = datetime.utcnow().isoformat()
        self.classify_status()
        return self.health_score

    def classify_status(self) -> str:
        """Classify asset operational status from health score."""
        score = self.health_score
        if score >= 80:
            self.status = "Healthy"
        elif score >= 60:
            self.status = "Warning"
        elif score >= 40:
            self.status = "Critical"
        else:
            self.status = "Failure"
        return self.status

    def generate_structured_report(self) -> dict:
        """Return a structured JSON-ready health report."""
        return {
            "AssetID": self.asset_id,
            "AssetType": self.asset_type,
            "HealthScore": round(self.health_score, 2),
            "Status": self.status,
            "Anomalies": self.anomalies,
            "LastEvaluated": self.last_evaluated,
        }


class BridgeAsset(InfrastructureAsset):
    """Specialised asset model for bridge infrastructure."""

    def __init__(self, asset_id: str, bridge_name: str = "Unknown Bridge"):
        super().__init__(asset_id=asset_id, asset_type="Bridge")
        self.bridge_name = bridge_name
        self.span_length_m: Optional[float] = None
        self.construction_year: Optional[int] = None
        self.material: str = "Reinforced Concrete"

    def generate_structured_report(self) -> dict:
        """Extend base report with bridge-specific metadata."""
        report = super().generate_structured_report()
        report["BridgeName"] = self.bridge_name
        report["Material"] = self.material
        if self.span_length_m:
            report["SpanLengthMeters"] = self.span_length_m
        if self.construction_year:
            report["ConstructionYear"] = self.construction_year
        return report
