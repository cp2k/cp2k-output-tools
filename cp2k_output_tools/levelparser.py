"""This is the level-based parser, allowing to correctly parse arbitrarily nested CP2K output"""

import re
from itertools import chain
from typing import Iterator, Optional

from .blocks.common import Level
from .blocks.geo_opt import match_geo_opt

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


def parse_iter(content: str, start: Optional[int] = 0, end: Optional[int] = 0) -> Iterator[Level]:
    # Since a program can terminate in many ways but only start with a few,
    # let's determine end of a program run output by looking for the beginning of the next.
    # This assumes that we only find output of CP2K in content.
    starts = [match.span()[0] for match in PROG_START_MATCH.finditer(content, start)]
    for start, end in zip(starts, starts[1:] + [None]):
        yield Level(name="prog", data=None, sublevels=chain(match_geo_opt(content, start, end)))
