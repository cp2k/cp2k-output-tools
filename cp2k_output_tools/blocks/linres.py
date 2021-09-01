import sys
from dataclasses import dataclass
from decimal import Decimal
from typing import List, Optional, Tuple

import regex as re

from . import UREG
from .common import Level
from .warnings import Message, match_messages

LINRES_RE = re.compile(
    r"""
^\ =+\n
\ + START\ LINRES\ CALCULATION \n
\ \=+\n\n
\ LINRES\|\ Properties\ to\ be\ calculated:\n
(?:\ {2,}(?P<props>.+)\n)+
(?:\ LINRES\|\ (?P<key>(?:\S|\s(?!\s))+) \s+ (?P<value>.+)\n)+
""",
    re.VERBOSE | re.MULTILINE,
)

LINRES_END_RE = re.compile(
    r"""
^\ =+\n
\ \s+ ENDED\ LINRES\ CALCULATION .+\n
\ \=\n
""",
    re.VERBOSE | re.MULTILINE,
)

POLARIZABILITY_TENSOR_RE = re.compile(
    r"""
\ POLAR\|\ Polarizability\ tensor\ \[a\.u\.\]\n
(?:\ POLAR\|\ (?:(?P<coord>\w\w)[,\s]+){3} (?:\s+(?P<val>\S+)){3} \n) +
""",
    re.VERBOSE | re.MULTILINE,
)


@dataclass
class PolarizabilityTensor:
    xx: Decimal
    yy: Decimal
    zz: Decimal
    xy: Decimal
    xz: Decimal
    yz: Decimal
    yx: Decimal
    zx: Decimal
    zy: Decimal


@dataclass
class Linres(Level):
    properties: List[str]
    optimization_algorithm: str
    preconditioner: str
    eps: Decimal
    max_iter: int
    messages: List[Message]
    polarizability_tensor: Optional[PolarizabilityTensor]


def match_linres(content: str, start: int = 0, end: int = sys.maxsize) -> Optional[Tuple[Linres, Tuple[int, int]]]:
    match = LINRES_RE.search(content, start, end)

    if not match:
        return None, (start, end)

    start = match.span()[1]

    props = match.captures("props")
    kv = dict(zip([k.lower().replace(" ", "_") for k in match.captures("key")], match.captures("value")))
    kv["eps"] = Decimal(kv["eps"])
    kv["max_iter"] = int(kv["max_iter"])

    match = LINRES_END_RE.search(content, start, end)
    if match:
        end = match.span()[0]

    msgs = list(match_messages(content, start, end))

    ptensor: Optional[PolarizabilityTensor] = None
    match = POLARIZABILITY_TENSOR_RE.search(content, start, end)
    if match:
        ptensor = PolarizabilityTensor(**{k: Decimal(v) * UREG.bohr ** 3 for k, v in zip(*match.captures("coord", "val"))})

    # TODO: linres contains minimalization loops which should go into sublevels
    return Linres(properties=props, messages=msgs, polarizability_tensor=ptensor, sublevels=[], **kv), (start, end)
