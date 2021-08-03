from cp2k_output_tools.blocks import match_kpoints
from cp2k_output_tools.parser import parse_iter

from . import TEST_DIR


def test_kpoints_v5():
    # test file is from aiida-cp2k
    with TEST_DIR.joinpath("outputs/BANDS_output_v5.1.out").open() as fhandle:
        result = next(parse_iter(fhandle.read(), matchers=[match_kpoints]))

    result = result["kpoints"]["bandstructure"]
    assert len(result["sets"]) == 6
    assert all(len(s["specialpoints"]) == 2 for s in result["sets"])
    assert all(s["npoints"] == 11 for s in result["sets"])


def test_kpoints_v8():
    # test file is from aiida-cp2k
    with TEST_DIR.joinpath("outputs/BANDS_output_v8.1.out").open() as fhandle:
        result = next(parse_iter(fhandle.read(), matchers=[match_kpoints]))

    result = result["kpoints"]["bandstructure"]
    assert len(result["sets"]) == 6
    assert all(len(s["specialpoints"]) == 2 for s in result["sets"])
    assert all(s["npoints"] == 11 for s in result["sets"])
