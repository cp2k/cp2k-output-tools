"""
Parse the CP2K bandstructure output file to a set of dataclasses
"""

__all__ = ["SpecialPoint", "Point", "BandstructureSet", "parse_bandstructure", "set_gen"]


import itertools
import re
from dataclasses import dataclass
from decimal import Decimal
from typing import Iterator, List, Optional, Tuple


@dataclass
class SpecialPoint:
    number: int
    name: str
    a: Decimal
    b: Decimal
    c: Decimal


@dataclass
class Point:
    a: Decimal
    b: Decimal
    c: Decimal
    bands: List[Decimal]
    spin: int
    weight: Optional[Decimal] = None


@dataclass
class BandstructureSet:
    setnr: int
    npoints: int
    nbands: Optional[int]
    points: List[Point]
    specialpoints: List[SpecialPoint]


SET_MATCH = re.compile(
    r"""
[ ]*
  SET: [ ]* (?P<setnr>\d+) [ ]*
  TOTAL [ ] POINTS: [ ]* (?P<npoints>\d+) [ ]*
  \n
(?P<content>
  [\s\S]*?(?=\n.*?[ ] SET|$)  # match everything until next 'SET' or EOL
)
""",
    re.VERBOSE,
)

SPOINTS_MATCH = re.compile(
    r"""
[ ]*
  POINT [ ]+ (?P<number>\d+) [ ]+ (?P<name>\S+) [ ]+ (?P<a>\S+) [ ]+ (?P<b>\S+) [ ]+ (?P<c>\S+)
""",
    re.VERBOSE,
)

POINTS_MATCH = re.compile(
    r"""
[ ]*
  Nr\. [ ]+ (?P<nr>\d+) [ ]+
  Spin [ ]+ (?P<spin>\d+) [ ]+
  K-Point [ ]+ (?P<a>\S+) [ ]+ (?P<b>\S+) [ ]+ (?P<c>\S+) [ ]*
  \n
[ ]* (?P<npoints>\d+) [ ]* \n
(?P<bands>
  [\s\S]*?(?=\n.*?[ ] Nr|$)  # match everything until next 'Nr.' or EOL
)
""",
    re.VERBOSE,
)


def _specialpoints_gen(content) -> Iterator[SpecialPoint]:
    for match in SPOINTS_MATCH.finditer(content):
        yield SpecialPoint(int(match["number"]), match["name"], Decimal(match["a"]), Decimal(match["b"]), Decimal(match["c"]))


def _points_gen(content) -> Iterator[Point]:
    for match in POINTS_MATCH.finditer(content):
        yield Point(
            a=Decimal(match["a"]),
            b=Decimal(match["b"]),
            c=Decimal(match["c"]),
            bands=[Decimal(v) for v in match["bands"].split()],
            spin=int(match["spin"]),
        )


SET_MATCH8 = re.compile(
    r"""
\#\ Set\ (?P<setnr>\d+):\ \d+\ special\ points,\ (?P<npoints>\d+)\ k-points,\ (?P<nbands>\d+)\ bands \s*
(?P<content>
  [\s\S]*?(?=\n.*?\#\ Set|$)  # match everything until next 'SET' or EOL
)
""",
    re.VERBOSE,
)


SPOINTS_MATCH8 = re.compile(
    r"""
\#\s+ Special\ point\ (?P<number>\d+) \s+ (?P<a>\S+) \s+ (?P<b>\S+) \s+ (?P<c>\S+) \s+ (?P<name>\S+)
""",
    re.VERBOSE,
)


POINTS_MATCH8 = re.compile(
    r"""
\#\ \ Point\ (?P<nr>\d+)\s+ Spin\ (?P<spin>\d+): \s+ (?P<a>\S+) \s+ (?P<b>\S+) \s+ (?P<c>\S+) [ ]* ((?P<weight>\S+) [ ]*)? \n
\#\ \ \ Band \s+ Energy\ \[eV\] \s+ Occupation \s*
(?P<bands>
  [\s\S]*?(?=\n.*?\#\ \ Point|$)  # match everything until next '# Point' or EOL
)
""",
    re.VERBOSE,
)


def _points_gen8(content: str) -> Iterator[Point]:
    for match in POINTS_MATCH8.finditer(content):
        weight: Optional[Decimal] = None
        try:
            weight = Decimal(match["weight"])
        except TypeError:
            pass  # ignore if None, conversion error is a ValueError

        values = match["bands"].split()

        yield Point(
            a=Decimal(match["a"]),
            b=Decimal(match["b"]),
            c=Decimal(match["c"]),
            bands=[Decimal(v) for v in values[1::3]],
            weight=weight,
            spin=int(match["spin"]),
        )


def _specialpoints_gen8(content: str) -> Iterator[SpecialPoint]:
    for match in SPOINTS_MATCH8.finditer(content):
        yield SpecialPoint(int(match["number"]), match["name"], Decimal(match["a"]), Decimal(match["b"]), Decimal(match["c"]))


def set_gen(content: str) -> Iterator[Tuple[int, int, Iterator[SpecialPoint], Iterator[Point]]]:
    """
    Parse the bandstructure from a CP2K bandstructure file content and return
    a tuple of metadata and SpecialPoint/Point Iterator.
    Supports both CP2K v8+ and previous version format transparently.
    """

    # try with the CP2K+8+ regex first
    matchiter = SET_MATCH8.finditer(content)
    specialpoints_gen = _specialpoints_gen8
    points_gen = _points_gen8

    try:
        peek = next(matchiter)
        matchiter = itertools.chain([peek], matchiter)
    except StopIteration:
        # if nothing could be found, fallback to the older format
        matchiter = SET_MATCH.finditer(content)
        specialpoints_gen = _specialpoints_gen
        points_gen = _points_gen

    for match in matchiter:
        nbands: Optional[int] = None

        try:
            nbands = int(match["nbands"])
        except IndexError:  # v7 doesn't have it (only implicitly)
            pass

        yield (
            int(match["setnr"]),
            int(match["npoints"]),
            nbands,
            specialpoints_gen(match["content"]),
            points_gen(match["content"]),
        )


def parse_bandstructure(content: str) -> Iterator[BandstructureSet]:
    """
    Parse the bandstructure from a CP2K bandstructure file content and return instances of BandstructureSet.
    """

    for setnr, npoints, nbands, spgen, pgen in set_gen(content):
        yield BandstructureSet(setnr, npoints, nbands, list(pgen), list(spgen))
