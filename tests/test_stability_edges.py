from src.stability_engine import calculate_adsi


def test_adsi_upper_bound():

    metrics = {
        "kpi_error": 0.0,
        "embedding_shift": 0.0,
        "retrieval_score": 1.0,
        "latency_dev": 0.0
    }

    result = calculate_adsi(metrics)

    assert result <= 1.0


def test_adsi_lower_bound():

    metrics = {
        "kpi_error": 1.0,
        "embedding_shift": 1.0,
        "retrieval_score": 0.0,
        "latency_dev": 1.0
    }

    result = calculate_adsi(metrics)

    assert result >= 0.0
