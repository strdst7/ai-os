def calculate_adsi(*args):

    if len(args) == 1 and isinstance(args[0], dict):

        metrics = args[0]

        ahi = calculate_ahi(metrics.get("kpi_error", 0))
        ihi = calculate_ihi(metrics.get("retrieval_score", 0))
        dhi = calculate_dhi(
            metrics.get("latency_dev", 0),
            metrics.get("embedding_shift", 0),
        )

    elif len(args) == 3:

        ahi, ihi, dhi = args

    else:
        raise ValueError("Invalid ADSI inputs")

    adsi = (ahi + ihi + dhi) / 3

    return {
        "AHI": ahi,
        "IHI": ihi,
        "DHI": dhi,
        "ADSI": adsi
    }
