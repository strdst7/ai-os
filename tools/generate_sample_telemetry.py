"""Generate data/sample_telemetry.json.

Produces a deterministic 500-cycle synthetic telemetry series with three
degradation phases (stable, warning, critical). Field names match the
``Telemetry`` schema in src/models.py exactly (``latency_dev``, not
``latency_deviation``).

Usage:
    python tools/generate_sample_telemetry.py
"""
import json
import random
from datetime import datetime, timedelta, timezone
from pathlib import Path

OUTPUT = Path(__file__).resolve().parents[1] / "data" / "sample_telemetry.json"

CYCLES = 500
START = datetime(2026, 1, 1, tzinfo=timezone.utc)
STEP = timedelta(minutes=1)
SEED = 7

# (name, cycle count, starting targets, drift per cycle).
# Phase 1 settles near ADSI 0.95 (stable). Phase 2 declines into the warning
# band (~0.75-0.85). Phase 3 crosses 0.65 into critical. Values stay in [0, 1].
PHASES = (
    ("stable", 200, {"kpi_error": 0.04, "retrieval_score": 0.94,
                     "latency_dev": 0.05, "embedding_shift": 0.03},
     {"kpi_error": -0.0001, "retrieval_score": 0.00002,
      "latency_dev": 0.0002, "embedding_shift": -0.0001}),
    ("warning", 180, {"kpi_error": 0.0, "retrieval_score": 0.95,
                      "latency_dev": 0.12, "embedding_shift": 0.0},
     {"kpi_error": 0.00067, "retrieval_score": -0.00083,
      "latency_dev": 0.0018, "embedding_shift": 0.0014}),
    ("critical", 120, None,
     {"kpi_error": 0.0025, "retrieval_score": -0.00208,
      "latency_dev": 0.0025, "embedding_shift": 0.00167}),
)


def clamp(value):
    return round(min(1.0, max(0.0, value)), 4)


def main():
    rng = random.Random(SEED)
    records = []
    current = dict(PHASES[0][2])
    cycle = 0
    for _name, count, _start, drift in PHASES:
        for _ in range(count):
            for key in current:
                current[key] += drift[key] + rng.uniform(-0.004, 0.004)
            metrics = {key: clamp(value) for key, value in current.items()}
            records.append({
                "timestamp": (START + cycle * STEP).isoformat().replace("+00:00", "Z"),
                **metrics,
            })
            cycle += 1

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(records, indent=2) + "\n")
    print(f"wrote {len(records)} records to {OUTPUT}")


if __name__ == "__main__":
    main()
