from .condition_number import match as match_overlap_condition_number
from .mulliken import match as match_mulliken

matchers = {"overlap_condition_number": match_overlap_condition_number, "mulliken_population_analysis": match_mulliken}

available_matchers = list(matchers.keys())
