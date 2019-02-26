import ast
import os
import pytest
import typing

from flake8_if_checker import IfChecker, IfCheckerErrors

PWD = os.path.dirname(os.path.realpath(__file__))
MSG = IfCheckerErrors.IF01.value
COL = 0
FILE_NAME = 'test1.py'

@pytest.fixture
def report():
    class Options:
        max_if_conditions = 0

    with open(os.path.join(PWD, FILE_NAME), 'r') as file:
        tree = ast.parse(file.read(), FILE_NAME)
        file.seek(0)
        lines = file.readlines()

    checker = IfChecker(
        tree=tree,
        lines=lines,
        options=Options(),
    )

    return tuple(checker.run())


EXPECTED_REPORTS = [
    # No  Line Col  Count Type    Kind
    # 001 -------------------------------------
    (0,   2,   0,   1,    'IF',   'Statement'),
    (1,   5,   12,  1,    'IF',   'Statement'),
    (2,   7,   0,   2,    'ELIF', 'Statement'),
    (3,   11,  12,  2,    'IF',   'Statement'),
    (4,   16,  12,  2,    'IF',   'Statement'),
    (5,   19,  0,   2,    'ELIF', 'Statement'),
    (6,   22,  12,  1,    'IF',   'Statement'),
    (7,   27,  12,  1,    'IF',   'Statement'),

    # 002 -------------------------------------
    (8,   32,  0,   1,    'IF',   'Statement'),

    # 003 -------------------------------------
    (9,   39,  0,   1,    'IF',   'Statement'),
    (10,  41,  0,   1,    'ELIF', 'Statement'),

    # 004 -------------------------------------
    (11,  45,  0,   1,    'IF',   'Statement'),
    (12,  47,  0,   1,    'ELIF', 'Statement'),

    # 005 -------------------------------------
    (13,  54,  0,   2,    'IF',   'Statement'),

    # 006 -------------------------------------
    (14,  59,  0,   2,    'IF',   'Statement'),
    (15,  61,  0,   2,    'ELIF', 'Statement'),

    # 007 -------------------------------------
    (16,  66,  0,   2,    'IF',   'Statement'),

    # 008 -------------------------------------
    (17,  71,  0,   2,    'IF',   'Statement'),

    # 009 -------------------------------------
    (18,  77,  0,   2,    'IF',   'Statement'),

    # 010 -------------------------------------
    (19,  86,  0,   2,    'IF',   'Statement'),

    # 011 -------------------------------------
    (20,  93,  15,  1,    'IF',   'Expression'),

    # 012 -------------------------------------
    (21,  97,  0,   6,    'IF',   'Statement'),

    # 013 -------------------------------------
    (22, 106,  0,   5,    'IF',   'Statement'),
    (23, 109,  26,  1,    'IF',   'Expression'),
    (24, 111,  0,   3,    'ELIF', 'Statement'),

    # 014 -------------------------------------
    (25, 118,  0,   2,    'IF',   'Statement'),

    # 015 -------------------------------------
    (26, 122,  0,   2,    'IF',   'Statement'),

    # 016 -------------------------------------
    (27, 130,  0,   4,    'IF',   'Statement'),

    # 017 -------------------------------------
    (28, 135,  0,   2,    'IF',   'Statement'),

    # 018 -------------------------------------
    (29, 140,  0,   3,    'IF',   'Statement'),
    (30, 140,  4,   2,    'IF',   'Expression'),

    # 019 -------------------------------------
    (31, 146,  0,   1,    'IF',   'Statement'),
    (32, 147,  4,   1,    'IF',   'Statement'),
    (33, 148,  8,   1,    'IF',   'Statement'),
    (34, 151,  8,   1,    'IF',   'Statement'),
    (35, 153,  8,   1,    'ELIF', 'Statement'),
    (36, 154,  12,  1,    'IF',   'Statement'),
    (37, 157,  16,  1,    'IF',   'Statement'),

    # 020 -------------------------------------
    (38, 164,  0,   4,    'IF',  'Statement'),
    (39, 164,  4,   1,    'IF',  'Expression'),
    (40, 164,  13,  1,    'IF',  'Expression'),
]


@pytest.mark.parametrize('index,line,col,condition_count,type,kind', EXPECTED_REPORTS)
def test_if01_error(
        report: typing.Tuple[tuple, ...],
        index: int,
        line: int,
        col: int,
        condition_count: int,
        type: str,
        kind: str,
):
    report_result = report[index][:-1]
    expected_result = (
        line,
        col,
        MSG.format(
            line=line,
            col=col,
            type=type,
            kind=kind,
            condition_count=condition_count,
        ),
    )
    assert report_result == expected_result
