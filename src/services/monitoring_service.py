from src.config import MonitoringConfig
from collections import deque
from src.agent import generate_stability_report
from src.stability_engine import detect_degradation, detect_anomaly

class MonitoringService:

    def __init__(self):
        self.latest = None
        self.last_telemetry = None
        self.history = deque(maxlen=MonitoringConfig.HISTORY_LIMIT)

    def evaluate(self, telemetry: dict, mode="manual_trigger"):
        self.last_telemetry = telemetry

        report = generate_stability_report(telemetry)

        self.latest = {
            "timestamp": report["timestamp"],
            "ADSI": report["scores"]["ADSI"],
            "stability_tier": report["stability_tier"],
            "guardrail_flags": report["guardrail_flags"],
            "mode": mode
        }

        self.history.append(self.latest)

        return report

    def get_observability(self):
        if self.latest is None:
            return {"message": "No evaluations performed yet"}

        degradation = detect_degradation(self.latest["ADSI"])
        anomaly = detect_anomaly([entry["ADSI"] for entry in self.history])

        return {
            "current": self.latest,
            "history": list(self.history),
            "degradation": degradation,
            "anomaly": anomaly
        }

    def autonomous_check(self):
        if self.last_telemetry:
            self.evaluate(self.last_telemetry, mode="autonomous_monitor")
