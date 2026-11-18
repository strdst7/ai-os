import json
from pathlib import Path

from src.models import Telemetry
from src.stability_engine import calculate_adsi, detect_degradation

DATA = Path(__file__).resolve().parents[1] / "data" / "sample_telemetry.json"
METRICS = ("kpi_error", "retrieval_score", "latency_dev", "embedding_shift")


def load_records():
    return json.loads(DATA.read_text())


def test_sample_telemetry_is_valid_json():
    # Regression: this file was previously prose, not JSON, and failed to parse.
    assert isinstance(load_records(), list)


def test_every_record_matches_the_telemetry_schema():
    records = load_records()
    assert records
    for record in records:
        model = Telemetry(**{k: record[k] for k in METRICS})
        assert 0.0 <= model.kpi_error <= 1.0


def test_sample_telemetry_spans_all_stability_tiers():
    tiers = {
        detect_degradation(calculate_adsi({k: record[k] for k in METRICS}))
        for record in load_records()
    }
    assert {"stable", "warning", "degrading", "critical"} <= tiers
