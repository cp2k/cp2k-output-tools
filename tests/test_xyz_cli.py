import pytest

from . import TEST_DIR


@pytest.mark.script_launch_mode("subprocess")
def test_one_restart(script_runner):
    ret = script_runner.run("xyz_restart_cleaner", str(TEST_DIR / "inputs" / "one_restart.xyz"))

    assert ret.success
    assert "found restart point @1, dropping 1 frames, flushing 1" in ret.stderr
    assert "i = 0, time = 0, E = 0" in ret.stdout


@pytest.mark.script_launch_mode("subprocess")
def test_restart_before_first(script_runner):
    ret = script_runner.run("xyz_restart_cleaner", str(TEST_DIR / "inputs" / "restart_before_first.xyz"))

    assert ret.success
    assert (
        "WARNING: restart point may lie before already flushed frames, please run this again on the generated output" in ret.stderr
    )
    assert "i = 1, time = 2, E = -1" in ret.stdout
