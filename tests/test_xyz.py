from . import TEST_DIR


from cp2k_output_tools.trajectories import xyz


def test_parse():
    with (TEST_DIR / "outputs" / "minimal.xyz").open("rb") as fhandle:
        data = xyz.parse(fhandle)

    assert len(data) == 3


def test_parse_from_textfile():
    with (TEST_DIR / "outputs" / "minimal.xyz").open("r") as fhandle:
        data = xyz.parse(fhandle)

    assert len(data) == 3


def test_parse_from_str():
    with (TEST_DIR / "outputs" / "minimal.xyz").open("r") as fhandle:
        data = xyz.parse(fhandle.read())

    assert len(data) == 3


def test_parse_from_bytes():
    with (TEST_DIR / "outputs" / "minimal.xyz").open("rb") as fhandle:
        data = xyz.parse(fhandle.read())

    assert len(data) == 3
