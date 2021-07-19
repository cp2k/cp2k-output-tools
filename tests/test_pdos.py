import pytest

from . import TEST_DIR


@pytest.mark.script_launch_mode("subprocess")
def test_pdos(script_runner):
    ret = script_runner.run("cp2k_pdos", str(TEST_DIR / "outputs" / "graphene-k1-1.pdos"))

    assert ret.success
    assert "Nr of lines:                  936" in ret.stderr
    assert "Energy_[eV]" in ret.stdout


@pytest.mark.script_launch_mode("subprocess")
def test_pdos_list_of_atoms(script_runner):

    ret = script_runner.run("cp2k_pdos", str(TEST_DIR / "outputs" / "list-of-atoms.pdos"))

    assert ret.success
    assert "Nr of lines:                 6142" in ret.stderr
    assert "Energy_[eV]" in ret.stdout
