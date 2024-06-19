from __future__ import annotations

import importlib.util

import pytest

from pytest_apiver import _internal


def pytest_addoption(parser):
    group = parser.getgroup("apiver", "Test API versions.")
    group.addoption(
        "--target-package-name",
        action="store",
        dest="target_package_name",
        help="The name of the package to test API versions of.",
    )
    parser.addini(
        "target_package_name",
        help="The name of the package to test API versions of.",
        default=None,
    )


def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "apiver(from_ver, to_ver): run test against ApiVer interfaces of target package.",
    )


def pytest_generate_tests(metafunc):
    if "apiver" in metafunc.fixturenames:
        all_versions = getattr(metafunc.config, "apiver_all_versions", None)
        if all_versions is None:
            package_name = _internal.get_package_name(metafunc.config)
            all_versions = _internal.get_api_versions(package_name)
            metafunc.config.apiver_all_versions = all_versions

        markers = [mark for mark in metafunc.definition.iter_markers(name="apiver")]
        if markers:
            min_ver = all_versions[0]
            max_ver = all_versions[-1]
            for marker in markers:
                min_ver = max(min_ver, marker.kwargs.get("from_ver", min_ver))
                max_ver = min(max_ver, marker.kwargs.get("to_ver", max_ver))
            applicable_versions = range(min_ver, max_ver + 1)
        else:
            applicable_versions = all_versions
        metafunc.parametrize("apiver", [f"v{ver}" for ver in applicable_versions])


@pytest.fixture(scope="session")
def apiver_tested_package_name(request):
    return _internal.get_package_name(request.config)


@pytest.fixture
def apiver_int(apiver):
    """Get apiver as an int, e.g., 2."""
    return int(apiver[1:])


def _get_module_name(pkg: str, apiver, module_name: str | None = None):
    return f"{pkg}.{apiver}.{module_name}" if module_name else f"{pkg}.{apiver}"


@pytest.fixture
def apiver_import(apiver, apiver_tested_package_name):
    def importer(module_name: str | None = None):
        full_module_name = _get_module_name(apiver_tested_package_name, apiver, module_name)
        try:
            return importlib.import_module(full_module_name)
        except ModuleNotFoundError:
            unstable_full_module_name = _get_module_name(apiver_tested_package_name, f"_{apiver}", module_name)
            try:
                return importlib.import_module(unstable_full_module_name)
            except ModuleNotFoundError:
                pass
            raise ModuleNotFoundError(f"Module {full_module_name!r} or {unstable_full_module_name!r} not found.")

    return importer


@pytest.fixture
def apiver_module(apiver_import):
    module = apiver_import()
    return _internal.install_submodule_importer_getter(module)
