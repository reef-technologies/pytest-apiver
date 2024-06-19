import sys

from pytest_apiver._internal import (
    copy_module,
    get_api_versions,
    install_submodule_importer_getter,
)


def test_get_api_versions():
    assert get_api_versions("tests.fixtures.dummy_pkg") == [1, 2, 3]


def test_copy_module():
    import sys

    sys_copy = copy_module(sys)

    assert sys.path is sys_copy.path

    sys_copy.dummy = 1
    assert sys_copy.dummy == 1
    assert not hasattr(sys, "dummy")


def test_install_submodule_importer_getter():
    # remove multiprocessing from sys.modules to simulate not imported yet
    sys.modules.pop("multiprocessing", None)

    import multiprocessing

    assert not hasattr(multiprocessing, "queues")  #  sanity check: not imported yet

    augmented_multiprocessing_module = install_submodule_importer_getter(multiprocessing)

    # test auto-import
    assert augmented_multiprocessing_module.queues.Queue is multiprocessing.queues.Queue

    # test nested auto-import
    assert augmented_multiprocessing_module.dummy.connection.Listener is multiprocessing.dummy.connection.Listener
