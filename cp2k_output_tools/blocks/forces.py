from typing import Optional
import regex as re
from .common import FLOAT, BlockMatch


FORCES_RE = re.compile(
    rf"""
# anchor to indicate beginning of the FORCES output
^\ (?P<type>\w+)\ FORCES\ in\ \[(?P<unit>[^\]]+)\] \s* \n\n
 \ \#  .+ \n  # match the header
(
 \s+ (?P<atom>\d+) \s+ (?P<kind>\d+) \s+ (?P<element>\w+) \s+
     (?P<x>{FLOAT}) \s+ (?P<y>{FLOAT}) \s+ (?P<z>{FLOAT}) \s* \n
)+
\ SUM\ OF\ (?P<type>\w+)\ FORCES \s+
(
      (?P<sum_x>{FLOAT}) \s+
      (?P<sum_y>{FLOAT}) \s+
      (?P<sum_z>{FLOAT}) \s+
      (?P<norm>{FLOAT})
) \s* \n
""",
    re.VERSION1 | re.MULTILINE | re.VERBOSE,
)


def match_forces(content: str) -> Optional[BlockMatch]:
    forces = {}
    spans = []

    for match in FORCES_RE.finditer(content):
        ftype = match["type"].lower()

        per_atom = [
            {
                "atom": int(atom),
                "kind": int(kind),
                "element": element,
                "x": float(x),
                "y": float(y),
                "z": float(z),
            }
            for atom, kind, element, x, y, z in zip(*match.captures("atom", "kind", "element", "x", "y", "z"))
        ]
        fsum = {
            "x": float(match["sum_x"]),
            "y": float(match["sum_y"]),
            "z": float(match["sum_z"]),
            "norm": float(match["norm"]),
        }

        forces[ftype] = {"unit": match["unit"], "per_atom": per_atom, "sum": fsum}
        spans += match.spans(0)

    return BlockMatch({"forces": forces}, spans)
