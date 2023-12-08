import pytest

from cp2k_output_tools.levelparser import parse_all

from . import TEST_DIR

REF_VALUES = {
    "geo": {
        "opt": [
            {
                "nspin": 1,
                "nelec": 2,
                "num_occ_orb": 1,
                "num_mol_orb": 1,
                "num_orb_func": 10,
                "nsteps": 8,
                "force_eval_energy": -1.16096052,
            },
            {
                "nspin": 1,
                "nelec": 2,
                "num_occ_orb": 1,
                "num_mol_orb": 1,
                "num_orb_func": 10,
                "nsteps": 4,
                "force_eval_energy": -1.16118019,
            },
            {
                "nspin": 1,
                "nelec": 2,
                "num_occ_orb": 1,
                "num_mol_orb": 1,
                "num_orb_func": 10,
                "nsteps": 4,
                "force_eval_energy": -1.16118537,
            },
            {
                "nspin": 1,
                "nelec": 2,
                "num_occ_orb": 1,
                "num_mol_orb": 1,
                "num_orb_func": 10,
                "nsteps": 4,
                "force_eval_energy": -1.16118537,
            },
        ],
    },
    "cell": {
        "opt": [
            {
                "nspin": 1,
                "nelec": 32,
                "num_occ_orb": 16,
                "num_mol_orb": 16,
                "num_orb_func": 55,
                "nsteps": 10,
                "force_eval_energy": -65.98706397,
            },
            {
                "nspin": 1,
                "nelec": 32,
                "num_occ_orb": 16,
                "num_mol_orb": 16,
                "num_orb_func": 55,
                "nsteps": 9,
                "force_eval_energy": -65.98706506,
            },
            {
                "nspin": 1,
                "nelec": 32,
                "num_occ_orb": 16,
                "num_mol_orb": 16,
                "num_orb_func": 55,
                "nsteps": 5,
                "force_eval_energy": -65.98710767,
            },
            {
                "nspin": 1,
                "nelec": 32,
                "num_occ_orb": 16,
                "num_mol_orb": 16,
                "num_orb_func": 55,
                "nsteps": 4,
                "force_eval_energy": -65.98710770,
            },
            {
                "nspin": 1,
                "nelec": 32,
                "num_occ_orb": 16,
                "num_mol_orb": 16,
                "num_orb_func": 55,
                "nsteps": 1,
                "force_eval_energy": -65.98710770,
            },
        ],
        "cell_infos": [
            {
                "volume": 204.400073,
                "numerically_orthorombic": False,
                "periodicity": None,
                "vectors": [[6.612, 0.0, 0.0], [3.306, 5.726, 0.000], [3.306, 1.909, 5.399]],
                "vector_norms": [6.611987, 6.611987, 6.611987],
                "angles": [60.0, 60.0, 60.0],
            },
            {
                "volume": 204.433884,
                "numerically_orthorombic": False,
                "periodicity": None,
                "vectors": [[6.612, 0.0, 0.0], [3.306, 5.726, 0.000], [3.306, 1.909, 5.399]],
                "vector_norms": [6.612271, 6.612274, 6.612274],
                "angles": [60.001888, 60.001414, 60.001414],
            },
            {
                "volume": 207.291619,
                "numerically_orthorombic": False,
                "periodicity": None,
                "vectors": [[6.636, 0.0, 0.0], [3.306, 5.754, 0.000], [3.306, 1.909, 5.428]],
                "vector_norms": [6.636193, 6.636448, 6.636460],
                "angles": [60.159492, 60.119661, 60.119604],
            },
            {
                "volume": 207.386966,
                "numerically_orthorombic": False,
                "periodicity": None,
                "vectors": [[6.637, 0.0, 0.0], [3.306, 5.755, 0.000], [3.306, 1.909, 5.429]],
                "vector_norms": [6.637017, 6.637262, 6.637274],
                "angles": [60.164238, 60.123286, 60.123227],
            },
            {
                "volume": 207.386966,
                "numerically_orthorombic": False,
                "periodicity": None,
                "vectors": [[6.637, 0.0, 0.0], [3.306, 5.755, 0.000], [3.306, 1.909, 5.429]],
                "vector_norms": [6.637017, 6.637262, 6.637274],
                "angles": [60.164238, 60.123286, 60.123227],
            },
        ],
    },
}


@pytest.mark.parametrize("opt_type", ["geo", "cell"])
def test_optimization(opt_type):
    with open(TEST_DIR.joinpath(f"outputs/{opt_type}_opt_snippet.out"), "r") as fhandle:
        result = parse_all(fhandle.read())
    ref = REF_VALUES[opt_type]
    assert len(result.levels[0].sublevels[0].sublevels) == len(ref["opt"]) - 1
    opt_steps_scf = [step.sublevels[0] for step in result.levels[0].sublevels[0].sublevels]
    for step_scf, opt_ref in zip(opt_steps_scf + [result.levels[0].sublevels[1]], ref["opt"]):
        assert step_scf.converged
        assert step_scf.sublevels[0].converged
        assert abs(float(step_scf.force_eval_energy.magnitude) - opt_ref.pop("force_eval_energy")) < 1.0e-7
        assert step_scf.sublevels[0].nsteps == opt_ref.pop("nsteps")
        for keyw, val in opt_ref.items():
            assert getattr(step_scf, keyw) == val
    if opt_type == "cell":
        print(result.levels[0].cell_infos)
        assert len(result.levels[0].cell_infos) == len(ref["cell_infos"])
        for info, ref_info in zip(result.levels[0].cell_infos, ref["cell_infos"]):
            assert abs(float(info.volume.magnitude) - ref_info.pop("volume")) < 1.0e-7
            for keyw in ["vector_norms", "angles"]:
                ref0 = ref_info.pop(keyw)
                for i0 in range(3):
                    assert abs(float(getattr(info, keyw)[i0].magnitude) - ref0[i0]) < 1.0e-7
            ref_vectors = ref_info.pop("vectors")
            for i0 in range(3):
                for i1 in range(3):
                    assert abs(float(info.vectors[i0][i1].magnitude) - ref_vectors[i0][i1]) < 1.0e-7
            for keyw, val in ref_info.items():
                assert getattr(info, keyw) == val
