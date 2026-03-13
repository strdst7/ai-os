def evaluate_guardrails(adsi):
    """
    Evaluate deployment stability and return guardrail state.
    """

    if adsi >= 0.85:
        return "stable"

    elif adsi >= 0.75:
        return "warning"

    elif adsi >= 0.65:
        return "degrading"

    else:
        return "critical"
