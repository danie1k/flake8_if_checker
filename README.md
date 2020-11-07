[![Build Status](https://travis-ci.org/danie1k/python-flake8-if-checker.svg?branch=master)](https://travis-ci.org/danie1k/python-flake8-if-checker)
[![Code Coverage](https://codecov.io/gh/danie1k/python-flake8-if-checker/branch/master/graph/badge.svg?token=A496BD37Qj)](https://codecov.io/gh/danie1k/python-flake8-if-checker)
[![MIT License](https://img.shields.io/github/license/danie1k/python-flake8-if-checker)](https://github.com/danie1k/python-flake8-if-checker/blob/master/LICENSE)

# flake8-if-checker

[Flake8](https://pypi.org/project/flake8/)'s `IF` statement complexity linter.


## Table of Contents

1. [About the Project](#about-the-project)
1. [Installation](#installation)
1. [Configuration](#usage)
1. [License](#license)


## About the Project

This plugins adds 1 new flake8 warning(s).

`IF01` Too many conditions in IF/ELIF Statement/Expression.


## Installation

```
pip install flake8-if-checker
```

## Configuration

If using the select [option from flake8](http://flake8.pycqa.org/en/latest/user/options.html#cmdoption-flake8-select)
be sure to enable the `IF` category as well.


## License

MIT
