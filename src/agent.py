from datetime import datetime
from src.stability_engine import (
    calculate_ahi,
    calculate_ihi,
    calculate_dhi,
    calculate_adsi,
)
from src.guardrails import evaluate_guardrails


def generate_stability_report(metrics: dict) -> dict:
    """
    Orchestrates stability score calculation + guardrail evaluation.
    """

    # --- Core Scores ---
    ahi = calculate_ahi(metrics.get("kpi_error", 0.0))
    ihi = calculate_ihi(metrics.get("retrieval_score", 0.0))
    dhi = calculate_dhi(
        metrics.get("latency_dev", 0.0),
        metrics.get("embedding_shift", 0.0),
    )

    adsi = calculate_adsi(ahi, ihi, dhi)

    # --- Guardrails ---
    guardrail_result = evaluate_guardrails(metrics)

    # --- Stability Tier ---
    if adsi >= 0.85:
        tier = "Stable"
    elif adsi >= 0.65:
        tier = "Warning"
    else:
        tier = "Critical"

    return {
        "timestamp": datetime.utcnow().isoformat(),
        "scores": {
            "AHI": round(ahi, 3),
            "IHI": round(ihi, 3),
            "DHI": round(dhi, 3),
            "ADSI": adsi,
        },
        "stability_tier": tier,
        "guardrail_flags": guardrail_result,
    }
