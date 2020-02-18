from . import TEST_DIR

from cp2k_output_tools.parser import parse_iter
from cp2k_output_tools.blocks import match_mulliken_population_analysis


def test_mulliken_unrestricted():
    with open(TEST_DIR.joinpath("inputs/mulliken_unrestricted_snippet.out"), "r") as fhandle:
        results = list(parse_iter(fhandle.read(), matchers=[match_mulliken_population_analysis]))

        assert results
        assert results[0] == {
            "mulliken_population_analysis": {
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
        }


def test_mulliken_restricted():
    with open(TEST_DIR.joinpath("inputs/mulliken_restricted_snippet.out"), "r") as fhandle:
        results = list(parse_iter(fhandle.read(), matchers=[match_mulliken_population_analysis]))

        assert results
        assert results[0] == {
            "mulliken_population_analysis": {
                "per-atom": [
                    {"element": "Si", "kind": 1, "population": 3.999993, "charge": 7e-06},
                    {"element": "Si", "kind": 1, "population": 4.0, "charge": 0.0},
                    {"element": "Si", "kind": 1, "population": 4.0, "charge": -0.0},
                    {"element": "Si", "kind": 1, "population": 4.000001, "charge": -1e-06},
                    {"element": "Si", "kind": 1, "population": 4.0, "charge": -0.0},
                    {"element": "Si", "kind": 1, "population": 4.000001, "charge": -1e-06},
                    {"element": "Si", "kind": 1, "population": 4.000001, "charge": -1e-06},
                    {"element": "Si", "kind": 1, "population": 4.0, "charge": -0.0},
                    {"element": "Si", "kind": 1, "population": 3.999863, "charge": 0.000137},
                    {"element": "Si", "kind": 1, "population": 4.00002, "charge": -2e-05},
                    {"element": "Si", "kind": 1, "population": 4.000133, "charge": -0.000133},
                    {"element": "Si", "kind": 1, "population": 3.999979, "charge": 2.1e-05},
                    {"element": "Si", "kind": 1, "population": 4.000133, "charge": -0.000133},
                    {"element": "Si", "kind": 1, "population": 3.999979, "charge": 2.1e-05},
                    {"element": "Si", "kind": 1, "population": 3.999863, "charge": 0.000137},
                    {"element": "Si", "kind": 1, "population": 4.00002, "charge": -2e-05},
                    {"element": "Si", "kind": 1, "population": 4.000039, "charge": -3.9e-05},
                    {"element": "Si", "kind": 1, "population": 3.999964, "charge": 3.6e-05},
                    {"element": "Si", "kind": 1, "population": 4.00001, "charge": -1e-05},
                    {"element": "Si", "kind": 1, "population": 3.99999, "charge": 1e-05},
                    {"element": "Si", "kind": 1, "population": 4.000039, "charge": -3.9e-05},
                    {"element": "Si", "kind": 1, "population": 3.999964, "charge": 3.6e-05},
                    {"element": "Si", "kind": 1, "population": 4.00001, "charge": -1e-05},
                    {"element": "Si", "kind": 1, "population": 3.99999, "charge": 1e-05},
                    {"element": "Si", "kind": 1, "population": 4.000039, "charge": -3.9e-05},
                    {"element": "Si", "kind": 1, "population": 3.999964, "charge": 3.6e-05},
                    {"element": "Si", "kind": 1, "population": 4.000039, "charge": -3.9e-05},
                    {"element": "Si", "kind": 1, "population": 3.999964, "charge": 3.6e-05},
                    {"element": "Si", "kind": 1, "population": 4.00001, "charge": -1e-05},
                    {"element": "Si", "kind": 1, "population": 3.99999, "charge": 1e-05},
                    {"element": "Si", "kind": 1, "population": 4.00001, "charge": -1e-05},
                    {"element": "Si", "kind": 1, "population": 3.99999, "charge": 1e-05},
                    {"element": "Si", "kind": 1, "population": 3.999994, "charge": 6e-06},
                    {"element": "Si", "kind": 1, "population": 3.999965, "charge": 3.5e-05},
                    {"element": "Si", "kind": 1, "population": 3.999967, "charge": 3.3e-05},
                    {"element": "Si", "kind": 1, "population": 3.999991, "charge": 9e-06},
                    {"element": "Si", "kind": 1, "population": 3.999967, "charge": 3.3e-05},
                    {"element": "Si", "kind": 1, "population": 3.999991, "charge": 9e-06},
                    {"element": "Si", "kind": 1, "population": 3.999997, "charge": 3e-06},
                    {"element": "Si", "kind": 1, "population": 4.000312, "charge": -0.000312},
                    {"element": "Si", "kind": 1, "population": 3.999997, "charge": 3e-06},
                    {"element": "Si", "kind": 1, "population": 4.000311, "charge": -0.000311},
                    {"element": "Si", "kind": 1, "population": 3.999966, "charge": 3.4e-05},
                    {"element": "Si", "kind": 1, "population": 3.99999, "charge": 1e-05},
                    {"element": "Si", "kind": 1, "population": 3.999966, "charge": 3.4e-05},
                    {"element": "Si", "kind": 1, "population": 3.99999, "charge": 1e-05},
                    {"element": "Si", "kind": 1, "population": 3.999994, "charge": 6e-06},
                    {"element": "Si", "kind": 1, "population": 3.999965, "charge": 3.5e-05},
                    {"element": "Si", "kind": 1, "population": 4.000009, "charge": -9e-06},
                    {"element": "Si", "kind": 1, "population": 4.000033, "charge": -3.3e-05},
                    {"element": "Si", "kind": 1, "population": 3.999692, "charge": 0.000308},
                    {"element": "Si", "kind": 1, "population": 4.000004, "charge": -4e-06},
                    {"element": "Si", "kind": 1, "population": 4.000036, "charge": -3.6e-05},
                    {"element": "Si", "kind": 1, "population": 4.000007, "charge": -7e-06},
                    {"element": "Si", "kind": 1, "population": 4.000009, "charge": -9e-06},
                    {"element": "Si", "kind": 1, "population": 4.000033, "charge": -3.3e-05},
                    {"element": "Si", "kind": 1, "population": 4.000008, "charge": -8e-06},
                    {"element": "Si", "kind": 1, "population": 4.000033, "charge": -3.3e-05},
                    {"element": "Si", "kind": 1, "population": 4.000035, "charge": -3.5e-05},
                    {"element": "Si", "kind": 1, "population": 4.000006, "charge": -6e-06},
                    {"element": "Si", "kind": 1, "population": 3.999692, "charge": 0.000308},
                    {"element": "Si", "kind": 1, "population": 4.000004, "charge": -4e-06},
                    {"element": "Si", "kind": 1, "population": 4.000008, "charge": -8e-06},
                    {"element": "Si", "kind": 1, "population": 4.000033, "charge": -3.3e-05},
                ],
                "total": {"population": 256.0, "charge": 0.0},
            }
        }
