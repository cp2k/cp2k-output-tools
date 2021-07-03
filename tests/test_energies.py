from . import TEST_DIR

from cp2k_output_tools.parser import parse_iter
from cp2k_output_tools.blocks import match_energies


def test_energies():
    with open(TEST_DIR.joinpath("outputs/Si.out"), "r") as fhandle:
        result = next(parse_iter(fhandle.read(), matchers=[match_energies]))

        assert result
        assert result.data == {"energies": {"total force_eval": -251.687390311050706}}
