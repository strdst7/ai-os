from collections import deque
from threading import Lock
from uuid import uuid4

from fastapi import HTTPException

from src.agent import generate_stability_report
from src.config import MonitoringConfig
from src.stability_engine import detect_degradation, detect_anomaly

class MonitoringService:

    def __init__(self):
        self.latest = None
        self.last_telemetry = None
        self.history = deque(maxlen=MonitoringConfig.HISTORY_LIMIT)
        self.anomaly = False
        self.recovery_count = 0
        self.lock = Lock()
        self.observations = {}

    def evaluate(self, telemetry: dict, mode="manual_trigger"):
        report = generate_stability_report(telemetry)
        with self.lock:
            return self._record(telemetry, report, mode)

    def _record(self, telemetry: dict, report: dict, mode: str):
        observation_id = telemetry.get("observation_id")
        if observation_id is not None and observation_id in self.observations:
            previous_telemetry, previous_report = self.observations[observation_id]
            if telemetry != previous_telemetry:
                raise HTTPException(status_code=409, detail="Observation ID already used")
            return previous_report
        if observation_id is None and self.latest is not None and telemetry == self.last_telemetry:
            return self.observations[self.latest["observation_id"]][1]

        observation_id = str(observation_id or uuid4())
        self.last_telemetry = telemetry.copy() if telemetry.get("observation_id") is None else None
        self.latest = {
            "observation_id": observation_id,
            "timestamp": report["timestamp"],
            "ADSI": report["scores"]["ADSI"],
            "stability_tier": report["stability_tier"],
            "guardrail_flags": report["guardrail_flags"],
            "mode": mode
        }

        self.history.append(self.latest)
        # ponytail: process-local ID map grows; use durable storage for unbounded retention.
        self.observations[observation_id] = (telemetry.copy(), report)
        scores = [entry["ADSI"] for entry in self.history]
        if self.anomaly and report["stability_tier"] == "Stable":
            # ponytail: two distinct healthy samples clear an alert; calibrate recovery for production.
            self.recovery_count += 1
            if self.recovery_count >= 2:
                self.anomaly = False
                self.recovery_count = 0
        elif detect_anomaly(scores) or report["stability_tier"] == "Critical":
            self.anomaly = True
            self.recovery_count = 0
        else:
            self.recovery_count = 0

        return report

    def get_observability(self):
        with self.lock:
            if self.latest is None:
                return {"message": "No evaluations performed yet"}

            degradation = detect_degradation(self.latest["ADSI"])
            return {
                "current": self.latest,
                "history": list(self.history),
                "degradation": degradation,
                "anomaly": self.anomaly
            }

    def autonomous_check(self):
        # No new observation arrives here; replay must not change history or alerts.
        with self.lock:
            return self.latest
