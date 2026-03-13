from src.guardrails import evaluate_guardrails


def test_guardrail_trigger():

    score = 0.5

    result = evaluate_guardrails(score)

    assert result is not None
