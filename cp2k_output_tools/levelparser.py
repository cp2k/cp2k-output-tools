"""This is the level-based parser, allowing to correctly parse arbitrarily nested CP2K output"""

import re
import sys
from dataclasses import dataclass
from functools import singledispatch
from typing import List, Optional

from .blocks.cell import CellInformation, match_cell
from .blocks.common import Level, Tree
from .blocks.geo_opt import (
    GeometryOptimization,
    GeometryOptimizationStep,
    match_geo_opt,
)
from .blocks.linres import Linres, match_linres
from .blocks.program_info import ProgramInfo, match_program_info
from .blocks.scf import SCF, InnerSCF, OuterSCF, match_scf
from .blocks.vibrational import VibrationalAnalysis, match_vibrational_analysis

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
    cell_infos: List[CellInformation]


@singledispatch
def pretty_print(level, indent=""):
    print(f"{indent}{type(level).__name__}:")


@pretty_print.register
def _(level: CP2KRun, indent=""):
    print(f"{indent}CP2K:")
    print(f"{indent}    started at: {level.program_info.started_at}")
    print(f"{indent}    ended at: {level.program_info.ended_at}")
    for cell_info in level.cell_infos:
        print(f"{indent}    {cell_info.cell_info_type} cell volume: {cell_info.volume}")


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

    for msg in level.messages:
        print(f"{indent}    [{msg.type}]: {msg.message}")


@pretty_print.register
def _(scf: SCF, indent=""):
    print(f"{indent}SCF:")
    print(f"{indent}    converged: {scf.converged}")
    if scf.force_eval_energy:
        print(f"{indent}    Total FORCE_EVAL energy: {scf.force_eval_energy}")

    if scf.homo_lumo_gap:
        print(f"{indent}    HOMO-LUMO Gap: {scf.homo_lumo_gap}")

    if scf.fermi_energy:
        print(f"{indent}    Fermi energy: {scf.fermi_energy}")

    if scf.moments:
        print(f"{indent}    Moments:")
        print(f"{indent}        Ref.point:", scf.moments.reference_point)
        print(f"{indent}        Dipole available:", bool(scf.moments.dipole))
        print(f"{indent}        Quadrupole available:", bool(scf.moments.quadrupole))

    if scf.mulliken_population_analysis:
        print(f"{indent}    Mulliken Population Analysis:")
        print(f"{indent}        (present)")

    for msg in scf.messages:
        print(f"{indent}    [{msg.type}]: {msg.message}")


@pretty_print.register
def _(outer_scf: OuterSCF, indent=""):
    print(f"{indent}Outer SCF:")
    print(f"{indent}    converged: {outer_scf.converged}")
    print(f"{indent}    number of iterations: {outer_scf.niter}")
    print(f"{indent}    total number of steps: {outer_scf.nsteps}")
    print(f"{indent}    RMS gradient: {outer_scf.rms_gradient}")
    print(f"{indent}    energy: {outer_scf.energy}")


@pretty_print.register
def _(innner_scf: InnerSCF, indent=""):
    print(f"{indent}Inner SCF:")
    print(f"{indent}    converged: {innner_scf.converged}")
    print(f"{indent}    number of steps: {innner_scf.nsteps}")


@pretty_print.register
def _(vib_analysis: VibrationalAnalysis, indent=""):
    print(f"{indent}Vibrational Analysis:")
    if vib_analysis.data:
        print(f"{indent}    Modes found: {len(vib_analysis.data.frequencies)}")

    for msg in vib_analysis.messages:
        print(f"{indent}    [{msg.type}]: {msg.message}")


def parse_all(content: str, start: int = 0, end: int = sys.maxsize) -> Tree:
    levels = []

    starts = [match.span()[0] for match in PROG_START_MATCH.finditer(content, start)]
    for start, end in zip(starts, starts[1:] + [None]):
        sublevels = []

        program_info = match_program_info(content, start, end, as_tree_obj=True)

        cell_infos = []
        while True:
            cell_info, span = match_cell(content, start, end)
            if cell_info is None:
                break

            cell_infos.append(cell_info)
            start = span[1]  # move the start ahead to the end of the cell section

        geo_opt, span = match_geo_opt(content, start, end)
        if geo_opt:
            sublevels.append(geo_opt)
            start = span[1]

        scf, span = match_scf(content, start, end)
        if scf:
            sublevels.append(scf)
            start = span[1]

        linres, span = match_linres(content, start, end)
        if linres:
            sublevels.append(linres)
            start = span[1]

        vib_analysis, span = match_vibrational_analysis(content, start, end)
        if vib_analysis:
            sublevels.append(vib_analysis)
            start = span[1]

        levels.append(CP2KRun(sublevels=sublevels, program_info=program_info, cell_infos=cell_infos))

    return Tree(levels=levels)
