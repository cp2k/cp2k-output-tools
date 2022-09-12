import sys
from dataclasses import dataclass
from decimal import Decimal
from enum import Enum
from typing import List, Optional, Tuple

import numpy as np
import numpy.typing as npt
import regex as re

from . import UREG

CELL_RE = re.compile(
    r"""
^(?:
  \ (?P<name>CELL(?P<type>_REF|_TOP)?)\|
  \ 
  (?P<key>.+?(?=\ {3}))  # match everything unless followed by 3 spaces
  \s+
  (?P<value>.+)
  \n
 )+
""",  # noqa: W291
    re.VERBOSE | re.MULTILINE,
)


class CellInfoType(str, Enum):
    default = ""
    reference = "REF"
    top = "TOP"


@dataclass
class CellInformation:
    cell_info_type: CellInfoType
    volume: Decimal
    vectors: npt.NDArray
    vector_norms: List[Decimal]
    angles: List[Decimal]
    numerically_orthorombic: bool
    periodicity: Optional[str]  # older versions of CP2K did not output this one


def match_cell(content: str, start: int = 0, end: int = sys.maxsize) -> Tuple[Optional[CellInformation], Tuple[int, int]]:

    match = CELL_RE.search(content, start, end)

    if not match:
        return None, (start, end)

    vectors = []
    vector_norms = []
    vector_unit = None
    numerically_orthorombic = None
    volume = None
    angles = []
    periodicity: Optional[str] = None

    for key, value in zip(*match.captures("key", "value")):
        try:
            name, unit = key.split("[")
            unit = unit.rstrip(":").rstrip("]")  # some units have formatting errors and are missing the right bracket
        except ValueError:
            name = key

        name = name.rstrip(":").strip()

        if name == "Numerically orthorhombic":
            if value == "YES":
                numerically_orthorombic = True
            elif value == "NO":
                numerically_orthorombic = False
        elif name == "Volume":
            volume = Decimal(value) * UREG(unit)
        elif name == "Periodicity":
            periodicity = value
        elif "=" in value:
            a, b, c, _, _, norm = value.split()
            vector_unit = UREG(unit)
            vectors.append([Decimal(a), Decimal(b), Decimal(c)])
            vector_norms.append(Decimal(norm) * vector_unit)
        elif "Angle" in name:
            angles.append(Decimal(value) * UREG(unit))
        else:
            raise AssertionError(f"No matching clause for '{name}'")

    if match["type"]:
        cell_info_type = CellInfoType(match["type"][1:])  # strip the '_'
    else:
        cell_info_type = CellInfoType.default

    return (
        CellInformation(
            cell_info_type=cell_info_type,
            volume=volume,
            vectors=np.array(vectors) * vector_unit,
            vector_norms=vector_norms,
            angles=angles,
            numerically_orthorombic=numerically_orthorombic,
            periodicity=periodicity,
        ),
        match.span(),
    )
