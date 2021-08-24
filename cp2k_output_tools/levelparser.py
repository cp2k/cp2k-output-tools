"""This is the level-based parser, allowing to correctly parse arbitrarily nested CP2K output"""

import re
from dataclasses import dataclass
from functools import singledispatch
from typing import Optional

from .blocks.common import Level, Tree
from .blocks.geo_opt import (
    GeometryOptimization,
    GeometryOptimizationStep,
    match_geo_opt,
)

PROG_START_MATCH = re.compile(
    r"""
    (^(?:  # match any empty lines
        |SIRIUS\ \d.+  # SIRIUS library output
        |\ DBCSR\|.+   # DBCSR library output
        |(?:
            \ \*+\n    # RESTART block
            \ \*\s*RESTART\ INFORMATION\s*\*\n
            (?:\ \*.+\n)+
        )
    )\n)*
    \ [ \*]+\ PROGRAM\ STARTED\ AT .+
    """,
    re.VERBOSE | re.MULTILINE,
)


@dataclass
class CP2KRun(Level):
    pass


@singledispatch
def pretty_print(level, indent=""):
    pass


@pretty_print.register
def _(level: CP2KRun, indent=""):
    print(f"{indent}CP2K:")


@pretty_print.register
def _(level: GeometryOptimization, indent=""):
    print(f"{indent}Geometry Optimization:")
    print(f"{indent}    converged: {level.converged}")


@pretty_print.register
def _(level: GeometryOptimizationStep, indent=""):
    print(f"{indent}Geometry Optimization Step:")
    for msg in level.messages:
        print(f"{indent}    [{msg.type}]: {msg.message}")


def parse_all(content: str, start: Optional[int] = 0, end: Optional[int] = 0) -> Tree:
    levels = []

    starts = [match.span()[0] for match in PROG_START_MATCH.finditer(content, start)]
    for start, end in zip(starts, starts[1:] + [None]):
        sublevels = []
        geo_opt = match_geo_opt(content, start, end)
        if geo_opt:
            sublevels.append(geo_opt)

        levels.append(CP2KRun(sublevels=sublevels))

    return Tree(levels=levels)
