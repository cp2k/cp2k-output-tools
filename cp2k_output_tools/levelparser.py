"""This is the level-based parser, allowing to correctly parse arbitrarily nested CP2K output"""

import re
import sys
from dataclasses import dataclass
from functools import singledispatch
from typing import Optional

from .blocks.common import Level, Tree
from .blocks.geo_opt import (
    GeometryOptimization,
    GeometryOptimizationStep,
    match_geo_opt,
)
from .blocks.linres import Linres, match_linres
from .blocks.program_info import ProgramInfo, match_program_info
from .blocks.scf import SCF, match_scf

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
    program_info: Optional[ProgramInfo]


@singledispatch
def pretty_print(level, indent=""):
    print(f"{indent}{type(level).__name__}:")


@pretty_print.register
def _(level: CP2KRun, indent=""):
    print(f"{indent}CP2K:")
    print(f"{indent}    started at: {level.program_info.started_at}")
    print(f"{indent}    ended at: {level.program_info.ended_at}")


@pretty_print.register
def _(level: GeometryOptimization, indent=""):
    print(f"{indent}Geometry Optimization:")
    print(f"{indent}    converged: {level.converged}")


@pretty_print.register
def _(level: GeometryOptimizationStep, indent=""):
    print(f"{indent}Geometry Optimization Step:")
    for msg in level.messages:
        print(f"{indent}    [{msg.type}]: {msg.message}")


@pretty_print.register
def _(level: Linres, indent=""):
    print(f"{indent}Linres:")
    print(f"{indent}    properties: {', '.join(level.properties)}")

    if level.polarizability_tensor:
        print(f"{indent}    Polarizability Tensor:", level.polarizability_tensor)

    for msg in level.messages:
        print(f"{indent}    [{msg.type}]: {msg.message}")


@pretty_print.register
def _(level: SCF, indent=""):
    print(f"{indent}SCF:")
    if level.force_eval_energy:
        print(f"{indent}    Total FORCE_EVAL energy: {level.force_eval_energy}")

    for msg in level.messages:
        print(f"{indent}    [{msg.type}]: {msg.message}")


def parse_all(content: str, start: int = 0, end: int = sys.maxsize) -> Tree:
    levels = []

    starts = [match.span()[0] for match in PROG_START_MATCH.finditer(content, start)]
    for start, end in zip(starts, starts[1:] + [None]):
        sublevels = []

        geo_opt = match_geo_opt(content, start, end)
        if geo_opt:
            sublevels.append(geo_opt)

        scf = match_scf(content, start, end)
        if scf:
            sublevels.append(scf)

        linres = match_linres(content, start, end)
        if linres:
            sublevels.append(linres)

        program_info = match_program_info(content, start, end, as_tree_obj=True)

        levels.append(CP2KRun(sublevels=sublevels, program_info=program_info))

    return Tree(levels=levels)
