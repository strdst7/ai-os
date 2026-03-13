import numpy as np


def calculate_ahi(kpi_error):
    """
    Alignment Health Index
    """
    return 1 - kpi_error


def calculate_ihi(retrieval_score):
    """
    Infrastructure Health Index
    """
    return retrieval_score


def calculate_dhi(latency_dev, embedding_shift):
    """
    Drift Health Index
    """
    return 1 - ((latency_dev + embedding_shift) / 2)


def calculate_adsi(metrics):
    """
    Composite AI Deployment Stability Index
    """

    kpi_error = metrics.get("kpi_error", 0)
    retrieval_score = metrics.get("retrieval_score", 0)
    latency_dev = metrics.get("latency_dev", 0)
    embedding_shift = metrics.get("embedding_shift", 0)

    ahi = calculate_ahi(kpi_error)
    ihi = calculate_ihi(retrieval_score)
    dhi = calculate_dhi(latency_dev, embedding_shift)

    adsi = (ahi + ihi + dhi) / 3

    return {
        "ADSI": adsi,
        "AHI": ahi,
        "IHI": ihi,
        "DHI": dhi
    }


def detect_anomaly(adsi_history):
    """
    Detect anomaly using Z-score
    """

    if len(adsi_history) < 3:
        return False

    mean = np.mean(adsi_history)
    std = np.std(adsi_history)

    if std == 0:
        return False

    z = (adsi_history[-1] - mean) / std

    return abs(z) > 2


def detect_degradation(adsi):
    """
    Classify stability tier
    """

    if adsi >= 0.85:
        return "stable"
    elif adsi >= 0.75:
        return "warning"
    elif adsi >= 0.65:
        return "degrading"
    else:
        return "critical"
