from typing import Optional

import regex as re

from .common import BlockMatch

DOI_RE = re.compile(r"^\s*\Khttps?://doi\.org/[^\s]+$", re.MULTILINE | re.VERSION1)


def match_bibliography(content: str) -> Optional[BlockMatch]:
    """Currently we only match the DOIs, but any decent bibliography manager can resolve this metadata"""

    bibliography = []
    spans = []

    for match in DOI_RE.finditer(content):
        bibliography.append({"doi": match[0]})
        spans += match.spans(0)

    if not bibliography:
        return None

    return BlockMatch({"bibliography": bibliography}, spans)
