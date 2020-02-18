# cp2k-output-tools

[![Build Status](https://github.com/dev-zero/cp2k-output-tools/workflows/Run%20Tests/badge.svg)](https://github.com/dev-zero/cp2k-output-tools/actions) [![codecov](https://codecov.io/gh/dev-zero/cp2k-output-tools/branch/develop/graph/badge.svg)](https://codecov.io/gh/dev-zero/cp2k-output-tools) [![PyPI](https://img.shields.io/pypi/pyversions/cp2k-output-tools)](https://pypi.org/project/cp2k-output-tools/)

Modular CP2K output file parsers, mostly in the form of regular expressions.

## Requirements

* Python 3.6+
* regex 2020+

For development: https://poetry.eustace.io/ https://pytest.org/


## Usage

There is a simple command-line interface `cp2kparse`:

```console
$ cp2kparse calc.out
{
  "overlap_matrix_condition_number": {
    "1-norm (estimate)": {
      "CN": 113900.0,
      "Log(CN)": 5.0563,
      "|A^-1|": 7525.0,
      "|A|": 15.13
    },
    "1-norm (using diagonalization)": {
      "CN": 347700.0,
      "Log(CN)": 5.5412,
      "|A^-1|": 22980.0,
      "|A|": 15.13
    },
    "2-norm (using diagonalization)": {
      "CN": 104400.0,
      "Log(CN)": 5.0187,
      "max EV": 10.81,
      "min EV": 0.0001036
    }
  }
}
```

and an API:

```python
from cp2k_output_tools import parse_iter

with open("calc.out", "r") as fhandle:
    for match in parse_iter(fhandle.read()):
        print(match.values)
```

## Development

```console
$ poetry install
$ poetry run pytest -v
```
