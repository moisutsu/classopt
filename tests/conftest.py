import sys

import pytest


@pytest.fixture(scope="function", autouse=True)
def cleanup_args():
    # Cleanup args before each test
    # otherwise tests fail with e.g. "pytest -s" because sys.argv[1:] becomes ["-s"]
    # and pytest options will be parsed by `ArgumentParser`
    del_args()

    # Run a test...
    yield

    # Cleanup args after each test
    del_args()


def set_args(*args):
    del_args()
    for arg in args:
        sys.argv.append(arg)


def del_args():
    del sys.argv[1:]
