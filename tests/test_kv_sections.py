from . import TEST_DIR

from cp2k_output_tools.parser import parse_iter
from cp2k_output_tools.blocks import match_kv_sections


def test_kv_sections():
    with open(TEST_DIR.joinpath("inputs/Si.out"), "r") as fhandle:
        result = next(parse_iter(fhandle.read(), matchers=[match_kv_sections]))

        assert result
        assert result == {
            "cp2k": {
                "cp2kflags": "libint fftw3 libxc xsmm spglib",
                "data directory path": "/data/tiziano/cp2k/data",
                "input file name": "Si-supercell-001.inp",
                "is freely available from": "https://www.cp2k.org/",
                "program compiled at": "Mon Sep 16 14:42:43 CEST 2019",
                "program compiled for": "local",
                "program compiled on": "tcpc18",
                "source code revision number": "git:43f50e2",
                "version string": "CP2K version 7.0 (Development Version)",
            },
            "dbcsr": {
                "cpu multiplication driver": "XSMM",
                "maximum elements for images": "UNLIMITED",
                "multiplication size stacks": 3,
                "multiplication stack size": 1000,
                "multiplicative factor virtual images": 1,
                "multrec recursion limit": 512,
                "use multiplication densification": True,
            },
            "dft": {
                "charge": 0,
                "cutoffs": {"cutoff_smoothing_range": 0.0, "density": 1e-10, "gradient": 1e-10, "tau": 1e-10},
                "multiplicity": 1,
                "number of spin states": 1,
                "self-interaction correction (sic)": "NO",
                "spin restricted kohn-sham (rks) calculation": "RKS",
                "xc density smoothing": "NONE",
                "xc derivatives": "PW",
            },
            "global": {
                "all-to-all communication in single precision": False,
                "basis set file name": "BASIS_MOLOPT",
                "coordinate file name": "__STD_INPUT__",
                "cpu model name": "Intel(R) Core(TM) i7-4790 CPU @ 3.60GHz",
                "cpuid": 1002,
                "ffts using library dependent lengths": False,
                "force environment number": 1,
                "global print level": "MEDIUM",
                "method name": "CP2K",
                "mm potential file name": "MM_POTENTIAL",
                "mpi i/o enabled": True,
                "number of threads for this process": 1,
                "potential file name": "POTENTIAL",
                "preferred diagonalization lib.": "SL",
                "preferred fft library": "FFTW3",
                "project name": "Si-supercell-001",
                "run type": "ENERGY_FORCE",
                "this output is from process": 0,
                "total number of message passing processes": 1,
            },
            "qs": {
                "density cutoff [a.u.]": 140.0,
                "density plane wave grid type": "NON-SPHERICAL FULLSPACE",
                "grid level progression factor": 3.0,
                "interaction thresholds": {
                    "eps_core_charge": 1e-12,
                    "eps_filter_matrix": 0.0,
                    "eps_gvg_rspace": 1e-05,
                    "eps_ppl": 0.01,
                    "eps_ppnl": 1e-07,
                    "eps_rho_gspace": 1e-10,
                    "eps_rho_rspace": 1e-10,
                    "ps_pgf_orb": 1e-05,
                },
                "method": "GPW",
                "multi grid cutoff [a.u.]": {
                    "1) grid level": 140.0,
                    "2) grid level": 46.7,
                    "3) grid level": 15.6,
                    "4) grid level": 5.2,
                },
                "number of grid levels": 4,
                "relative density cutoff [a.u.]": 20.0,
            },
        }
