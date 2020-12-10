# cp2k-output-tools

[![Build Status](https://github.com/cp2k/cp2k-output-tools/workflows/tests/badge.svg)](https://github.com/cp2k/cp2k-output-tools/actions) [![codecov](https://codecov.io/gh/cp2k/cp2k-output-tools/branch/develop/graph/badge.svg)](https://codecov.io/gh/cp2k/cp2k-output-tools) [![PyPI](https://img.shields.io/pypi/pyversions/cp2k-output-tools)](https://pypi.org/project/cp2k-output-tools/)

Modular CP2K output file parsers, mostly in the form of regular expressions plus other tools to mangle various CP2K output:

  * `cp2kparse` ... parse CP2K output (for restart & input files look at the [cp2k-input-tools](https://github.com/cp2k/cp2k-input-tools) project)
  * `xyz_restart_parser` ... when restarts occur during an MD you may end up with duplicated frames in the trajectory, this tool filters them
  * `cp2k_bs2csv` ... convert a CP2K band structure file to multiple (one-per-set) CSV files for easier plotting. There is also an API available if you need to import bandstructure data into your application.
  * `cp2k_pdos` ... bring CP2Ks PDOS dump into a more CSV-like form for easier plotting/parsing

## Requirements

* Python 3.6+
* regex 2020+

For development: https://poetry.eustace.io/ https://pytest.org/


## Usage: cp2kparse

There is a simple command-line interface `cp2kparse`:

```console
$ cp2kparse --help
usage: cp2kparse [-h] [-y] [-k <path>] [<file>]

Parse the CP2K output file and return a JSON

positional arguments:
  <file>                CP2K output file, stdin if not specified

optional arguments:
  -h, --help            show this help message and exit
  -y, --yaml            output yaml instead of json
  -k <path>, --key <path>
                        Path, ex.: 'energies/total force_eval'

$ cp2kparse calc.out
{
  "cp2k": {
    "cp2kflags: libint fftw3 libxc xsmm spglib": " ",
    "data directory path": "/data/tiziano/cp2k/data",
    "input file name": "Si-supercell-001.inp",
    "is freely available from": "https://www.cp2k.org/",
    "program compiled at": "Mon Sep 16 14:42:43 CEST 2019",
    "program compiled for": "local",
    "program compiled on": "tcpc18",
    "source code revision number": "git:43f50e2",
    "version string": "CP2K version 7.0 (Development Version)"
  },
  "dbcsr": {
    "cpu multiplication driver": "XSMM",
    "maximum elements for images": "UNLIMITED",
    "multiplication size stacks": 3,
    "multiplication stack size": 1000,
    "multiplicative factor virtual images": 1,
    "multrec recursion limit": 512,
    "use multiplication densification": true
  },
  "energies": {
    "total force_eval": -251.6873903110507
  },
  "global": {
    "all-to-all communication in single precision": false,
    "basis set file name": "BASIS_MOLOPT",
    "coordinate file name": "__STD_INPUT__",
    "cpu model name": "Intel(R) Core(TM) i7-4790 CPU @ 3.60GHz",
    "cpuid": 1002,
    "ffts using library dependent lengths": false,
    "force environment number": 1,
    "global print level": "MEDIUM",
    "method name": "CP2K",
    "mm potential file name": "MM_POTENTIAL",
    "mpi i/o enabled": true,
    "number of threads for this process": 1,
    "potential file name": "POTENTIAL",
    "preferred diagonalization lib.": "SL",
    "preferred fft library": "FFTW3",
    "project name": "Si-supercell-001",
    "run type": "ENERGY_FORCE",
    "this output is from process": 0,
    "total number of message passing processes": 1
  },
  "mulliken population analysis": {
    "per atom": [
      {
        "charge": 7e-06,
        "element": "Si",
        "kind": 1,
        "population": 3.999993
      },
      {
        "charge": 0.0,
        "element": "Si",
        "kind": 1,
        "population": 4.0
      },
      {
        "charge": -0.0,
        "element": "Si",
        "kind": 1,
        "population": 4.0
      },
      {
        "charge": -1e-06,
        "element": "Si",
        "kind": 1,
        "population": 4.000001
      },
      {
        "charge": -0.0,
        "element": "Si",
        "kind": 1,
        "population": 4.0
      },
      {
        "charge": -1e-06,
        "element": "Si",
        "kind": 1,
        "population": 4.000001
      },
      {
        "charge": -1e-06,
        "element": "Si",
        "kind": 1,
        "population": 4.000001
      },
      {
        "charge": -0.0,
        "element": "Si",
        "kind": 1,
        "population": 4.0
      },
      {
        "charge": 0.000137,
        "element": "Si",
        "kind": 1,
        "population": 3.999863
      },
      {
        "charge": -2e-05,
        "element": "Si",
        "kind": 1,
        "population": 4.00002
      },
      {
        "charge": -0.000133,
        "element": "Si",
        "kind": 1,
        "population": 4.000133
      },
      {
        "charge": 2.1e-05,
        "element": "Si",
        "kind": 1,
        "population": 3.999979
      },
      {
        "charge": -0.000133,
        "element": "Si",
        "kind": 1,
        "population": 4.000133
      },
      {
        "charge": 2.1e-05,
        "element": "Si",
        "kind": 1,
        "population": 3.999979
      },
      {
        "charge": 0.000137,
        "element": "Si",
        "kind": 1,
        "population": 3.999863
      },
      {
        "charge": -2e-05,
        "element": "Si",
        "kind": 1,
        "population": 4.00002
      },
      {
        "charge": -3.9e-05,
        "element": "Si",
        "kind": 1,
        "population": 4.000039
      },
      {
        "charge": 3.6e-05,
        "element": "Si",
        "kind": 1,
        "population": 3.999964
      },
      {
        "charge": -1e-05,
        "element": "Si",
        "kind": 1,
        "population": 4.00001
      },
      {
        "charge": 1e-05,
        "element": "Si",
        "kind": 1,
        "population": 3.99999
      },
      {
        "charge": -3.9e-05,
        "element": "Si",
        "kind": 1,
        "population": 4.000039
      },
      {
        "charge": 3.6e-05,
        "element": "Si",
        "kind": 1,
        "population": 3.999964
      },
      {
        "charge": -1e-05,
        "element": "Si",
        "kind": 1,
        "population": 4.00001
      },
      {
        "charge": 1e-05,
        "element": "Si",
        "kind": 1,
        "population": 3.99999
      },
      {
        "charge": -3.9e-05,
        "element": "Si",
        "kind": 1,
        "population": 4.000039
      },
      {
        "charge": 3.6e-05,
        "element": "Si",
        "kind": 1,
        "population": 3.999964
      },
      {
        "charge": -3.9e-05,
        "element": "Si",
        "kind": 1,
        "population": 4.000039
      },
      {
        "charge": 3.6e-05,
        "element": "Si",
        "kind": 1,
        "population": 3.999964
      },
      {
        "charge": -1e-05,
        "element": "Si",
        "kind": 1,
        "population": 4.00001
      },
      {
        "charge": 1e-05,
        "element": "Si",
        "kind": 1,
        "population": 3.99999
      },
      {
        "charge": -1e-05,
        "element": "Si",
        "kind": 1,
        "population": 4.00001
      },
      {
        "charge": 1e-05,
        "element": "Si",
        "kind": 1,
        "population": 3.99999
      },
      {
        "charge": 6e-06,
        "element": "Si",
        "kind": 1,
        "population": 3.999994
      },
      {
        "charge": 3.5e-05,
        "element": "Si",
        "kind": 1,
        "population": 3.999965
      },
      {
        "charge": 3.3e-05,
        "element": "Si",
        "kind": 1,
        "population": 3.999967
      },
      {
        "charge": 9e-06,
        "element": "Si",
        "kind": 1,
        "population": 3.999991
      },
      {
        "charge": 3.3e-05,
        "element": "Si",
        "kind": 1,
        "population": 3.999967
      },
      {
        "charge": 9e-06,
        "element": "Si",
        "kind": 1,
        "population": 3.999991
      },
      {
        "charge": 3e-06,
        "element": "Si",
        "kind": 1,
        "population": 3.999997
      },
      {
        "charge": -0.000312,
        "element": "Si",
        "kind": 1,
        "population": 4.000312
      },
      {
        "charge": 3e-06,
        "element": "Si",
        "kind": 1,
        "population": 3.999997
      },
      {
        "charge": -0.000311,
        "element": "Si",
        "kind": 1,
        "population": 4.000311
      },
      {
        "charge": 3.4e-05,
        "element": "Si",
        "kind": 1,
        "population": 3.999966
      },
      {
        "charge": 1e-05,
        "element": "Si",
        "kind": 1,
        "population": 3.99999
      },
      {
        "charge": 3.4e-05,
        "element": "Si",
        "kind": 1,
        "population": 3.999966
      },
      {
        "charge": 1e-05,
        "element": "Si",
        "kind": 1,
        "population": 3.99999
      },
      {
        "charge": 6e-06,
        "element": "Si",
        "kind": 1,
        "population": 3.999994
      },
      {
        "charge": 3.5e-05,
        "element": "Si",
        "kind": 1,
        "population": 3.999965
      },
      {
        "charge": -9e-06,
        "element": "Si",
        "kind": 1,
        "population": 4.000009
      },
      {
        "charge": -3.3e-05,
        "element": "Si",
        "kind": 1,
        "population": 4.000033
      },
      {
        "charge": 0.000308,
        "element": "Si",
        "kind": 1,
        "population": 3.999692
      },
      {
        "charge": -4e-06,
        "element": "Si",
        "kind": 1,
        "population": 4.000004
      },
      {
        "charge": -3.6e-05,
        "element": "Si",
        "kind": 1,
        "population": 4.000036
      },
      {
        "charge": -7e-06,
        "element": "Si",
        "kind": 1,
        "population": 4.000007
      },
      {
        "charge": -9e-06,
        "element": "Si",
        "kind": 1,
        "population": 4.000009
      },
      {
        "charge": -3.3e-05,
        "element": "Si",
        "kind": 1,
        "population": 4.000033
      },
      {
        "charge": -8e-06,
        "element": "Si",
        "kind": 1,
        "population": 4.000008
      },
      {
        "charge": -3.3e-05,
        "element": "Si",
        "kind": 1,
        "population": 4.000033
      },
      {
        "charge": -3.5e-05,
        "element": "Si",
        "kind": 1,
        "population": 4.000035
      },
      {
        "charge": -6e-06,
        "element": "Si",
        "kind": 1,
        "population": 4.000006
      },
      {
        "charge": 0.000308,
        "element": "Si",
        "kind": 1,
        "population": 3.999692
      },
      {
        "charge": -4e-06,
        "element": "Si",
        "kind": 1,
        "population": 4.000004
      },
      {
        "charge": -8e-06,
        "element": "Si",
        "kind": 1,
        "population": 4.000008
      },
      {
        "charge": -3.3e-05,
        "element": "Si",
        "kind": 1,
        "population": 4.000033
      }
    ],
    "total": {
      "charge": 0.0,
      "population": 256.0
    }
  },
  "program info": {
    "ended at": "2019-09-17 17:02:35.738",
    "process id": "23773",
    "ran by": "tiziano",
    "ran on": "tcpc18",
    "started at": "2019-09-17 17:01:19.273",
    "started by": "tiziano",
    "started in": "/users/tiziano/work/phonopy/example/Si-CP2K",
    "started on": "tcpc18",
    "stopped in": "/users/tiziano/work/phonopy/example/Si-CP2K"
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

## Usage: xyz_restart_cleaner

```console
$ xyz_restart_cleaner orig_trajectory.xyz new_trajectory.xyz
found restart point @1, dropping 1 frames, flushing 1
flushing remaining 2 frames
```

## Usage: cp2k_bs2csv

Given a `.bs` file as written by CP2K the script will generate CSV files with the same name and suffixes `.set-X.csv` in the same directory as the source file:

```console
$ cp2k_bs2csv WO3.bs
writing point set WO3.bs.set-1.csv (total number of k-points: 11)
with the following special points:
     GAMMA: 0.00000000 / 0.00000000 / 0.00000000
         X: 0.00000000 / 0.50000000 / 0.00000000
writing point set WO3.bs.set-2.csv (total number of k-points: 11)
with the following special points:
         X: 0.00000000 / 0.50000000 / 0.00000000
         M: 0.50000000 / 0.50000000 / 0.00000000
writing point set WO3.bsset-3.csv (total number of k-points: 11)
with the following special points:
         M: 0.50000000 / 0.50000000 / 0.00000000
     GAMMA: 0.00000000 / 0.00000000 / 0.00000000
writing point set WO3.bs.set-4.csv (total number of k-points: 11)
with the following special points:
     GAMMA: 0.00000000 / 0.00000000 / 0.00000000
         R: 0.50000000 / 0.50000000 / 0.50000000
writing point set WO3.bs.set-5.csv (total number of k-points: 11)
with the following special points:
         R: 0.50000000 / 0.50000000 / 0.50000000
         X: 0.00000000 / 0.50000000 / 0.00000000
writing point set WO3.bs.set-6.csv (total number of k-points: 11)
with the following special points:
         R: 0.50000000 / 0.50000000 / 0.50000000
         M: 0.50000000 / 0.50000000 / 0.00000000
$ ls
WO3.cp2k-8.bs            WO3.cp2k-8.bs.set-2.csv  WO3.cp2k-8.bs.set-4.csv  WO3.cp2k-8.bs.set-6.csv
WO3.cp2k-8.bs.set-1.csv  WO3.cp2k-8.bs.set-3.csv  WO3.cp2k-8.bs.set-5.csv
```

## Development

```console
$ poetry install
$ poetry run pytest -v
```
