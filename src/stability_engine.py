from math import isfinite

import numpy as np


METRIC_NAMES = ("kpi_error", "retrieval_score", "latency_dev", "embedding_shift")


def validate_metrics(metrics):
    for name in METRIC_NAMES:
        if name not in metrics or metrics[name] is None:
            raise ValueError(f"insufficient_data: {name} is missing")
        value = metrics[name]
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not isfinite(value) or not 0 <= value <= 1:
            raise ValueError(f"invalid_data: {name} must be a finite number between 0 and 1")


def calculate_ahi(kpi_error):
    return 1 - kpi_error


def calculate_ihi(retrieval_score):
    return retrieval_score


def calculate_dhi(latency_dev, embedding_shift):
    return 1 - ((latency_dev + embedding_shift) / 2)


def calculate_adsi(metrics_or_ahi, ihi=None, dhi=None):
    """
    Compute the ADSI score.

    Accepts either:
    - a metrics dict (kpi_error, retrieval_score, latency_dev, embedding_shift), or
    - three precomputed scores: calculate_adsi(ahi, ihi, dhi)
    """
    if isinstance(metrics_or_ahi, dict):
        if ihi is not None or dhi is not None:
            raise TypeError("Pass either a metrics dict or (ahi, ihi, dhi), not both")
        metrics = metrics_or_ahi
        validate_metrics(metrics)
        ahi = calculate_ahi(metrics["kpi_error"])
        ihi = calculate_ihi(metrics["retrieval_score"])
        dhi = calculate_dhi(
            metrics["latency_dev"],
            metrics["embedding_shift"]
        )
    else:
        if ihi is None or dhi is None:
            raise TypeError("calculate_adsi requires a metrics dict or (ahi, ihi, dhi)")
        ahi = metrics_or_ahi

    return (ahi + ihi + dhi) / 3


def detect_anomaly(history):
    if len(history) < 3:
        return False

    mean = np.mean(history)
    std = np.std(history)

    if std == 0:
        return False

    z = (history[-1] - mean) / std
    return bool(abs(z) > 2)


def detect_degradation(adsi):
    if adsi >= 0.85:
        return "stable"
    elif adsi >= 0.75:
        return "warning"
    elif adsi >= 0.65:
        return "degrading"
    else:
        return "critical"
