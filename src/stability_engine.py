def calculate_adsi(*args):
    """
    Calculate AI Deployment Stability Index (ADSI)

    Supports two formats:
    1) calculate_adsi(metrics_dict)
    2) calculate_adsi(ahi, ihi, dhi)
    """

    # Case 1: metrics dictionary
    if len(args) == 1 and isinstance(args[0], dict):

        metrics = args[0]

        kpi_error = metrics.get("kpi_error", 0)
        retrieval_score = metrics.get("retrieval_score", 0)
        latency_dev = metrics.get("latency_dev", 0)
        embedding_shift = metrics.get("embedding_shift", 0)

        ahi = 1 - kpi_error
        ihi = retrieval_score
        dhi = 1 - ((latency_dev + embedding_shift) / 2)

    # Case 2: ahi, ihi, dhi provided directly
    elif len(args) == 3:

        ahi, ihi, dhi = args

    else:
        raise ValueError("Invalid arguments for calculate_adsi")

    adsi = (ahi + ihi + dhi) / 3

    return {
        "ADSI": adsi,
        "AHI": ahi,
        "IHI": ihi,
        "DHI": dhi
    }
