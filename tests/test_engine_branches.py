from src.stability_engine import (
    detect_anomaly,
    detect_degradation,
    calculate_adsi
)

def test_detect_anomaly_trigger():

    history = [0.92, 0.91, 0.93, 0.94, 0.60]

    result = detect_anomaly(history)

    assert isinstance(result, bool)


def test_detect_degradation_tiers():

    assert detect_degradation(0.90) == "stable"
    assert detect_degradation(0.80) == "warning"
    assert detect_degradation(0.70) == "degrading"
    assert detect_degradation(0.50) == "critical"


def test_adsi_three_inputs():

    result = calculate_adsi(0.9, 0.8, 0.85)

    assert "ADSI" in result
    assert result["ADSI"] <= 1.0
