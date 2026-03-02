from src.stability_engine import calculate_adsi


def test_stability_calculation():
    sample_metrics = {
        "kpi_error": 0.1,
        "embedding_shift": 0.05,
        "retrieval_score": 0.9,
        "latency_dev": 0.1
    }

    result = calculate_adsi(sample_metrics)

    assert "ADSI" in result
    assert result["ADSI"] <= 1.0
    assert result["ADSI"] >= 0.0
