import statistics


# -----------------------------
# Core Health Index Calculations
# -----------------------------

def calculate_ahi(kpi_error: float) -> float:
    return max(0.0, 1.0 - kpi_error)


def calculate_ihi(retrieval_score: float) -> float:
    return max(0.0, retrieval_score)


def calculate_dhi(latency_dev: float, embedding_shift: float) -> float:
    return max(0.0, 1.0 - ((latency_dev + embedding_shift) / 2))


def calculate_adsi(ahi: float, ihi: float, dhi: float) -> float:
    return round((ahi + ihi + dhi) / 3, 3)


# -----------------------------
# Stability Degradation Detection
# -----------------------------

def detect_degradation(history: list) -> dict:
    """
    Detect consecutive ADSI drops.
    """

    if len(history) < 3:
        return {"degrading": False}

    last_three = [entry["ADSI"] for entry in history[-3:]]

    degrading = last_three[0] > last_three[1] > last_three[2]

    return {
        "degrading": degrading,
        "trend": last_three
    }


# -----------------------------
# Z-Score Anomaly Detection
# -----------------------------

def detect_anomaly(history: list) -> dict:
    """
    Z-score anomaly detection on ADSI.
    """

    if len(history) < 5:
        return {"anomaly": False}

    values = [entry["ADSI"] for entry in history]

    mean = statistics.mean(values)
    stdev = statistics.stdev(values)

    if stdev == 0:
        return {"anomaly": False}

    latest = values[-1]
    z_score = (latest - mean) / stdev

    return {
        "anomaly": abs(z_score) > 2,
        "z_score": round(z_score, 3)
    }
