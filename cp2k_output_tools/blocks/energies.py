from typing import Optional

import regex as re

from .common import FLOAT, BlockMatch

MAIN_ENERGY_RE = re.compile(
    rf"""
^\s*Overlap\ energy\ of\ the\ core\ charge\ distribution:\s*(?P<overlap_core>{FLOAT})\n
\s*Self\ energy\ of\ the\ core\ charge\ distribution:\s*(?P<self_core>{FLOAT})\n
\s*Core\ Hamiltonian\ energy:\s*(?P<core_hamiltonian>{FLOAT})\n
\s*Hartree\ energy:\s*(?P<hartree>{FLOAT})\n
(?:\s*Exchange-correlation\ energy:\s*(?P<xc>{FLOAT})\n)?
(?:\s*Electronic\ entropic\ energy:\s*(?P<electronic_entropic>{FLOAT})\n)?
(?:\s*Fermi\ energy:\s*(?P<fermi>{FLOAT})\n)?
(?:\s*Dispersion\ energy:\s*(?P<dispersion>{FLOAT})\n)?
\n
\s*Total\ energy:\s*(?P<total>{FLOAT})\n
""",
    re.VERBOSE | re.MULTILINE,
)


FORCE_EVAL_ENERGY_RE = re.compile(
    rf"""
^\s*ENERGY\|\ Total\ FORCE_EVAL [^:]+:\s*(?P<value>{FLOAT})\n
""",
    re.VERBOSE | re.MULTILINE,
)


def match_energies(content: str) -> Optional[BlockMatch]:
    spans = []
    energies = {}
    match = MAIN_ENERGY_RE.search(content)
    if match:
        energies = match.groupdict()
        spans = match.spans(0)
    match = FORCE_EVAL_ENERGY_RE.search(content)
    if match:
        energies["total force_eval"] = match["value"]
        spans += match.spans(0)
    if len(energies) == 0:
        return None
    return BlockMatch({"energies": {key: float(val) for key, val in energies.items() if val is not None}}, spans)
