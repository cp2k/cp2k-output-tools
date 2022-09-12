import sys
from dataclasses import dataclass
from decimal import Decimal
from typing import List, Optional, Tuple

import regex as re

from . import UREG
from .common import Level
from .energies import FORCE_EVAL_ENERGY_RE
from .warnings import Message, match_messages

SIRIUS_START_RE = re.compile(r"^SIRIUS\ version \ *: \ + (?P<version>\S+)", re.VERBOSE | re.MULTILINE)

CONVERGED_RE = re.compile(r"^\[find\]\ converged\ after\ (?P<nsteps>\d+)\ SCF\ iterations!", re.VERBOSE | re.MULTILINE)


@dataclass
class Sirius(Level):
    """The SIRIUS FORCE_EVAL"""

    version: str
    force_eval_energy: Optional[Decimal]
    messages: List[Message]
    converged: bool


@dataclass
class SiriusSCF(Level):
    converged: bool
    nsteps: Optional[int]  # ideally we parse the max number of iterations and make this non-optional


def match_sirius(content: str, start: int = 0, end: int = sys.maxsize) -> Optional[Tuple[SiriusSCF, Tuple[int, int]]]:
    sirius_match = SIRIUS_START_RE.search(content, start, end)

    if not sirius_match:
        return None, (start, end)

    # update the start for the rest
    start = sirius_match.span()[0]

    force_eval_energy: Optional[Decimal] = None
    match = FORCE_EVAL_ENERGY_RE.search(content, start, end)
    if match:
        force_eval_energy = Decimal(match["value"]) * UREG.hartree
        end = match.span()[1]  # denotes the end of the SCF section

    match = CONVERGED_RE.search(content, start, end)
    if match:
        converged = True  # present only if converged
        nsteps = int(match["nsteps"])
    else:
        converged = False
        nsteps = None

    scf = SiriusSCF(
        converged=converged,
        nsteps=nsteps,
        sublevels=[],
    )

    sirius = Sirius(
        version=sirius_match["version"],
        converged=converged,
        force_eval_energy=force_eval_energy,
        messages=list(match_messages(content, start, end)),
        sublevels=[scf],
    )

    return sirius, (start, end)
