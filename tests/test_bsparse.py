from cp2k_output_tools.bandstructure_parser import (
    BandstructureSet,
    SpecialPoint,
    parse_bandstructure,
)

from . import TEST_DIR


def test_bsparse():
    with TEST_DIR.joinpath("outputs/WO3.cp2k-8.bs").open() as fhandle:
        first_set = next(parse_bandstructure(fhandle.read()))

    assert isinstance(first_set, BandstructureSet)
    assert first_set.npoints == 11
    assert first_set.nbands == 20
    assert first_set.specialpoints == [
        SpecialPoint(1, "GAMMA", 0, 0, 0),
        SpecialPoint(2, "X", 0, 0.5, 0),
    ]
    assert len(first_set.points) == first_set.npoints
    assert first_set.points[0].a == 0
    assert first_set.points[0].b == 0
    assert first_set.points[0].c == 0
    assert all(len(p.bands) == first_set.nbands for p in first_set.points)
