import sys
from dataclasses import dataclass
from decimal import Decimal
from math import ceil
from typing import List, Optional, Tuple

import numpy as np
import numpy.typing as npt
import regex as re

from . import UREG
from .warnings import Message, match_messages

VIB_ANALYSIS_START_RE = re.compile(
    r"""
^(?:\ \*+\n){2}
[\*\s#]+ N\.\ Replicas:\s+ (?P<nreplicas>\d+)
[\*\s#]+ N\.\ Procs/Rep:\s+ (?P<nprocs_per_rep>\d+)
(?:[\*\s#]+ [\w\s.-]+){2}
(?:\ \*+\n){3}
""",
    re.VERBOSE | re.MULTILINE,
)

FREQUENCY_RE = re.compile(
    r"""
^
(?:
  \ VIB\|(?:\ +(?P<colnr>\d+)){1,3} \n
  \ VIB\|Frequency\ \(cm\^-1\) (?:\ +(?P<freq>\S+)){1,3} \n
  (\ VIB\|(?:Intensities|IR\ int\ \(KM/Mole\)) (?:\ +(?P<intens>\S+)){1,3} \n)?
  \ VIB\|Red\.Masses\ \(a\.u\.\) (?:\ +(?P<mass>\S+)){1,3} \n
  \ VIB\|Frc\ consts\ \(a\.u\.\) (?:\ +(?P<frcc>\S+)){1,3} \n
  \ +ATOM\ +EL (?:\ +[XYZ])+ \ * \n
  (\ + (?P<idx>\d+) \ + (?P<sym>\w+) (?:(?:\ + (?P<coord>\S+)){3}){1,3} \n )+
  \n\n
)+
""",
    re.VERBOSE | re.MULTILINE,
)


@dataclass
class Data:
    frequencies: List[Decimal]
    reduced_masses: List[Decimal]
    force_constants: List[Decimal]
    intensities: Optional[List[Decimal]]
    atomic_symbols: List[int]
    normal_coords: npt.NDArray


@dataclass
class VibrationalAnalysis:
    data: Optional[Data]
    messages: List[Message]


def _match_data(content: str, start: int = 0, end: int = sys.maxsize) -> Tuple[Optional[VibrationalAnalysis], Tuple[int, int]]:

    match = FREQUENCY_RE.search(content, start, end)

    if not match:
        return None, (start, end)

    natoms = max(int(n) for n in match.captures("idx"))
    ncols = int(match["colnr"])  # get the last colnr, which is equal the number of frequencies

    # the capture contains a list of all atom indexes (repeated in each column):
    normal_coords = np.empty((ncols, natoms, 3))

    nblocks = ceil(ncols / 3)
    coords = match.captures("coord")
    for block in range(0, nblocks):
        nbcols = min(3, ncols - block * 3)
        for col in range(0, nbcols):
            for row in range(natoms):
                idx = row * 3 * nbcols + block * 9 * natoms + 3 * col
                normal_coords[col + 3 * block, row, :] = [Decimal(d) for d in coords[idx : idx + 3]]

    intensities: Optional[List[Decimal]] = None
    if match["intens"]:
        intensities = [Decimal(v) * UREG.kilometers / UREG.mole for v in match.captures("intens")]

    return (
        Data(
            frequencies=[Decimal(v) * UREG.cm**-1 for v in match.captures("freq")],
            reduced_masses=[Decimal(v) * UREG.amu for v in match.captures("mass")],
            force_constants=[Decimal(v) * UREG.hartree / UREG.bohr**2 for v in match.captures("frcc")],  # TODO: check
            intensities=intensities,
            atomic_symbols=match.captures("sym")[:natoms],
            normal_coords=normal_coords * UREG.angstrom,
        ),
        (match.span()[1], end),
    )


def match_vibrational_analysis(
    content: str, start: int = 0, end: int = sys.maxsize
) -> Tuple[Optional[VibrationalAnalysis], Tuple[int, int]]:

    match = VIB_ANALYSIS_START_RE.search(content, start, end)

    if not match:
        return None, (start, end)

    start = match.span()[1]

    data, span = _match_data(content, start, end)

    messages = list(match_messages(content, start, end))

    return VibrationalAnalysis(data=data, messages=messages), (span[1], end)
