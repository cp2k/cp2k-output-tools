from cp2k_output_tools.blocks import match_energies
from cp2k_output_tools.parser import parse_iter

from . import TEST_DIR


def test_energies():
    with open(TEST_DIR.joinpath("outputs/Si.out"), "r") as fhandle:
        result = next(parse_iter(fhandle.read(), matchers=[match_energies]))

        assert result
        assert result == {
            "energies": {
                "core_hamiltonian": 138.60026809219576,
                "electronic_entropic": -1.256404e-08,
                "fermi": 0.20382509931778,
                "hartree": 343.3040142273272,
                "overlap_core": 3.0088e-10,
                "self_core": -656.5115154010256,
                "total": -251.63989121633358,
                "xc": -77.03265812258856,
                "total force_eval": -251.687390311050706,
            }
        }
