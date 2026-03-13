def calculate_adsi(metrics):
    """
    Calculate AI Deployment Stability Index (ADSI)
    """

    kpi_error = metrics.get("kpi_error", 0)
    retrieval_score = metrics.get("retrieval_score", 0)
    latency_dev = metrics.get("latency_dev", 0)
    embedding_shift = metrics.get("embedding_shift", 0)

    ahi = 1 - kpi_error
    ihi = retrieval_score
    dhi = 1 - ((latency_dev + embedding_shift) / 2)

    adsi = (ahi + ihi + dhi) / 3

    return {
        "ADSI": adsi,
        "AHI": ahi,
        "IHI": ihi,
        "DHI": dhi
    }
