import datetime
import pathlib
from dataclasses import dataclass
from typing import Optional, Union

import regex as re

from .common import BlockMatch

PROGRAM_INFO_START_RE = re.compile(
    r"""
(^[\* ]{14,}
\ PROGRAM\ (?P<key>
        (?:STARTED\ (?:AT|ON|BY))|
        PROCESS\ ID|
        )
    \s+
    (?P<value>.+)
    \n
    ){4}

[\* ]{14,}
\ PROGRAM\ (?P<inkey>(?:STARTED\ IN))
    \s+
    (?P<invalue>.+)
    \n
(\ \s{42}(?P<invalue>.+)\n)*
""",
    re.VERSION1 | re.VERBOSE | re.MULTILINE,
)


PROGRAM_INFO_STOP_RE = re.compile(
    r"""
(^[\* ]{14,}
\ PROGRAM\ (?P<key>
        ENDED\ AT|
        (?:RAN\ (?:ON|BY))|
        PROCESS\ ID|
        )
    \s+
    (?P<value>.+)
    \n
    ){4}

[\* ]{14,}
\ PROGRAM\ (?P<inkey>(?:STOPPED\ IN))
    \s+
    (?P<invalue>.+)
    \n
(\ \s{42}(?P<invalue>.+)\n)*
""",
    re.VERSION1 | re.VERBOSE | re.MULTILINE,
)


@dataclass
class ProgramInfo:
    started_at: datetime.datetime
    started_on: str
    started_by: str
    process_id: int
    started_in: pathlib.Path
    ended_at: Optional[datetime.datetime] = None
    ran_on: Optional[str] = None
    ran_by: Optional[str] = None
    stopped_in: Optional[pathlib.Path] = None


def match_program_info(content: str, start=0, end=0, as_tree_obj: bool = False) -> Optional[Union[BlockMatch, ProgramInfo]]:
    spans = []
    match = PROGRAM_INFO_START_RE.search(content, start, end)

    if not match:
        return None

    keys = match.captures("key")
    values = match.captures("value")

    result = dict(zip([k.lower() for k in keys], values))
    result[match["inkey"].lower()] = "".join(match.captures("invalue"))
    spans += match.spans(0)

    match = PROGRAM_INFO_STOP_RE.search(content, start, end)

    if match:
        keys = match.captures("key")
        values = match.captures("value")

        result.update(zip([k.lower() for k in keys], values))
        result[match["inkey"].lower()] = "".join(match.captures("invalue"))
        spans += match.spans(0)

    if as_tree_obj:
        result = {k.replace(" ", "_"): v for k, v in result.items()}
        result["process_id"] = int(result["process_id"])
        result["started_at"] = datetime.datetime.fromisoformat(result["started_at"])
        try:
            result["ended_at"] = datetime.datetime.fromisoformat(result["ended_at"])
        except KeyError:
            pass  # didn't finish properly, ignore it
        return ProgramInfo(**result)

    return BlockMatch({"program info": result}, spans)
