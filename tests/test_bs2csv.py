import pytest

from . import TEST_DIR


@pytest.mark.script_launch_mode("subprocess")
def test_bs2csv_cp2k7_input(script_runner, tmp_path):
    ret = script_runner.run("cp2k_bs2csv", str(TEST_DIR / "outputs" / "WO3.cp2k-7.bs"), cwd=tmp_path)

    assert ret.success
    assert "total number of k-points: 11" in ret.stdout
    assert "GAMMA: 0.00000000 / 0.00000000 / 0.00000000" in ret.stdout


@pytest.mark.script_launch_mode("subprocess")
def test_bs2csv_cp2k8_input(script_runner, tmp_path):
    ret = script_runner.run("cp2k_bs2csv", str(TEST_DIR / "outputs" / "WO3.cp2k-8.bs"), cwd=tmp_path)

    assert ret.success
    assert "total number of k-points: 11" in ret.stdout
    assert "GAMMA: 0.00000000 / 0.00000000 / 0.00000000" in ret.stdout
