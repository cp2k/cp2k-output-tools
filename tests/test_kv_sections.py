from . import TEST_DIR

from cp2k_output_tools.parser import parse_iter
from cp2k_output_tools.blocks import match_kv_sections


def test_kv_sections():
    with open(TEST_DIR.joinpath("inputs/Si.out"), "r") as fhandle:
        result = next(parse_iter(fhandle.read(), matchers=[match_kv_sections]))

        assert result
        assert result == {
            "dbcsr": {
                "cpu multiplication driver": "XSMM",
                "multrec recursion limit": "512",
                "multiplication stack size": "1000",
                "maximum elements for images": "UNLIMITED",
                "multiplicative factor virtual images": "1",
                "use multiplication densification": "T",
                "multiplication size stacks": "3",
            },
            "cp2k": {
                "version string": "CP2K version 7.0 (Development Version)",
                "source code revision number": "git:43f50e2",
                "cp2kflags: libint fftw3 libxc xsmm spglib": " ",
                "is freely available from": "https://www.cp2k.org/",
                "program compiled at": "Mon Sep 16 14:42:43 CEST 2019",
                "program compiled on": "tcpc18",
                "program compiled for": "local",
                "data directory path": "/data/tiziano/cp2k/data",
                "input file name": "Si-supercell-001.inp",
            },
            "global": {
                "force environment number": "1",
                "basis set file name": "BASIS_MOLOPT",
                "potential file name": "POTENTIAL",
                "mm potential file name": "MM_POTENTIAL",
                "coordinate file name": "__STD_INPUT__",
                "method name": "CP2K",
                "project name": "Si-supercell-001",
                "preferred fft library": "FFTW3",
                "preferred diagonalization lib.": "SL",
                "run type": "ENERGY_FORCE",
                "all-to-all communication in single precision": "F",
                "ffts using library dependent lengths": "F",
                "global print level": "MEDIUM",
                "mpi i/o enabled": "T",
                "total number of message passing processes": "1",
                "number of threads for this process": "1",
                "this output is from process": "0",
                "cpu model name": "Intel(R) Core(TM) i7-4790 CPU @ 3.60GHz",
                "cpuid": "1002",
            },
        }
