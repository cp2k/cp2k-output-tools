from dataclasses import dataclass
from typing import Any, Dict, Iterator, Optional

import regex as re

from .common import BlockMatch

WARNING_MESSAGE_RE = re.compile(
    r"""
^\ \*{3}\ WARNING\ in\ (?<filename>[^:]+):(?P<line>\d+)\ ::\ (?P<message>.+?) \*{3} \n
(\ \*{3}\ (?P<message>.+?) \*{3} \n)*
""",
    re.VERSION1 | re.VERBOSE | re.MULTILINE,
)

WARNING_MESSAGE_SIRIUS_RE = re.compile(
    r"""
^===\ (?P<type>Warning|Fatal\ error)\ at\ line\ (?P<line>\d+)\ of\ file\ (?P<filename>.+?)\ ===\n
(?P<message>.+) \n
(?:(?P<details>.+) \n)*
""",
    re.VERSION1 | re.VERBOSE | re.MULTILINE,
)

TOTAL_WARNING_COUNT_RE = re.compile(
    r"""
^\ The\ number\ of\ warnings\ for\ this\ run\ is\ :\s* (?P<value>\d+)
""",
    re.VERBOSE | re.MULTILINE,
)

ABORT_RE = re.compile(
    r"""
^\ \*+\n
(?:\ \*.+\n)+
(?:\ \*\ \[ABORT\]\ +\*\n)
(?:\ \*.{7} \s* (?P<message>.+?)\s*\*\n)+
\ \*\ /\ \\ \s* (?P<filename>[^:]+):(?P<line>\d+) \ \*\n  # match the feet of the figure to get the location of the abort
\ \*+\n
""",
    re.VERBOSE | re.MULTILINE,
)


@dataclass
class Message:
    type: str
    message: str
    details: Optional[str]
    component: str
    filename: str
    line: int


def match_warnings(content: str) -> Optional[BlockMatch]:
    result: Dict[str, Any] = {"warnings": []}
    spans = []

    for wmatch in WARNING_MESSAGE_RE.finditer(content):
        result["warnings"] += [
            {"filename": wmatch["filename"], "line": int(wmatch["line"]), "message": "".join(wmatch.captures("message")).rstrip()}
        ]
        spans += wmatch.spans(0)

    match = TOTAL_WARNING_COUNT_RE.search(content)
    if match:
        result["nwarnings"] = int(match["value"])
        spans += match.spans(0)

    for wmatch in WARNING_MESSAGE_SIRIUS_RE.finditer(content):
        msg = {"filename": wmatch["filename"], "line": int(wmatch["line"]), "message": wmatch["message"].strip()}
        if wmatch.captures("details"):
            msg["details"] = [d.strip() for d in wmatch.captures("details")]

        if wmatch["type"] == "Warning":
            result["warnings"].append(msg)
            result.setdefault("nwarnings", 0)
            result["nwarnings"] += 1
        elif wmatch["type"] == "Fatal error":
            assert "error" not in result, "multiple fatal errors found when parsing SIRIUS warnings"
            result["error"] = msg
        else:
            raise AssertionError("invalid type found when parsing SIRIUS warnings")

        spans += wmatch.spans(0)

    return BlockMatch(result, spans)


def match_messages(content: str, start: int = 0, end: int = 0) -> Iterator[Message]:
    for match in WARNING_MESSAGE_RE.finditer(content, start, end):
        yield Message(
            type="warning",
            message="".join(match.captures("message")).rstrip(),
            details=None,
            component="CP2K",
            filename=match["filename"],
            line=int(match["line"]),
        )

    for match in ABORT_RE.finditer(content, start, end):
        yield Message(
            type="abort",
            message=" ".join(m.strip() for m in match.captures("message") if m.strip()),
            details=None,
            component="CP2K",
            filename=match["filename"],
            line=int(match["line"]),
        )

    for match in WARNING_MESSAGE_SIRIUS_RE.finditer(content):
        yield Message(
            type=match["type"].lower(),
            message=match["message"].strip(),
            details=match.captures("details").strip() if match.captures("details") else None,
            component="SIRIUS",
            filename=match["filename"],
            line=int(match["line"]),
        )
