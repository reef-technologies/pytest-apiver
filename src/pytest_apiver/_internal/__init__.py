from __future__ import annotations

import importlib.util
import itertools
import re
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
