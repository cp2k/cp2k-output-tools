import sys
from dataclasses import dataclass
from decimal import Decimal
from typing import List, Optional, Tuple, Union

import regex as re

from . import UREG
from .common import Level
from .energies import FORCE_EVAL_ENERGY_RE
from .warnings import Message, match_messages

SCF_START_RE = re.compile(
    r"""
^(?:
  (?:\ Spin\s+(?P<nspins>\d+)\n)?
  \n
  \ Number\ of\ electrons:\s+ (?P<nelec>\d+)\n
  \ Number\ of\ occupied\ orbitals:\s+  (?P<num_occ_orb>\d+)\n
  \ Number\ of\ molecular\ orbitals:\s+ (?P<num_mol_orb>\d+)\n
){1,2}
\n
\ Number\ of\ orbital\ functions:\s+ (?P<num_orb_func>\d+)\n
    """,
    re.VERBOSE | re.MULTILINE,
)


@dataclass
class SCF(Level):
    nspins: int
    nelec: Union[int, Tuple[int, int]]
    num_occ_orb: Union[int, Tuple[int, int]]
    num_mol_orb: Union[int, Tuple[int, int]]
    num_orb_func: int
    force_eval_energy: Optional[Decimal]
    messages: List[Message]


def match_scf(content: str, start: int = 0, end: int = sys.maxsize) -> Optional[SCF]:
    match = SCF_START_RE.search(content, start, end)

    if not match:
        return None

    start = match.span()[1]

    kv = match.capturesdict()

    nspins = len(kv.pop("nspins"))

    for key in kv:
        kv[key] = [int(v) for v in kv[key]]

    if nspins == 1:
        for key in kv:
            kv[key] = kv[key][0]

    force_eval_energy: Optional[Decimal] = None
    match = FORCE_EVAL_ENERGY_RE.search(content, match.span()[1], end)
    if match:
        force_eval_energy = Decimal(match["value"]) * UREG.hartree
        end = match.span()[0]

    # TODO: can have outer and inner loop
    return SCF(
        nspins=nspins, force_eval_energy=force_eval_energy, sublevels=[], messages=list(match_messages(content, start, end)), **kv
    )
