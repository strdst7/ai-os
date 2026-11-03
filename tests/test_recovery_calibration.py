"""Behavior checks for the provisional two-fresh-Stable recovery rule.

These scenarios are not a statistical calibration of the threshold.
"""

from datetime import datetime, timedelta, timezone
from uuid import uuid4

import pytest

from src.agent import generate_stability_report
from src.services.monitoring_service import MonitoringService


CRITICAL = {"kpi_error": 1.0, "retrieval_score": 0.0,
            "latency_dev": 1.0, "embedding_shift": 1.0}
STABLE = {"kpi_error": 0.0, "retrieval_score": 1.0,
          "latency_dev": 0.0, "embedding_shift": 0.0}
WARNING = {**STABLE, "kpi_error": 0.5}


@pytest.mark.parametrize(
    ("sequence", "expected_latch", "expected_count"),
    [
        (["Critical", "Stable", "Stable"], [True, True, False], [0, 1, 0]),
        (["Critical", "Stable", "Warning"], [True, True, True], [0, 1, 0]),
        (["Critical", "Stable", "Critical"], [True, True, True], [0, 1, 0]),
    ],
)
def test_recovery_sequences(tmp_path, sequence, expected_latch, expected_count):
    monitor = MonitoringService(tmp_path / "observations.db")
    stable_id = str(uuid4())
    for index, label in enumerate(sequence):
        payload = {"Critical": CRITICAL, "Stable": STABLE, "Warning": WARNING}[label]
        identity = stable_id if index == 1 else str(uuid4())
        report = monitor.evaluate({**payload, "observation_id": identity})
        assert report["stability_tier"] == label
        state = monitor.get_observability()
        assert state["anomaly"] is expected_latch[index]
        assert monitor.db.execute(
            "SELECT recovery_count FROM monitor_state WHERE id = 1"
        ).fetchone()[0] == expected_count[index]
        assert len(state["history"]) == index + 1
    monitor.close()


@pytest.mark.parametrize("interruption", ["Warning", "Critical"])
def test_recovery_requires_consecutive_stable_after_interruption(tmp_path, interruption):
    monitor = MonitoringService(tmp_path / "observations.db")
    for label, expected_latch, expected_count in (
        ("Critical", True, 0),
        ("Stable", True, 1),
        (interruption, True, 0),
        ("Stable", True, 1),
        ("Stable", False, 0),
    ):
        payload = {"Critical": CRITICAL, "Stable": STABLE, "Warning": WARNING}[label]
        monitor.evaluate({**payload, "observation_id": str(uuid4())})
        assert monitor.get_observability()["anomaly"] is expected_latch
        assert monitor.db.execute(
            "SELECT recovery_count FROM monitor_state WHERE id = 1"
        ).fetchone()[0] == expected_count
    monitor.close()


def test_duplicate_stable_does_not_clear_anomaly(tmp_path):
    monitor = MonitoringService(tmp_path / "observations.db")
    monitor.evaluate({**CRITICAL, "observation_id": str(uuid4())})
    stable = {**STABLE, "observation_id": str(uuid4())}
    first = monitor.evaluate(stable)
    before = monitor.get_observability()
    assert before["anomaly"] is True
    assert monitor.evaluate(stable) == first
    assert monitor.get_observability() == before
    assert monitor.db.execute(
        "SELECT recovery_count FROM monitor_state WHERE id = 1"
    ).fetchone()[0] == 1
    monitor.evaluate({**STABLE, "observation_id": str(uuid4())})
    assert monitor.get_observability()["anomaly"] is False
    assert len(monitor.get_observability()["history"]) == 3
    monitor.close()


@pytest.mark.parametrize("gap", [timedelta(seconds=1), timedelta(days=1)])
def test_recovery_does_not_enforce_elapsed_time(tmp_path, monkeypatch, gap):
    clock = [datetime(2026, 1, 1, tzinfo=timezone.utc)]

    def report_at_controlled_time(metrics):
        report = generate_stability_report(metrics)
        report["timestamp"] = clock[0].isoformat()
        return report

    monkeypatch.setattr("src.services.monitoring_service.generate_stability_report", report_at_controlled_time)
    path = tmp_path / "observations.db"
    monitor = MonitoringService(path)
    monitor.evaluate({**CRITICAL, "observation_id": str(uuid4())})
    clock[0] += gap
    monitor.evaluate({**STABLE, "observation_id": str(uuid4())})
    assert monitor.get_observability()["anomaly"] is True
    monitor.close()

    clock[0] += gap
    monitor = MonitoringService(path)
    monitor.evaluate({**STABLE, "observation_id": str(uuid4())})
    state = monitor.get_observability()
    assert state["anomaly"] is False
    timestamps = [datetime.fromisoformat(row["timestamp"]) for row in state["history"]]
    assert timestamps[1] - timestamps[0] == gap
    assert timestamps[2] - timestamps[1] == gap
    monitor.close()


def test_stale_stable_replay_after_warning_does_not_advance_recovery(tmp_path):
    monitor = MonitoringService(tmp_path / "observations.db")
    first_stable = {**STABLE, "observation_id": str(uuid4())}
    monitor.evaluate({**CRITICAL, "observation_id": str(uuid4())})
    monitor.evaluate(first_stable)
    monitor.evaluate({**WARNING, "observation_id": str(uuid4())})
    before = monitor.get_observability()
    monitor.evaluate(first_stable)
    assert monitor.get_observability() == before
    monitor.evaluate({**STABLE, "observation_id": str(uuid4())})
    assert monitor.get_observability()["anomaly"] is True
    monitor.close()


def test_idless_duplicate_stable_does_not_count_as_fresh(tmp_path):
    monitor = MonitoringService(tmp_path / "observations.db")
    monitor.evaluate(CRITICAL)
    first = monitor.evaluate(STABLE)
    before = monitor.get_observability()
    assert monitor.evaluate(STABLE) == first
    assert monitor.get_observability() == before
    monitor.evaluate({**STABLE, "observation_id": str(uuid4())})
    assert monitor.get_observability()["anomaly"] is False
    monitor.close()
