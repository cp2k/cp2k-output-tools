import json

from . import TEST_DIR


def test_cp2kparse_mulliken(script_runner):
    ret = script_runner.run("cp2kparse", str(TEST_DIR.joinpath("inputs/mulliken_unrestricted_snippet.out")))

    assert ret.success
    assert ret.stderr == ""

    tree = json.loads(ret.stdout)

    assert isinstance(tree, dict)
    assert tree == {
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
