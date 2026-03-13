from src.stability_engine import calculate_adsi


def test_stability_calculation():

    ahi = 0.9
    ihi = 0.85
    dhi = 0.88

    score = calculate_adsi(ahi, ihi, dhi)

    assert score <= 1.0
    assert score >= 0.0
