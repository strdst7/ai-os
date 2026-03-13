from src.stability_engine import calculate_adsi

def test_adsi_range():
    score = calculate_adsi(0.9, 0.8, 0.85)
    assert 0 <= score <= 1
