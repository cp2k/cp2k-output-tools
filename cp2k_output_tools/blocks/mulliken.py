import regex as re
from .common import FLOAT


MULLIKEN_POPULATION_ANALYSIS_RE = re.compile(
    rf"""
# anchor to indicate beginning of the Mulliken Population Analysis
^[ \t]* Mulliken\ Population\ Analysis [ \t]* \n
 [ \t]* \n
 [ \t]* \#  [\w \t\,\(\)]+\n  # match the header
(
  ^
  [ \t]*
  (?P<atom>\d+) [ \t]+
  (?P<element>\w+) [ \t]+
  (?P<kind>\d+) [ \t]+
  (
    ( # spin unrestricted case:
      (?P<population_alpha>({FLOAT})) [ \t]+ (?P<population_beta>({FLOAT})) [ \t]+
      (?P<charge>({FLOAT})) [ \t]+ (?P<spin>({FLOAT}))
    )
    |
    (
      (?P<population>({FLOAT})) [ \t]+
      (?P<charge>({FLOAT}))
    )
  ) [ \t]*
  \n
)+
^ [ \t]* \#\ Total\ charge (\ and\ spin)? [ \t]+
(
  ( # spin unrestricted case:
    (?P<total_population_alpha>({FLOAT})) [ \t]+ (?P<total_population_beta>({FLOAT})) [ \t]+
    (?P<total_charge>({FLOAT})) [ \t]+ (?P<total_spin>({FLOAT}))
  )
  |
  (
    (?P<total_population>({FLOAT})) [ \t]+
    (?P<total_charge>({FLOAT}))
  )
) [ \t]*
\n
""",
    re.VERSION1 | re.MULTILINE | re.VERBOSE,
)


def match_mulliken_population_analysis(content):
    match = MULLIKEN_POPULATION_ANALYSIS_RE.search(content)

    if match is None:
        return None

    captures = match.capturesdict()
    per_atom = []

    if captures.get("population_alpha"):
        for idx in range(len(captures["atom"])):
            per_atom.append(
                {
                    "element": captures["element"][idx],
                    "kind": int(captures["kind"][idx]),
                    "population_alpha": float(captures["population_alpha"][idx]),
                    "population_beta": float(captures["population_beta"][idx]),
                    "charge": float(captures["charge"][idx]),
                    "spin": float(captures["spin"][idx]),
                }
            )

        return {
            "mulliken_population_analysis": {
                "per-atom": per_atom,
                "total": {
                    "population_alpha": float(captures["total_population_alpha"][0]),
                    "population_beta": float(captures["total_population_beta"][0]),
                    "charge": float(captures["total_charge"][0]),
                    "spin": float(captures["total_spin"][0]),
                },
            }
        }

    # spin-restricted case:
    for idx in range(len(captures["atom"])):
        per_atom.append(
            {
                "element": captures["element"][idx],
                "kind": int(captures["kind"][idx]),
                "population": float(captures["population"][idx]),
                "charge": float(captures["charge"][idx]),
            }
        )

    return {
        "mulliken_population_analysis": {
            "per-atom": per_atom,
            "total": {"population": float(captures["total_population"][0]), "charge": float(captures["total_charge"][0])},
        }
    }
