import pytest

from . import TEST_DIR

from cp2k_output_tools.parser import parse_iter
from cp2k_output_tools.blocks import match_program_info


def test_start_and_stop():
    with open(TEST_DIR.joinpath("inputs/Si.out"), "r") as fhandle:
        result = next(parse_iter(fhandle.read(), matchers=[match_program_info]))

        assert result
        print(result)
        assert result == {
            "program info": {
                "started at": "2019-09-17 17:01:19.273",
                "started on": "tcpc18",
                "started by": "tiziano",
                "process id": "23773",
                "started in": "/users/tiziano/work/phonopy/example/Si-CP2K",
                "ended at": "2019-09-17 17:02:35.738",
                "ran on": "tcpc18",
                "ran by": "tiziano",
                "stopped in": "/users/tiziano/work/phonopy/example/Si-CP2K",
            }
        }


def test_no_start_and_stop():
    with open(TEST_DIR.joinpath("inputs/mulliken_restricted_snippet.out"), "r") as fhandle:
        with pytest.raises(StopIteration):
            next(parse_iter(fhandle.read(), matchers=[match_program_info]))


def test_no_stop():
    with open(TEST_DIR.joinpath("inputs/Si-truncated.out"), "r") as fhandle:
        result = next(parse_iter(fhandle.read(), matchers=[match_program_info]))
        assert result
        assert result == {
            "program info": {
                "started at": "2019-09-17 17:01:19.273",
                "started on": "tcpc18",
                "started by": "tiziano",
                "process id": "23773",
                "started in": "/users/tiziano/work/phonopy/example/Si-CP2K",
            }
        }
