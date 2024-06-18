# pytest_apiver
&nbsp;[![Continuous Integration](https://github.com/reef-technologies/pytest_apiver/workflows/Continuous%20Integration/badge.svg)](https://github.com/reef-technologies/pytest_apiver/actions?query=workflow%3A%22Continuous+Integration%22)&nbsp;[![License](https://img.shields.io/pypi/l/pytest_apiver.svg?label=License)](https://pypi.python.org/pypi/pytest_apiver)&nbsp;[![python versions](https://img.shields.io/pypi/pyversions/pytest_apiver.svg?label=python%20versions)](https://pypi.python.org/pypi/pytest_apiver)&nbsp;[![PyPI version](https://img.shields.io/pypi/v/pytest_apiver.svg?label=PyPI%20version)](https://pypi.python.org/pypi/pytest_apiver)

Pytest plugin helping to test packages implementing [ApiVer](https://www.youtube.com/watch?v=FgcoAKchPjk). 

## Usage

Assuming your package exposes `v1`, `v2`, ... ApiVer interfaces, i.e. has structure like this:
```
my_package/
    __init__.py
    v1/
        __init__.py
    ...
    _v3/
        __init__.py
```

You can configure to run apiver-aware tests against it using `pyproject.toml`:
```toml
[tool.pytest.ini_options]
target_package_name = "my_package"
```

Then you can write tests like this:
```
@pytest.mark.apiver(from_ver=2, to_ver=3)
def test_run_for_apiver_ver_2_3(apiver_module):
    assert apiver_module.func()
```

Which will run test against `my_package.v2.func()` and `my_package.v3.func()` respectively.

For non-flat package structure, you can use auto-magical getter doing imports of submodules built into `apiver_module` fixture, e.g.:
```
@pytest.mark.apiver(from_ver=2, to_ver=2)
def test_func__v2(apiver_module):
    assert apiver_module.utils.func()  # equivalent to my_package.v2.utils.func()
```


## Versioning

This package uses [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
TL;DR you are safe to use [compatible release version specifier](https://packaging.python.org/en/latest/specifications/version-specifiers/#compatible-release) `~=MAJOR.MINOR` in your `pyproject.toml` or `requirements.txt`.

Internal packages, i.e. prefixed by `pytest_apiver._` do not share these guarantees and may change in a backwards-incompatible way at any time even in patch releases.


## Development


Pre-requisites:
- [pdm](https://pdm.fming.dev/)
- [nox](https://nox.thea.codes/en/stable/)
- [docker](https://www.docker.com/) and [docker compose plugin](https://docs.docker.com/compose/)


Ideally, you should run `nox -t format lint` before every commit to ensure that the code is properly formatted and linted.
Before submitting a PR, make sure that tests pass as well, you can do so using:
```
nox -t check # equivalent to `nox -t format lint test`
```

If you wish to install dependencies into `.venv` so your IDE can pick them up, you can do so using:
```
pdm install --dev
```

### Release process

Run `nox -s make_release -- X.Y.Z` where `X.Y.Z` is the version you're releasing and follow the printed instructions.
