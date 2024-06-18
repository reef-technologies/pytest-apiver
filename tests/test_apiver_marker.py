import pytest


@pytest.mark.apiver(from_ver=2, to_ver=2)
def test_apiver_3(apiver_int):
    assert apiver_int == 2


@pytest.mark.apiver(to_ver=2)
def test_passes_below_and_on_v2(apiver_int):
    assert apiver_int <= 2


@pytest.mark.apiver(from_ver=3)
def test_passes_above_and_on_v3(apiver_int):
    assert apiver_int >= 3


@pytest.mark.apiver(from_ver=2, to_ver=3)
def test_passes_from_v2_to_v3(apiver_int):
    assert 2 <= apiver_int <= 3
