import pytest

from . import TEST_DIR


@pytest.mark.script_launch_mode("subprocess")
def test_bs2csv(script_runner):
    ret = script_runner.run("cp2k_bs2csv", str(TEST_DIR / "inputs" / "WO3.cp2k-7.bs"))

    assert ret.success
    assert "total number of k-points: 11" in ret.stdout
    assert "GAMMA: 0.00000000/0.00000000/0.00000000" in ret.stdout
