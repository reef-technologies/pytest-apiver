from __future__ import annotations

import copy
import importlib.util
import itertools
import re
import types
from pathlib import Path


def get_package_name(config) -> str:
    package_name = config.getoption("target_package_name") or config.getini("target_package_name")
    assert package_name, "The --target-package-name CLI option or target_package_name INI option is required."
    return package_name


def get_api_versions(package_name: str) -> list[int]:
    versions = set()

    package_spec = importlib.util.find_spec(package_name)
    if not package_spec:
        raise ValueError(f"Package {package_name=!r} not found. Possibly `--target-package-name` is incorrect.")
    assert package_spec.origin
    package_path = Path(package_spec.origin).parent

    for apiver_package_path in itertools.chain(
        package_path.glob("*v*/__init__.py"),
        package_path.glob("*v*.py"),
    ):
        match = re.search(r"/_?v(\d+)(:?\.py|/__init__\.py)$", str(apiver_package_path))
        if match:
            versions.add(int(match.group(1)))
    assert versions, f"No API versions found in {package_path!r}"
    return sorted(versions)


def copy_module(original_module):
    # Create a new module object
    new_module = types.ModuleType(original_module.__name__)

    # Copy the dictionary of the original module
    new_module.__dict__.update(copy.copy(original_module.__dict__))

    return new_module


def install_submodule_importer_getter(module):
    module = copy_module(module)

    def __getattr__(name):
        try:
            submodule = importlib.import_module(f"{module.__name__}.{name}")
        except ModuleNotFoundError:
            raise AttributeError(f"module {module.__name__!r} has no attribute {name!r} nor submodule of that name")
        return install_submodule_importer_getter(submodule)

    module.__getattr__ = __getattr__
    return module
