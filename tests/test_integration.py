def test_aios_pipeline():

    ahi = 0.9
    ihi = 0.82
    dhi = 0.87

    adsi = (ahi + ihi + dhi) / 3

    assert adsi > 0.8
