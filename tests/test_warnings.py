from . import TEST_DIR

from cp2k_output_tools.parser import parse_iter
from cp2k_output_tools.blocks import match_warnings


def test_warnings():
    with open(TEST_DIR.joinpath("inputs/warning-snippet.out"), "r") as fhandle:
        result = next(parse_iter(fhandle.read(), matchers=[match_warnings]))

        assert result
        assert result == {
            "nwarnings": 2,
            "warnings": [
                {
                    "filename": "qs_scf_post_gpw.F",
                    "line": 2162,
                    "message": "Spin contamination estimate not implemented for k-points.",
                }
            ],
        }
