from src.guardrails import evaluate_guardrails

def test_guardrail_trigger():
    evaluate_guardrails(score=0.6)
        adsi=0.5,
        latency_dev=0.3,
        drift=0.2,
        token_volatility=0.4
    )
    assert len(events) > 0
