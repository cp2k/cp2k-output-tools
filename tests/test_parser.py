from . import TEST_DIR

from cp2k_output_tools.parser import parse_iter


def _key_iter(idict):
    if isinstance(idict, dict):
        for key, value in idict.items():
            yield key
            yield from _key_iter(value)

    elif isinstance(idict, list):
        for item in idict:
            yield from _key_iter(item)


FORBIDDEN_CHARS = " -[](){}/.|^"


def test_parse_safe_keys():
    with open(TEST_DIR.joinpath("outputs/Si.out"), "r") as fhandle:
        for match in parse_iter(fhandle.read(), key_mangling=True):
            assert not any(c in key for c in FORBIDDEN_CHARS for key in _key_iter(match))
