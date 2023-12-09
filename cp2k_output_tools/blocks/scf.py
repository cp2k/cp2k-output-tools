import sys
from dataclasses import dataclass
from decimal import Decimal
from typing import List, Optional, Tuple, Union

import regex as re

from . import UREG
from .common import FLOAT, Level
from .energies import FORCE_EVAL_ENERGY_RE, MAIN_ENERGY_RE
from .mulliken import MULLIKEN_POPULATION_ANALYSIS_RE
from .warnings import Message, match_messages

SCF_START_RE = re.compile(
    r"""
^(?:
  (?:\ Spin\ (?P<spin>\d+)\n\n)?
  \ Number\ of\ electrons:\s+ (?P<nelec>\d+)\n
  \ Number\ of\ occupied\ orbitals:\s+  (?P<num_occ_orb>\d+)\n
  \ Number\ of\ molecular\ orbitals:\s+ (?P<num_mol_orb>\d+)\n
  \n
){1,2}
\ Number\ of\ orbital\ functions:\s+ (?P<num_orb_func>\d+)\n
""",
    re.VERBOSE | re.MULTILINE,
)

EIGENVALUES_RE = re.compile(
    rf"""
^(?:
  \s*Eigenvalues\ of\ the\ occupied\ subspace\ spin \s+ (?P<spin>\d) \n
  \ \-+ \n
  (?:\s+(?P<eigenvalue>{FLOAT}))+
  \s+ Fermi\ Energy\ \[eV\]\ : \s+ (?P<fermi_energy>\S+)
)+
""",
    re.VERBOSE | re.MULTILINE,
)


HOMO_LUMO_GAP_RE = re.compile(r"^ HOMO - LUMO gap \[eV\]\s*:\s*(?P<val>\S+)\n", re.MULTILINE)


MOMENTS_RE = re.compile(
    r"""
^\ ELECTRIC/MAGNETIC\ MOMENTS
\s+ Reference\ Point\ \[Bohr\] (?:\ + (?P<ref>\S+)){3}
\s+ Charges
  (?:\s+(?P<charge_name>\w+)=\s*(?P<charge_value>\S+))+
(?:\s+ Dipoles .+
  \s+ Dipole\ moment\ \[[^\]]+\]
  (?:\s+(?P<dipole_coord>\w+)=\s*(?P<dipole_value>\S+))+
)?
(?:\s+ Quadrupole\ moment\ \[[^\]]+\]
  (?:\s+(?P<quadrupole_coord>\w+)=\s*(?P<quadrupole_value>\S+))+
)?
""",
    re.VERBOSE | re.MULTILINE,
)


OUTER_SCF_RE = re.compile(
    r"""
^
\s+ outer\ SCF\ iter\ = \s*\d+\ RMS\ gradient\ = \s* (?P<rms_gradient>\S+)\ energy\ = \s* (?P<energy>\S+) \n
\s+ outer\ SCF\ loop\ (?P<convtxt>converged\ in|FAILED\ to\ converge\ after)
    \s+ (?P<niter>\d+)\ iterations\ or \s+ (?P<nsteps>\d+)\ steps\n
""",
    re.VERBOSE | re.MULTILINE,
)


INNER_SCF_START_RE = re.compile(r"^\s+ SCF\ WAVEFUNCTION\ OPTIMIZATION", re.VERBOSE | re.MULTILINE)
INNER_SCF_CONV_RE = re.compile(
    r"^\s+ (?P<convtxt>\*\*\*\ SCF\ run\ converged\ in|Leaving\ inner\ SCF\ loop\ after\ reaching) \s+ (?P<nsteps>\d+)\ steps",
    re.VERBOSE | re.MULTILINE,
)


@dataclass
class DipoleMoment:
    x: Decimal
    y: Decimal
    z: Decimal
    total: Decimal


@dataclass
class QuadrupoleMoment:
    xx: Decimal
    xy: Decimal
    xz: Decimal
    yy: Decimal
    yz: Decimal
    zz: Decimal


@dataclass
class Moments:
    reference_point: Tuple[Decimal, Decimal, Decimal]
    electronic_charge: Decimal
    core_charge: Decimal
    total_charge: Decimal
    dipole: Optional[DipoleMoment] = None
    quadrupole: Optional[QuadrupoleMoment] = None


@dataclass
class MullikenPopulationAnalysis:
    elements: List[str]
    kinds: List[int]
    atomic_population_alpha: List[Decimal]
    atomic_population_beta: Optional[List[Decimal]]
    net_charge: List[Decimal]
    spin_moment: Optional[List[Decimal]]
    total_atomic_population_alpha: Decimal
    total_atomic_population_beta: Optional[Decimal]
    total_net_charge: Decimal
    total_spin_moment: Optional[Decimal]


@dataclass
class OuterSCF(Level):
    converged: bool
    niter: int
    nsteps: int
    rms_gradient: Decimal
    energy: Decimal


@dataclass
class InnerSCF(Level):
    converged: bool
    nsteps: int
    overlap_core_energy: Decimal
    self_core_energy: Decimal
    core_hamiltonian_energy: Decimal
    hartree_energy: Decimal
    xc_energy: Decimal
    total_energy: Decimal
    electronic_entropic_energy: Optional[Decimal] = None
    fermi_energy: Optional[Decimal] = None
    dispersion_energy: Optional[Decimal] = None


