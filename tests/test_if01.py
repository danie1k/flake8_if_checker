import ast
import os

import pytest

import flake8_if_checker

try:
    from typing import Tuple
except ImportError:
    pass


@pytest.fixture
def report_getter(fixture_file, max_if_conditions):
    # type: (str, int) -> Tuple[flake8_if_checker.IfCheckerReportItem]
    with open(fixture_file, "r") as fobj:
        tree = ast.parse(fobj.read(), os.path.basename(fixture_file))
        fobj.seek(0)
        lines = fobj.readlines()

    checker = flake8_if_checker.IfChecker(
        tree=tree,
        lines=lines,
        options=type(  # type:ignore
            "Options", (object,), {"max_if_conditions": max_if_conditions}
        ),
    )

    return tuple(checker.run())  # type:ignore


EXPECTED_REPORTS = [
    # No  Line Col  Count Type    Kind
    # 001 -------------------------------------
    (0, 2, 0, 1, "IF", "Statement"),
    (1, 5, 12, 1, "IF", "Statement"),
    (2, 7, 0, 2, "ELIF", "Statement"),
    (3, 11, 12, 2, "IF", "Statement"),
    (4, 16, 12, 2, "IF", "Statement"),
    (5, 19, 0, 2, "ELIF", "Statement"),
    (6, 22, 12, 1, "IF", "Statement"),
    (7, 27, 12, 1, "IF", "Statement"),
    # 002 -------------------------------------
    (8, 32, 0, 1, "IF", "Statement"),
    # 003 -------------------------------------
    (9, 39, 0, 1, "IF", "Statement"),
    (10, 41, 0, 1, "ELIF", "Statement"),
    # 004 -------------------------------------
    (11, 45, 0, 1, "IF", "Statement"),
    (12, 47, 0, 1, "ELIF", "Statement"),
    # 005 -------------------------------------
    (13, 54, 0, 2, "IF", "Statement"),
    # 006 -------------------------------------
    (14, 59, 0, 2, "IF", "Statement"),
    (15, 61, 0, 2, "ELIF", "Statement"),
    # 007 -------------------------------------
    (16, 66, 0, 2, "IF", "Statement"),
    # 008 -------------------------------------
    (17, 71, 0, 2, "IF", "Statement"),
    # 009 -------------------------------------
    (18, 77, 0, 2, "IF", "Statement"),
    # 010 -------------------------------------
    (19, 86, 0, 2, "IF", "Statement"),
    # 011 -------------------------------------
    (20, 93, 30, 1, "IF", "Expression"),
    # 012 -------------------------------------
    (21, 97, 0, 6, "IF", "Statement"),
    # 013 -------------------------------------
    (22, 106, 0, 5, "IF", "Statement"),
    (23, 109, 58, 1, "IF", "Expression"),
    (24, 111, 0, 3, "ELIF", "Statement"),
    # 014 -------------------------------------
    (25, 118, 0, 2, "IF", "Statement"),
    # 015 -------------------------------------
    (26, 122, 0, 2, "IF", "Statement"),
    # 016 -------------------------------------
    (27, 130, 0, 4, "IF", "Statement"),
    # 017 -------------------------------------
    (28, 135, 0, 2, "IF", "Statement"),
    # 018 -------------------------------------
    (29, 140, 0, 3, "IF", "Statement"),
    (30, 140, 9, 2, "IF", "Expression"),
    # 019 -------------------------------------
    (31, 146, 0, 1, "IF", "Statement"),
    (32, 147, 4, 1, "IF", "Statement"),
    (33, 148, 8, 1, "IF", "Statement"),
    (34, 151, 8, 1, "IF", "Statement"),
    (35, 153, 8, 1, "ELIF", "Statement"),
    (36, 154, 12, 1, "IF", "Statement"),
    (37, 157, 16, 1, "IF", "Statement"),
    # 020 -------------------------------------
    (38, 164, 0, 4, "IF", "Statement"),
    (39, 164, 9, 1, "IF", "Expression"),
    (40, 164, 9, 1, "IF", "Expression"),  # FIXME: Malformed check, should be col 18
]


@pytest.mark.parametrize(  # type:ignore
    "index,line,col,condition_count,type,kind", EXPECTED_REPORTS
)  # pylint:disable=too-many-arguments
def test_if01_error(
    report_getter, index, line, col, condition_count, type, kind
):  # pylint:disable=redefined-outer-name,redefined-builtin
    # type: (Tuple[tuple, ...], int, int, int, int, str, str) -> None
    report_result = report_getter[index][:-1]
    expected_result = (
        line,
        col,
        flake8_if_checker.IfCheckerErrors.IF01.value.format(
            line=line, col=col, type=type, kind=kind, condition_count=condition_count
        ),
    )
    assert report_result == expected_result
