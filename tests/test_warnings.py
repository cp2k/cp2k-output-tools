import gzip

from cp2k_output_tools.blocks import match_warnings
from cp2k_output_tools.parser import parse_iter

from . import TEST_DIR


def test_warnings():
    with TEST_DIR.joinpath("outputs/warning-snippet.out").open("r") as fhandle:
        result = next(parse_iter(fhandle.read(), matchers=[match_warnings]))

        assert result
        assert result == {
            "nwarnings": 2,
            "warnings": [
                {
                    "filename": "qs_scf_post_gpw.F",
                    "line": 2162,
                    "message": "Spin contamination estimate not implemented for k-points.",
                }
            ],
        }


def test_sirius_warnings():
    with gzip.open(TEST_DIR.joinpath("outputs/cp2k_sirius_interstitial_warning.out.gz"), "rt") as fhandle:
        result = next(parse_iter(fhandle.read(), matchers=[match_warnings]))

        assert result
        assert result["nwarnings"] == 196
        assert result["warnings"][0] == {
            "filename": (
                "/scratch/e1000/timuel/spack-stage/spack-stage-sirius-develop-aqhmg7a7ibklk6kz6ebfnpcsxhe43s6y"
                "/spack-src/src/context/simulation_parameters.cpp"
            ),
            "line": 104,
            "message": "The following configuration parameters were not recognized and ignored: potential_tol",
        }

        assert result["warnings"][1] == {
            "filename": (
                "/scratch/e1000/timuel/spack-stage/spack-stage-sirius-develop-aqhmg7a7ibklk6kz6ebfnpcsxhe43s6y"
                "/spack-src/src/density/density.hpp"
            ),
            "line": 989,
            "message": "Interstitial charge density has negative values",
            "details": ["most negatve value : -0.000674155"],
        }


def test_sirius_error():
    with gzip.open(TEST_DIR.joinpath("outputs/cp2k_sirius_fatal_error.out.gz"), "rt") as fhandle:
        result = next(parse_iter(fhandle.read(), matchers=[match_warnings]))

        assert result

        assert result["nwarnings"] == 17
        assert result["warnings"][0] == {
            "filename": (
                "/scratch/e1000/timuel/spack-stage/spack-stage-sirius-develop-aqhmg7a7ibklk6kz6ebfnpcsxhe43s6y"
                "/spack-src/src/context/simulation_parameters.cpp"
            ),
            "line": 104,
            "message": "The following configuration parameters were not recognized and ignored: potential_tol",
        }

        assert "error" in result

        assert result["error"] == {
            "filename": (
                "/scratch/e1000/timuel/spack-stage/spack-stage-sirius-develop-aqhmg7a7ibklk6kz6ebfnpcsxhe43s6y"
                "/spack-src/src/SDDK/wf_ortho.cpp"
            ),
            "line": 186,
            "message": "error in factorization, info = 44",
            "details": [
                "number of existing states: 55",
                "number of new states: 55",
                "number of wave_functions: 3",
                "idx_bra: 0 idx_ket:2",
            ],
        }