@dataclass
class SCF(Level):
    """The SCF procedure (which might again consist of InnerSCF or Outer+InnerSCF"""

    nspin: int
    nelec: Union[int, Tuple[int, int]]
    num_occ_orb: Union[int, Tuple[int, int]]
    num_mol_orb: Union[int, Tuple[int, int]]
    num_orb_func: int
    force_eval_energy: Optional[Decimal]
    messages: List[Message]
    fermi_energy: Optional[Union[Decimal, Tuple[Decimal, Decimal]]] = None
    homo_lumo_gap: Optional[Decimal] = None
    moments: Optional[Moments] = None
    mulliken_population_analysis: Optional[MullikenPopulationAnalysis] = None
    converged: bool = False


def match_scf(content: str, start: int = 0, end: int = sys.maxsize) -> Optional[Tuple[SCF, Tuple[int, int]]]:
    sublevels = []

    match = SCF_START_RE.search(content, start, end)

    if not match:
        return None, (start, end)

    start = match.span()[1]

    kv = match.capturesdict()

    try:
        nspin = int(kv.pop("spin")[1])
    except IndexError:
        nspin = 1

    for key in kv:
        kv[key] = [int(v) for v in kv[key]]

    if nspin == 1:
        for key in kv:
            kv[key] = kv[key][0]

    match = OUTER_SCF_RE.search(content, start, end)
    if match:
        sublevels.append(
            OuterSCF(
                converged=match["convtxt"] == "converged in",
                niter=int(match["niter"]),
                nsteps=int(match["nsteps"]),
                rms_gradient=Decimal(match["rms_gradient"]),
                energy=Decimal(match["energy"]) * UREG.hartree,
                sublevels=[],
            )
        )
        start = match.span()[1]  # if available, definitely before everything else below

    # try to match a single (inner) SCF
    match = INNER_SCF_START_RE.search(content, start, end)
    if match:
        start = match.span()[1]
        energy_match = MAIN_ENERGY_RE.search(content, start, end)
        conv_match = INNER_SCF_CONV_RE.search(content, start, end)
        if conv_match and energy_match:
            start = match.span()[1]
            kwargs = {
                key + "_energy": Decimal(val) * UREG.hartree for key, val in energy_match.groupdict().items() if val is not None
            }
            sublevels.append(
                InnerSCF(
                    converged="SCF run converged" in conv_match["convtxt"], nsteps=int(conv_match["nsteps"]), **kwargs, sublevels=[]
                )
            )

    force_eval_energy: Optional[Decimal] = None
    match = FORCE_EVAL_ENERGY_RE.search(content, start, end)
    if match:
        force_eval_energy = Decimal(match["value"]) * UREG.hartree
        end = match.span()[1]  # denotes the end of the SCF section

    scf = SCF(
        nspin=nspin,
        force_eval_energy=force_eval_energy,
        sublevels=sublevels,
        messages=list(match_messages(content, start, end)),
        converged=sublevels[-1].converged if sublevels else False,
        **kv,
    )

    match = HOMO_LUMO_GAP_RE.search(content, start, end)
    scf.homo_lumo_gap = Decimal(match["val"]) * UREG.eV if match else None

    match = EIGENVALUES_RE.search(content, start, end)
    if match:
        if nspin == 1:
            scf.fermi_energy = Decimal(match["fermi_energy"]) * UREG.eV
        else:
            scf.fermi_energy = tuple(Decimal(v) * UREG.eV for v in match.captures("fermi_energy"))

    match = MOMENTS_RE.search(content, start, end)  # TODO: there could be a second reference point
    if match:
        scf.moments = Moments(
            reference_point=tuple(Decimal(v) * UREG.bohr for v in match.captures("ref")),
            **{f"{k.lower()}_charge": Decimal(v) for k, v in zip(*match.captures("charge_name", "charge_value"))},
        )

        if match["dipole_coord"]:
            scf.moments.dipole = DipoleMoment(
                **{k.lower(): Decimal(v) * UREG.debye for k, v in zip(*match.captures("dipole_coord", "dipole_value"))}
            )

        if match["quadrupole_coord"]:
            scf.moments.quadrupole = QuadrupoleMoment(
                **{
                    k.lower(): Decimal(v) * UREG.debye * UREG.angstrom
                    for k, v in zip(*match.captures("quadrupole_coord", "quadrupole_value"))
                }
            )

    match = MULLIKEN_POPULATION_ANALYSIS_RE.search(content, start, end)
    if match:
        scf.mulliken_population_analysis = MullikenPopulationAnalysis(
            elements=match.captures("element"),
            kinds=[int(k) for k in match.captures("kind")],
            atomic_population_alpha=[Decimal(v) for v in match.captures("population_alpha" if nspin == 2 else "population")],
            atomic_population_beta=[Decimal(v) for v in match.captures("population_beta")] if nspin == 2 else None,
            net_charge=[Decimal(v) for v in match.captures("population_beta")],
            spin_moment=[Decimal(v) for v in match.captures("spin")] if nspin == 2 else None,
            total_atomic_population_alpha=Decimal(match["total_population_alpha"] if nspin == 2 else match["total_population"]),
            total_atomic_population_beta=Decimal(match["total_population_beta"]) if nspin == 2 else None,
            total_net_charge=Decimal(match["total_charge"]),
            total_spin_moment=Decimal(match["total_spin"]) if nspin == 2 else None,
        )

    return scf, (start, end)
