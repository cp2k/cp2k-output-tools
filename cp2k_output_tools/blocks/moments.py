import math
from typing import Optional

import regex as re

from .common import BlockMatch

MOMENTS_TRAJECTORY_RE = re.compile(r"^[ \t]*(?P<label>MOMENTS(?:_REF2)?)\|(?P<record>[^\r\n]*)", re.MULTILINE)


def match_moments(content: str) -> Optional[BlockMatch]:
    """Parse compact electric-moment trajectories, preserving restart order.

    Dipoles and the optional row-major cell matrix retain CP2K's printed units.
    In Berry-phase records the cell entries are lattice factors scaled to Debye,
    not geometric cell lengths in angstrom.
    """
    moments = {"unit": "Debye", "primary": [], "reference 2": []}
    spans = []
    for match in MOMENTS_TRAJECTORY_RE.finditer(content):
        fields = match["record"].split()
        try:
            if len(fields) not in (5, 14):
                raise ValueError("expected an iteration identifier and 4 or 13 numeric values")
            values = [float(value.replace("D", "E").replace("d", "e")) for value in fields[1:]]
            if not all(math.isfinite(value) for value in values):
                raise ValueError("non-finite numeric value")
        except ValueError as error:
            line = content.count("\n", 0, match.start()) + 1
            raise ValueError(f"Invalid {match['label']}| record on line {line}: {error}") from error

        record = {
            "iteration": fields[0],
            "dipole": dict(zip(("x", "y", "z", "norm"), values[:4])),
            "cell": [values[start : start + 3] for start in (4, 7, 10)] if len(values) == 13 else None,
        }
        key = "primary" if match["label"] == "MOMENTS" else "reference 2"
        moments[key].append(record)
        spans.append(match.span())

    return BlockMatch({"moments": moments}, spans) if spans else None
