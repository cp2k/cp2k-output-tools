import sys
from dataclasses import dataclass
from decimal import Decimal
from typing import List, Optional, Tuple, Union

import regex as re

from . import UREG
from .common import FLOAT, Level
from .energies import FORCE_EVAL_ENERGY_RE
from .warnings import Message, match_messages

SCF_START_RE = re.compile(
    r"""
^(?:
  (?:\ Spin\s+(?P<spin>\d+)\n)?
  \ Number\ of\ electrons:\s+ (?P<nelec>\d+)\n
  \ Number\ of\ occupied\ orbitals:\s+  (?P<num_occ_orb>\d+)\n
  \ Number\ of\ molecular\ orbitals:\s+ (?P<num_mol_orb>\d+)\n
){1,2}
\n
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
class SCF(Level):
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


def match_scf(content: str, start: int = 0, end: int = sys.maxsize) -> Optional[Tuple[SCF, Tuple[int, int]]]:
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

    force_eval_energy: Optional[Decimal] = None
    match = FORCE_EVAL_ENERGY_RE.search(content, match.span()[1], end)
    if match:
        force_eval_energy = Decimal(match["value"]) * UREG.hartree
        end = match.span()[0]

    # TODO: can have outer and inner loop
    scf = SCF(
        nspin=nspin, force_eval_energy=force_eval_energy, sublevels=[], messages=list(match_messages(content, start, end)), **kv
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

    return scf, (start, end)
