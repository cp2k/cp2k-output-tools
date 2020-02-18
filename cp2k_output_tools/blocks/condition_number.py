import regex as re
from .common import FLOAT, MatcherResult


MATCH = re.compile(
    rf"""
# anchor to indicate beginning the overlap matrix condition number section
^[ \t]* OVERLAP\ MATRIX\ CONDITION\ NUMBER\ AT\ GAMMA\ POINT [ \t]* \n
 [ \t]* 1-Norm\ Condition\ Number\ \(Estimate\) [ \t]* \n
 [ \t]* CN\ :\ \|A\|\*\|A\^-1\|:
   [ \t]* (?P<norm1_estimate_A>({FLOAT}))
   [ \t]* \*
   [ \t]* (?P<norm1_estimate_Ainv>({FLOAT}))
   [ \t]* =
   [ \t]* (?P<norm1_estimate>({FLOAT}))
   [ \t]* Log\(1-CN\):
   [ \t]* (?P<norm1_estimate_log>({FLOAT}))
   [ \t]* \n

 [ \t]* 1-Norm\ and\ 2-Norm\ Condition\ Numbers\ using\ Diagonalization [ \t]* \n

 [ \t]* CN\ :\ \|A\|\*\|A\^-1\|:
   [ \t]* (?P<norm1_diag_A>({FLOAT})) [ \t]* \* [ \t]* (?P<norm1_diag_Ainv>({FLOAT}))
   [ \t]* =
   [ \t]* (?P<norm1_diag>({FLOAT})) [ \t]* Log\(1-CN\): [ \t]* (?P<norm1_diag_log>({FLOAT}))
   [ \t]* \n

 [ \t]* CN\ :\ max/min\ ev:
   [ \t]* (?P<norm2_diag_max_ev>({FLOAT})) [ \t]* / [ \t]* (?P<norm2_diag_min_ev>({FLOAT}))
   [ \t]* =
   [ \t]* (?P<norm2_diag>({FLOAT})) [ \t]* Log\(2-CN\): [ \t]* (?P<norm2_diag_log>({FLOAT}))
   [ \t]* \n
""",
    re.MULTILINE | re.VERBOSE,
)


def match(content):
    match = MATCH.search(content)

    if match is None:
        return None

    captures = match.groupdict()

    return MatcherResult(
        {
            "1-norm (estimate)": {
                "|A|": float(captures["norm1_estimate_A"]),
                "|A^-1|": float(captures["norm1_estimate_Ainv"]),
                "CN": float(captures["norm1_estimate"]),
                "Log(CN)": float(captures["norm1_estimate_log"]),
            },
            "1-norm (using diagonalization)": {
                "|A|": float(captures["norm1_diag_A"]),
                "|A^-1|": float(captures["norm1_diag_Ainv"]),
                "CN": float(captures["norm1_diag"]),
                "Log(CN)": float(captures["norm1_diag_log"]),
            },
            "2-norm (using diagonalization)": {
                "max EV": float(captures["norm2_diag_max_ev"]),
                "min EV": float(captures["norm2_diag_min_ev"]),
                "CN": float(captures["norm2_diag"]),
                "Log(CN)": float(captures["norm2_diag_log"]),
            },
        },
        match.span(),
    )
