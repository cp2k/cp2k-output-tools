import json

import pytest

from cp2k_output_tools.blocks import match_moments
from cp2k_output_tools.parser import parse_iter

from . import TEST_DIR


def test_compact_moments():
    content = (TEST_DIR / "outputs/moments_trajectory.dat").read_text()
    block = match_moments(content)
    moments = next(parse_iter(content, matchers=[match_moments]))["moments"]

    assert moments["unit"] == "Debye"
    assert [record["iteration"] for record in moments["primary"]] == ["1_1", "1_1", "1_2"]
    assert moments["primary"][0] == {
        "iteration": "1_1",
        "dipole": {"x": 1.0, "y": 2.0, "z": 2.0, "norm": 3.0},
        "cell": None,
    }
    assert moments["primary"][1]["cell"] == [[10, 1, 2], [3, 20, 4], [5, 6, 30]]
    assert moments["primary"][2]["cell"] == [[11, 1, 2], [3, 21, 4], [5, 6, 31]]
    assert [record["iteration"] for record in moments["reference 2"]] == ["1_1", "1_2"]
    assert moments["reference 2"][1]["dipole"]["x"] == -2.0
    assert moments["reference 2"][1]["cell"] == moments["primary"][2]["cell"]
    assert len(block.spans) == 5
    assert all(content[start:end].lstrip().startswith("MOMENTS") for start, end in block.spans)
    assert match_moments("# MOMENTS| iter_level dipole_x dipole_y dipole_z dipole_norm [Debye]\n") is None


@pytest.mark.parametrize("record", ["1 1 2 3", "1 1 2 2 3 10", "1 1 bad 2 3", "1 1 nan 2 3"])
def test_invalid_compact_moments(record):
    with pytest.raises(ValueError, match=r"Invalid MOMENTS\| record on line 2"):
        match_moments(f"# header\n MOMENTS| {record}\n")


def test_compact_moments_cli(script_runner):
    ret = script_runner.run(["cp2kparse", "-s", str(TEST_DIR / "outputs/moments_trajectory.dat")])
    assert ret.success
    moments = json.loads(ret.stdout)["moments"]
    assert len(moments["primary"]) == 3
    assert len(moments["reference_2"]) == 2
