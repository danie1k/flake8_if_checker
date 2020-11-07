import os

import pytest

CWD = os.path.dirname(os.path.realpath(__file__))


@pytest.fixture
def fixture_file():
    # type: () -> str
    return os.path.join(CWD, "fixture_file.py.txt")


@pytest.fixture
def max_if_conditions():
    # type: () -> int
    return 0
