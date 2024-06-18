import pytest


def test_apiver_module(apiver_module):
    assert "dummy_pkg" in apiver_module.__file__


def test_apiver_module__foo(apiver_module, apiver_int):
    assert apiver_module.foo() == f"foo_v{apiver_int}"


@pytest.mark.apiver(to_ver=2)
def test_apiver_import__utils__module_not_found(apiver_import):
    with pytest.raises(ModuleNotFoundError):
        apiver_import("utils")


@pytest.mark.apiver(from_ver=3)
def test_apiver_import__dummy_util(apiver_import):
    assert apiver_import("utils").dummy_util() == 1


@pytest.mark.apiver(from_ver=3)
def test_apiver_module__dummy_util(apiver_module):
    assert apiver_module.utils.dummy_util() == 1
