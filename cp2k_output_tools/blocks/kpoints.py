from typing import Any, Dict, Iterator, Optional

import regex as re

from .common import FLOAT, BlockMatch

KPOINTS_BLOCK_RE = re.compile(
    r"""
^
\ KPOINTS\|\ Band\ Structure\ Calculation \s*\n
\ KPOINTS\|\ Number\ of\ (?P<marker>k-point)\ sets \s* (?P<nsets>\d+)\n
(?:\ KPOINTS\|\ Number\ of\ added\ MOs/bands \s+ (?P<nmos>\d+)\n)?
(?P<content>.*?)\n{2}
""",
    re.MULTILINE | re.VERBOSE | re.IGNORECASE | re.DOTALL,
)

KPOINTS_SET_RE = re.compile(
    rf"""
\ KPOINTS\|\ Number\ of\ k-points\ in\ set \s+ (?P<setnr>\d+) \s+ (?P<npoints>\d+) \s*\n
\ KPOINTS\|\ In\ units\ of\ b-vector\ \[(?P<unit>[^\]]+)\] \s*\n
(\ KPOINTS\|\ Special\ (?:K\-)?point \s+ (?P<specialnr>\d+) \s+ (?P<specialname>.+?)
  \s+ (?P<speciala>{FLOAT}) \s+ (?P<specialb>{FLOAT}) \s+ (?P<specialc>{FLOAT}) \n)+
(?P<content>[\s\S]*?)
\ KPOINTS\|\ Time\ for\ k-point\ line \s+ (?P<time>\S+)
""",
    re.VERSION1 | re.MULTILINE | re.VERBOSE | re.IGNORECASE,
)

POINTS_MATCH = re.compile(
    r"""
[ ]*
  Nr\. \s+ (?P<nr>\d+) \s+
  Spin \s+ (?P<spin>\d+) \s+
  K-Point \s+ (?P<a>\S+) \s+ (?P<b>\S+) \s+ (?P<c>\S+) \s*
  \n
\s* (?P<npoints>\d+) \s* \n
(?P<bands>
  [\s\S]*?(?=\n.*?\s+ Nr|$)  # match everything until next 'Nr.' or EOL
)
""",
    re.VERBOSE,
)


POINTS_MATCH8 = re.compile(
    r"""
\#\ \ Point\ (?P<nr>\d+)\s+ Spin\ (?P<spin>\d+): \s+ (?P<a>\S+) \s+ (?P<b>\S+) \s+ (?P<c>\S+) \s* (?:(?P<weight>\S+) \s*)? \n
\#\ \ \ Band \s+ Energy\ \[eV\] \s+ Occupation \s*
(?P<bands>
  [\s\S]*?(?=\n.*?\#\s+ Point|$)  # match everything until next '# Point' or EOL
)
""",
    re.VERBOSE,
)


def _points_gen(content) -> Iterator[Dict[str, Any]]:
    for match in POINTS_MATCH.finditer(content):
        yield {
            "a": float(match["a"]),
            "b": float(match["b"]),
            "c": float(match["c"]),
            "bands": [float(v) for v in match["bands"].split()],
            "spin": int(match["spin"]),
        }


def _points_gen8(content: str) -> Iterator[Dict[str, Any]]:
    for match in POINTS_MATCH8.finditer(content):
        weight: Optional[float] = None
        try:
            weight = float(match["weight"])
        except TypeError:
            pass  # ignore if None, conversion error is a ValueError

        values = match["bands"].split()

        yield {
            "a": float(match["a"]),
            "b": float(match["b"]),
            "c": float(match["c"]),
            "bands": [float(v) for v in values[1::3]],
            "weight": weight,
            "spin": int(match["spin"]),
        }


def match_kpoints(content: str) -> Optional[BlockMatch]:
    kpsets = []
    nadded_mos = None

    match = KPOINTS_BLOCK_RE.search(content)

    if not match:
        return None

    spans = match.spans(0)
    nsets = int(match["nsets"])

    if not nsets:
        return None

    if match["marker"] == "K-Point":  # CP2K < 8 had it capitalized
        points_gen = _points_gen
    else:
        points_gen = _points_gen8

    try:
        nadded_mos = int(match["nmos"])
    except TypeError:
        pass  # optional

    block_content = match["content"]

    for match in KPOINTS_SET_RE.finditer(block_content):
        specialpoints = [
            {
                "nr": int(nr),
                "name": name,
                "a": float(a),
                "b": float(b),
                "c": float(c),
            }
            for nr, name, a, b, c in zip(*match.captures("specialnr", "specialname", "speciala", "specialb", "specialc"))
        ]

        kpsets.append(
            {
                "time": float(match["time"]),
                "setnr": int(match["setnr"]),
                "npoints": int(match["npoints"]),
                "unit": match["unit"],
                "specialpoints": specialpoints,
                "points": list(points_gen(match["content"])),
            }
        )

        assert (
            len(kpsets[-1]["points"]) == kpsets[-1]["npoints"]
        ), "Number of parsed kpoints does not match the declared number of kpoints"

    assert len(kpsets) == nsets, "Number of parsed KP sets does not match the declared number of sets"

    data = {"sets": kpsets, "nsets": nsets}

    if nadded_mos:
        data["nadded_mos"] = nadded_mos

    return BlockMatch({"kpoints": {"bandstructure": data}}, spans)
