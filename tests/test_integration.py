import os
import runpy
import sys
import textwrap

from _pytest.capture import CaptureFixture  # pylint:disable=unused-import

try:
    from unittest import mock
except ImportError:
    import mock  # type:ignore

import pytest

CWD = os.path.dirname(os.path.realpath(__file__))


def test_flake8_integration(fixture_file, max_if_conditions, capsys):  # type:ignore
    # type: (str, int, CaptureFixture) -> None
    given_flake8_arguments = [
        "flake8",
        "--select=IF0",
        "--max-if-conditions",
        str(max_if_conditions),
        os.path.basename(fixture_file),
    ]
    expected_result = textwrap.dedent(
        """
        {fixture_file}:2:1: IF01 Too many conditions (1) in IF Statement
        {fixture_file}:5:13: IF01 Too many conditions (1) in IF Statement
        {fixture_file}:7:1: IF01 Too many conditions (2) in ELIF Statement
        {fixture_file}:11:13: IF01 Too many conditions (2) in IF Statement
        {fixture_file}:16:13: IF01 Too many conditions (2) in IF Statement
        {fixture_file}:19:1: IF01 Too many conditions (2) in ELIF Statement
        {fixture_file}:22:13: IF01 Too many conditions (1) in IF Statement
        {fixture_file}:27:13: IF01 Too many conditions (1) in IF Statement
        {fixture_file}:32:1: IF01 Too many conditions (1) in IF Statement
        {fixture_file}:39:1: IF01 Too many conditions (1) in IF Statement
        {fixture_file}:41:1: IF01 Too many conditions (1) in ELIF Statement
        {fixture_file}:45:1: IF01 Too many conditions (1) in IF Statement
        {fixture_file}:47:1: IF01 Too many conditions (1) in ELIF Statement
        {fixture_file}:54:1: IF01 Too many conditions (2) in IF Statement
        {fixture_file}:59:1: IF01 Too many conditions (2) in IF Statement
        {fixture_file}:61:1: IF01 Too many conditions (2) in ELIF Statement
        {fixture_file}:66:1: IF01 Too many conditions (2) in IF Statement
        {fixture_file}:71:1: IF01 Too many conditions (2) in IF Statement
        {fixture_file}:77:1: IF01 Too many conditions (2) in IF Statement
        {fixture_file}:86:1: IF01 Too many conditions (2) in IF Statement
        {fixture_file}:93:16: IF01 Too many conditions (1) in IF Expression
        {fixture_file}:97:1: IF01 Too many conditions (6) in IF Statement
        {fixture_file}:106:1: IF01 Too many conditions (5) in IF Statement
        {fixture_file}:109:27: IF01 Too many conditions (1) in IF Expression
        {fixture_file}:111:1: IF01 Too many conditions (3) in ELIF Statement
        {fixture_file}:118:1: IF01 Too many conditions (2) in IF Statement
        {fixture_file}:122:1: IF01 Too many conditions (2) in IF Statement
        {fixture_file}:130:1: IF01 Too many conditions (4) in IF Statement
        {fixture_file}:135:1: IF01 Too many conditions (2) in IF Statement
        {fixture_file}:140:1: IF01 Too many conditions (3) in IF Statement
        {fixture_file}:140:5: IF01 Too many conditions (2) in IF Expression
        {fixture_file}:146:1: IF01 Too many conditions (1) in IF Statement
        {fixture_file}:147:5: IF01 Too many conditions (1) in IF Statement
        {fixture_file}:148:9: IF01 Too many conditions (1) in IF Statement
        {fixture_file}:151:9: IF01 Too many conditions (1) in IF Statement
        {fixture_file}:153:9: IF01 Too many conditions (1) in ELIF Statement
        {fixture_file}:154:13: IF01 Too many conditions (1) in IF Statement
        {fixture_file}:157:17: IF01 Too many conditions (1) in IF Statement
        {fixture_file}:164:1: IF01 Too many conditions (4) in IF Statement
        {fixture_file}:164:5: IF01 Too many conditions (1) in IF Expression
        {fixture_file}:164:14: IF01 Too many conditions (1) in IF Expression
        {fixture_file}:176:5: IF01 Too many conditions (4) in IF Statement
        {fixture_file}:177:14: IF01 Too many conditions (1) in IF Expression
        """.format(
            fixture_file=os.path.basename(fixture_file)
        )
    )

    os.chdir(os.path.dirname(fixture_file))
    with pytest.raises(SystemExit), mock.patch.object(
        sys, "argv", given_flake8_arguments
    ):
        runpy.run_module("flake8")

    captured = capsys.readouterr()
    assert captured.out.strip() == expected_result.strip()
