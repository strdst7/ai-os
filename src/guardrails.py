from src.config import GuardrailConfig


def evaluate_guardrails(metrics: dict) -> dict:
    """
    Evaluate runtime stability guardrails
    using configurable thresholds.
    """

    latency_dev = metrics.get("latency_dev", 0.0)
    drift = metrics.get("embedding_shift", 0.0)
    token_volatility = metrics.get("token_volatility", 0.0)

    flags = {
        "latency_breach": latency_dev > GuardrailConfig.LATENCY_THRESHOLD,
        "drift_breach": drift > GuardrailConfig.DRIFT_THRESHOLD,
        "cost_volatility_breach": token_volatility > GuardrailConfig.COST_VOLATILITY_THRESHOLD,
    }

    return {
        "flags": flags,
        "overall_risk": any(flags.values())
    }
