import json

from . import TEST_DIR


def test_cp2kparse_mulliken(script_runner):
    ret = script_runner.run("cp2kparse", str(TEST_DIR.joinpath("inputs/mulliken_unrestricted_snippet.out")))

    assert ret.success
    assert ret.stderr == ""

    tree = json.loads(ret.stdout)

    assert isinstance(tree, dict)
    assert tree == {
        "warnings": [
            {"filename": "qs_scf_post_gpw.F", "line": 2162, "message": "Spin contamination estimate not implemented for k-points."}
        ],
        "mulliken population analysis": {
            "per atom": [
                {
                    "element": "Co",
                    "kind": 1,
                    "population alpha": 9.332183,
                    "population beta": 7.66782,
                    "charge": -2e-06,
                    "spin": 1.664363,
                },
                {
                    "element": "Co",
                    "kind": 1,
                    "population alpha": 9.332177,
                    "population beta": 7.66782,
                    "charge": 2e-06,
                    "spin": 1.664357,
                },
            ],
            "total": {"population alpha": 18.66436, "population beta": 15.33564, "charge": -0.0, "spin": 3.32872},
        },
    }
