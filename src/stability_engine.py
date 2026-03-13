import numpy as np


def calculate_ahi(kpi_error):
    """Alignment Health Index"""
    return 1 - kpi_error


def calculate_ihi(retrieval_score):
    """Infrastructure Health Index"""
    return retrieval_score


def calculate_dhi(latency_dev, embedding_shift):
    """Drift Health Index"""
    return 1 - ((latency_dev + embedding_shift) / 2)


def calculate_adsi(*args):
    """
    Calculate ADSI score.

    Supports:
    calculate_adsi(metrics_dict)
    calculate_adsi(ahi, ihi, dhi)
    """

    # Case 1: metrics dictionary
    if len(args) == 1 and isinstance(args[0], dict):

        metrics = args[0]

        ahi = calculate_ahi(metrics.get("kpi_error", 0))
        ihi = calculate_ihi(metrics.get("retrieval_score", 0))
        dhi = calculate_dhi(
            metrics.get("latency_dev", 0),
            metrics.get("embedding_shift", 0),
        )

    # Case 2: direct indices
    elif len(args) == 3:

        ahi, ihi, dhi = args

    else:
        raise ValueError("Invalid ADSI inputs")

    return (ahi + ihi + dhi) / 3


def detect_anomaly(adsi_history):
    """Detect anomaly using Z-score"""

    if len(adsi_history) < 3:
        return False

    mean = np.mean(adsi_history)
    std = np.std(adsi_history)

    if std == 0:
        return False

    z = (adsi_history[-1] - mean) / std

    return abs(z) > 2


def detect_degradation(adsi):
    """Classify stability tier"""

    if adsi >= 0.85:
        return "stable"
    elif adsi >= 0.75:
        return "warning"
    elif adsi >= 0.65:
        return "degrading"
    else:
        return "critical"
