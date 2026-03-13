import numpy as np


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
