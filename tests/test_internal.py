from pytest_apiver._internal import get_api_versions


def test_get_api_versions():
    assert get_api_versions("tests.fixtures.dummy_pkg") == [1, 2, 3]
