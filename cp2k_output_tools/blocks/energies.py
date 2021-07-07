from typing import Optional

import regex as re

from .common import FLOAT, BlockMatch

FORCE_EVAL_ENERGY_RE = re.compile(
    rf"""
^\s*ENERGY\|\ Total\ FORCE_EVAL [^:]+:\s*(?P<value>{FLOAT})\n
""",
    re.VERBOSE | re.MULTILINE,
)


def match_energies(content: str) -> Optional[BlockMatch]:
    match = FORCE_EVAL_ENERGY_RE.search(content)

    if not match:
        return None

    return BlockMatch({"energies": {"total force_eval": float(match["value"])}}, match.spans(0))
