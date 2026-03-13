import numpy as np


def calculate_ahi(kpi_error):
    return 1 - kpi_error


def calculate_ihi(retrieval_score):
    return retrieval_score


def calculate_dhi(latency_dev, embedding_shift):
    return 1 - ((latency_dev + embedding_shift) / 2)


def calculate_adsi(metrics):

    ahi = calculate_ahi(metrics.get("kpi_error", 0))
    ihi = calculate_ihi(metrics.get("retrieval_score", 0))
    dhi = calculate_dhi(
        metrics.get("latency_dev", 0),
        metrics.get("embedding_shift", 0)
    )

    return (ahi + ihi + dhi) / 3


def detect_anomaly(history):

    if len(history) < 3:
        return False

    mean = np.mean(history)
    std = np.std(history)

    if std == 0:
        return False

    z = (history[-1] - mean) / std

    return abs(z) > 2


def detect_degradation(adsi):

    if adsi >= 0.85:
        return "stable"
    elif adsi >= 0.75:
        return "warning"
    elif adsi >= 0.65:
        return "degrading"
    else:
        return "critical"
