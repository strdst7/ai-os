from datetime import datetime, timezone
from src.stability_engine import (
    calculate_ahi,
    calculate_ihi,
    calculate_dhi,
    calculate_adsi,
    validate_metrics,
)
from src.guardrails import evaluate_guardrails


def generate_stability_report(metrics: dict) -> dict:
    """
    Orchestrates stability score calculation + guardrail evaluation.
    """

    validate_metrics(metrics)

    # --- Core Scores ---
    ahi = calculate_ahi(metrics["kpi_error"])
    ihi = calculate_ihi(metrics["retrieval_score"])
    dhi = calculate_dhi(
        metrics["latency_dev"],
        metrics["embedding_shift"],
    )

    adsi = calculate_adsi(ahi, ihi, dhi)

    # --- Guardrails ---
    guardrail_result = evaluate_guardrails(adsi)

    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "scores": {
            "AHI": round(ahi, 3),
            "IHI": round(ihi, 3),
            "DHI": round(dhi, 3),
            "ADSI": adsi,
        },
        "stability_tier": guardrail_result.title(),
        "guardrail_flags": guardrail_result,
    }
