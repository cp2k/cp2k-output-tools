import json
import pytest

from . import TEST_DIR


def test_cp2kparse_key(script_runner):
    ret = script_runner.run("cp2kparse", "-k", "energies/total force_eval", str(TEST_DIR.joinpath("outputs/Si.out")))

    assert ret.success
    assert ret.stderr == ""
    assert ret.stdout == "energies/total force_eval: -251.6873903110507\n"


def test_cp2kparse_key_safe(script_runner):
    ret = script_runner.run("cp2kparse", "-k", "energies/total force_eval", "-s", str(TEST_DIR.joinpath("outputs/Si.out")))

    assert not ret.success
    assert "KeyError" in ret.stderr

    ret = script_runner.run("cp2kparse", "-k", "energies/total_force_eval", "-s", str(TEST_DIR.joinpath("outputs/Si.out")))

    assert ret.success
    assert ret.stderr == ""
    assert ret.stdout == "energies/total_force_eval: -251.6873903110507\n"


def test_cp2kparse_mulliken(script_runner):
    ret = script_runner.run("cp2kparse", str(TEST_DIR.joinpath("outputs/mulliken_unrestricted_snippet.out")))

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


def test_cp2kparse_mulliken_yaml(script_runner):
    ryaml = pytest.importorskip("ruamel.yaml")
    yaml = ryaml.YAML()

    ret = script_runner.run("cp2kparse", "-y", str(TEST_DIR.joinpath("outputs/mulliken_unrestricted_snippet.out")))

    assert ret.success
    assert ret.stderr == ""

    tree = yaml.load(ret.stdout)

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
