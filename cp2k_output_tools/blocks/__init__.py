from .bibliography import match_bibliography
from .condition_number import match_overlap_matrix_condition_number
from .energies import match_energies
from .forces import match_forces
from .kv_sections import match_kv_sections
from .mulliken import match_mulliken_population_analysis
from .program_info import match_program_info
from .warnings import match_warnings

builtin_matchers = [
    match_overlap_matrix_condition_number,
    match_mulliken_population_analysis,
    match_program_info,
    match_kv_sections,
    match_energies,
    match_forces,
    match_warnings,
    match_bibliography,
]
