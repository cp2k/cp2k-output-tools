from . import TEST_DIR
from cp2k_output_tools.parser import parse_iter


def test_mulliken_unrestricted():
    with open(TEST_DIR.joinpath("inputs/mulliken_unrestricted_snippet.out"), "r") as fhandle:
        results = list(parse_iter(fhandle.read(), matchers=["mulliken_population_analysis"]))

        assert results

        name, result = results[0]
        assert name == "mulliken_population_analysis"
        assert result == {
            "per-atom": [
                {
                    "element": "Co",
                    "kind": 1,
                    "population_alpha": 9.332183,
                    "population_beta": 7.66782,
                    "charge": -2e-06,
                    "spin": 1.664363,
                },
                {
                    "element": "Co",
                    "kind": 1,
                    "population_alpha": 9.332177,
                    "population_beta": 7.66782,
                    "charge": 2e-06,
                    "spin": 1.664357,
                },
            ],
            "total": {"population_alpha": 18.66436, "population_beta": 15.33564, "charge": -0.0, "spin": 3.32872},
        }
