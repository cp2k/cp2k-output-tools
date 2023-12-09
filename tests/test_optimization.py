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
                "force_eval_energy": -1.16096052,
                "inner_scf": {
                    "nsteps": 8,
                    "overlap_core_energy": 6.0512959e-07,
                    "self_core_energy": -2.82094792,
                    "core_hamiltonian_energy": 1.07883184,
                    "hartree_energy": 1.30392538,
                    "xc_energy": -0.72277042,
                    "total_energy": -1.16096052,
                    "electronic_entropic_energy": None,
                    "fermi_energy": None,
                    "dispersion_energy": None,
                },
            },
            {
                "nspin": 1,
                "nelec": 2,
                "num_occ_orb": 1,
                "num_mol_orb": 1,
                "num_orb_func": 10,
                "force_eval_energy": -1.16118019,
                "inner_scf": {
                    "nsteps": 4,
                    "overlap_core_energy": 0.0000012,
                    "self_core_energy": -2.82094792,
                    "core_hamiltonian_energy": 1.08370608,
                    "hartree_energy": 1.30183473,
                    "xc_energy": -0.72577425,
                    "total_energy": -1.16118019,
                    "electronic_entropic_energy": None,
                    "fermi_energy": None,
                    "dispersion_energy": None,
                },
            },
            {
                "nspin": 1,
                "nelec": 2,
                "num_occ_orb": 1,
                "num_mol_orb": 1,
                "num_orb_func": 10,
                "force_eval_energy": -1.16118537,
                "inner_scf": {
                    "nsteps": 4,
                    "overlap_core_energy": 1.07320985e-06,
                    "self_core_energy": -2.82094792,
                    "core_hamiltonian_energy": 1.08302262,
                    "hartree_energy": 1.30210002,
                    "xc_energy": -0.72536117,
                    "total_energy": -1.16118537,
                    "electronic_entropic_energy": None,
                    "fermi_energy": None,
                    "dispersion_energy": None,
                },
            },
            {
                "nspin": 1,
                "nelec": 2,
                "num_occ_orb": 1,
                "num_mol_orb": 1,
                "num_orb_func": 10,
                "force_eval_energy": -1.16118537,
                "inner_scf": {
                    "nsteps": 4,
                    "overlap_core_energy": 1.07320985e-06,
                    "self_core_energy": -2.82094792,
                    "core_hamiltonian_energy": 1.08302280,
                    "hartree_energy": 1.30210002,
                    "xc_energy": -0.72536117,
                    "total_energy": -1.16118537,
                    "electronic_entropic_energy": None,
                    "fermi_energy": None,
                    "dispersion_energy": None,
                },
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
                "force_eval_energy": -65.98706397,
                "inner_scf": {
                    "nsteps": 10,
                    "overlap_core_energy": 0.0,
                    "self_core_energy": -138.89582544,
                    "core_hamiltonian_energy": 27.22305865,
                    "hartree_energy": 56.70225641,
                    "xc_energy": -11.01655328,
                    "total_energy": -65.98706366,
                    "electronic_entropic_energy": None,
                    "fermi_energy": None,
                    "dispersion_energy": None,
                },
            },
            {
                "nspin": 1,
                "nelec": 32,
                "num_occ_orb": 16,
                "num_mol_orb": 16,
                "num_orb_func": 55,
                "force_eval_energy": -65.98706506,
                "inner_scf": {
                    "nsteps": 9,
                    "overlap_core_energy": 0.0,
                    "self_core_energy": -138.89582544,
                    "core_hamiltonian_energy": 27.22275912,
                    "hartree_energy": 56.70220023,
                    "xc_energy": -11.01647284,
                    "total_energy": -65.98733894,
                    "electronic_entropic_energy": None,
                    "fermi_energy": None,
                    "dispersion_energy": None,
                },
            },
            {
                "nspin": 1,
                "nelec": 32,
                "num_occ_orb": 16,
                "num_mol_orb": 16,
                "num_orb_func": 55,
                "force_eval_energy": -65.98710767,
                "inner_scf": {
                    "nsteps": 5,
                    "overlap_core_energy": 0.0,
                    "self_core_energy": -138.89582544,
                    "core_hamiltonian_energy": 27.20749466,
                    "hartree_energy": 56.71104696,
                    "xc_energy": -11.00902476,
                    "total_energy": -65.98630859,
                    "electronic_entropic_energy": None,
                    "fermi_energy": None,
                    "dispersion_energy": None,
                },
            },
            {
                "nspin": 1,
                "nelec": 32,
                "num_occ_orb": 16,
                "num_mol_orb": 16,
                "num_orb_func": 55,
                "force_eval_energy": -65.98710770,
                "inner_scf": {
                    "nsteps": 4,
                    "overlap_core_energy": 0.0,
                    "self_core_energy": -138.89582544,
                    "core_hamiltonian_energy": 27.20670707,
                    "hartree_energy": 56.71083178,
                    "xc_energy": -11.00884866,
                    "total_energy": -65.98713525,
                    "electronic_entropic_energy": None,
                    "fermi_energy": None,
                    "dispersion_energy": None,
                },
            },
            {
                "nspin": 1,
                "nelec": 32,
                "num_occ_orb": 16,
                "num_mol_orb": 16,
                "num_orb_func": 55,
                "force_eval_energy": -65.98710770,
                "inner_scf": {
                    "nsteps": 1,
                    "overlap_core_energy": 0.0,
                    "self_core_energy": -138.89582544,
                    "core_hamiltonian_energy": 27.20676302,
                    "hartree_energy": 56.71080149,
                    "xc_energy": -11.00884677,
                    "total_energy": -65.98710770,
                    "electronic_entropic_energy": None,
                    "fermi_energy": None,
                    "dispersion_energy": None,
                },
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
        inner_scf_ref = opt_ref.pop("inner_scf")
        inner_scf = step_scf.sublevels[0]
        for keyw, val in inner_scf_ref.items():
            if val is None:
                assert getattr(inner_scf, keyw) is None
            elif isinstance(val, float):
                assert abs(float(getattr(inner_scf, keyw).magnitude) - val) < 1.0e-7
            else:
                assert getattr(inner_scf, keyw) == val
        assert abs(float(step_scf.force_eval_energy.magnitude) - opt_ref.pop("force_eval_energy")) < 1.0e-7
        for keyw, val in opt_ref.items():
            assert getattr(step_scf, keyw) == val
    if opt_type == "cell":
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
