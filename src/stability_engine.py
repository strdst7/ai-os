def calculate_adsi(*args):
    """
    Calculate ADSI score
    Supports:
    calculate_adsi(metrics_dict)
    calculate_adsi(ahi, ihi, dhi)
    """

    # case 1: metrics dict
    if len(args) == 1 and isinstance(args[0], dict):

        metrics = args[0]

        kpi_error = metrics.get("kpi_error", 0)
        retrieval_score = metrics.get("retrieval_score", 0)
        latency_dev = metrics.get("latency_dev", 0)
        embedding_shift = metrics.get("embedding_shift", 0)

        ahi = 1 - kpi_error
        ihi = retrieval_score
        dhi = 1 - ((latency_dev + embedding_shift) / 2)

    # case 2: ahi, ihi, dhi directly
    elif len(args) == 3:

        ahi, ihi, dhi = args

    else:
        raise ValueError("Invalid ADSI inputs")

    return (ahi + ihi + dhi) / 3
