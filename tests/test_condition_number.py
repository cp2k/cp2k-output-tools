from . import TEST_DIR
from cp2k_output_tools.parser import parse_iter


def test_condition_number():
    with open(TEST_DIR.joinpath("inputs/overlap_condition_snippet.out"), "r") as fhandle:
        results = list(parse_iter(fhandle.read(), matchers=["overlap_condition_number"]))

        assert results
        name, result = results[0]
        assert name == "overlap_condition_number"
        assert result == {
            "1-norm (estimate)": {"|A|": 15.13, "|A^-1|": 7525.0, "CN": 113900.0, "Log(CN)": 5.0563},
            "1-norm (using diagonalization)": {"|A|": 15.13, "|A^-1|": 22980.0, "CN": 347700.0, "Log(CN)": 5.5412},
            "2-norm (using diagonalization)": {"max EV": 10.81, "min EV": 0.0001036, "CN": 104400.0, "Log(CN)": 5.0187},
        }
