import json
import os
import sqlite3
from threading import Lock
from uuid import uuid4

from fastapi import HTTPException

from src.agent import generate_stability_report
from src.config import MonitoringConfig
from src.stability_engine import detect_anomaly, detect_degradation


class MonitoringService:
    def __init__(self, db_path=None):
        db_path = db_path if db_path is not None else os.environ.get("AIOS_OBSERVATION_DB", ":memory:")
        if not db_path:
            raise ValueError("AIOS_OBSERVATION_DB must be a persistent file path")
        self.lock = Lock()
        self.db = sqlite3.connect(db_path, timeout=30, check_same_thread=False, isolation_level=None)
        self.db.execute("""CREATE TABLE IF NOT EXISTS observations (
            seq INTEGER PRIMARY KEY AUTOINCREMENT,
            observation_id TEXT NOT NULL UNIQUE,
            telemetry TEXT NOT NULL,
            report TEXT NOT NULL,
            entry TEXT NOT NULL
        )""")
        self.db.execute("""CREATE TABLE IF NOT EXISTS monitor_state (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            anomaly INTEGER NOT NULL,
            recovery_count INTEGER NOT NULL
        )""")
        self.db.execute("INSERT OR IGNORE INTO monitor_state VALUES (1, 0, 0)")

    def evaluate(self, telemetry: dict, mode="manual_trigger"):
        report = generate_stability_report(telemetry)
        metrics = {key: value for key, value in telemetry.items() if key != "observation_id"}
        fingerprint = json.dumps(metrics, sort_keys=True, separators=(",", ":"))
        observation_id = telemetry.get("observation_id")
        with self.lock:
            try:
                self.db.execute("BEGIN IMMEDIATE")
                if observation_id is not None:
                    previous = self.db.execute(
                        "SELECT telemetry, report FROM observations WHERE observation_id = ?",
                        (str(observation_id),),
                    ).fetchone()
                    if previous:
                        if previous[0] != fingerprint:
                            raise HTTPException(status_code=409, detail="Observation ID already used")
                        self.db.commit()
                        return json.loads(previous[1])
                else:
                    previous = self.db.execute(
                        "SELECT telemetry, report FROM observations ORDER BY seq DESC LIMIT 1"
                    ).fetchone()
                    if previous and previous[0] == fingerprint:
                        self.db.commit()
                        return json.loads(previous[1])

                observation_id = str(observation_id or uuid4())
                entry = {
                    "observation_id": observation_id,
                    "timestamp": report["timestamp"],
                    "ADSI": report["scores"]["ADSI"],
                    "stability_tier": report["stability_tier"],
                    "guardrail_flags": report["guardrail_flags"],
                    "mode": mode,
                }
                self.db.execute(
                    "INSERT INTO observations (observation_id, telemetry, report, entry) VALUES (?, ?, ?, ?)",
                    (observation_id, fingerprint, json.dumps(report), json.dumps(entry)),
                )
                scores = [json.loads(row[0])["ADSI"] for row in self.db.execute(
                    "SELECT entry FROM observations ORDER BY seq DESC LIMIT ?",
                    (MonitoringConfig.HISTORY_LIMIT,),
                ).fetchall()][::-1]
                anomaly, recovery_count = self.db.execute(
                    "SELECT anomaly, recovery_count FROM monitor_state WHERE id = 1"
                ).fetchone()
                if anomaly and report["stability_tier"] == "Stable":
                    # ponytail: two fresh Stable observations clear an alert; calibrate before production.
                    recovery_count += 1
                    if recovery_count >= 2:
                        anomaly, recovery_count = 0, 0
                elif detect_anomaly(scores) or report["stability_tier"] == "Critical":
                    anomaly, recovery_count = 1, 0
                else:
                    recovery_count = 0
                self.db.execute(
                    "UPDATE monitor_state SET anomaly = ?, recovery_count = ? WHERE id = 1",
                    (anomaly, recovery_count),
                )
                self.db.commit()
                return report
            except Exception:
                self.db.rollback()
                raise

    def get_observability(self):
        with self.lock:
            rows = self.db.execute(
                "SELECT entry FROM observations ORDER BY seq DESC LIMIT ?",
                (MonitoringConfig.HISTORY_LIMIT,),
            ).fetchall()
            if not rows:
                return {"message": "No evaluations performed yet"}
            history = [json.loads(row[0]) for row in rows[::-1]]
            anomaly = bool(self.db.execute(
                "SELECT anomaly FROM monitor_state WHERE id = 1"
            ).fetchone()[0])
            return {
                "current": history[-1],
                "history": history,
                "degradation": detect_degradation(history[-1]["ADSI"]),
                "anomaly": anomaly,
            }

    def autonomous_check(self):
        # No new observation arrives here; replay must not change history or alerts.
        return self.get_observability()

    def close(self):
        self.db.close()
