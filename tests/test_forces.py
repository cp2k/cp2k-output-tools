from cp2k_output_tools.blocks import match_forces
from cp2k_output_tools.parser import parse_iter

from . import TEST_DIR


def test_energies():
    with TEST_DIR.joinpath("outputs/Si_bulk8.out").open() as fhandle:
        result = next(parse_iter(fhandle.read(), matchers=[match_forces]))

        assert result
        assert result.data == {
            "forces": {
                "atomic": {
                    "per_atom": [
                        {"atom": 1, "element": "Si", "kind": 1, "x": 0.0, "y": 0.0, "z": 0.0},
                        {"atom": 2, "element": "Si", "kind": 1, "x": 0.0, "y": 1e-08, "z": 1e-08},
                        {"atom": 3, "element": "Si", "kind": 1, "x": 1e-08, "y": 1e-08, "z": 0.0},
                        {"atom": 4, "element": "Si", "kind": 1, "x": 1e-08, "y": 0.0, "z": 1e-08},
                        {"atom": 5, "element": "Si", "kind": 1, "x": -1e-08, "y": -1e-08, "z": -1e-08},
                        {"atom": 6, "element": "Si", "kind": 1, "x": -1e-08, "y": -1e-08, "z": -1e-08},
                        {"atom": 7, "element": "Si", "kind": 1, "x": -1e-08, "y": -1e-08, "z": -1e-08},
                        {"atom": 8, "element": "Si", "kind": 1, "x": -1e-08, "y": -1e-08, "z": -1e-08},
                    ],
                    "sum": {"norm": 0.0, "x": -0.0, "y": -0.0, "z": -0.0},
                    "unit": "a.u.",
                }
            }
        }
