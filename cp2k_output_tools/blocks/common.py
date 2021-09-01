from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Iterator, List, Tuple, Union

# floating point regex
FLOAT = r"[\+\-]?(\d*[\.]\d+|\d+[\.]?\d*)([Ee][\+\-]?\d+)?"


# convert possibly problematic characters to underscores
def safe_string(string):
    return (
        string.replace(" ", "_")
        .replace("-", "_")
        .replace("/", "_")
        .replace("[", "_")
        .replace("]", "_")
        .replace(".", "_")
        .replace("|", "_")
        .replace("^", "_")
        .replace("(", "_")
        .replace(")", "_")
        .replace("{", "_")
        .replace("}", "_")
    )


@dataclass
class BlockMatch:
    data: Dict[str, Any]  # the parsed/structured data
    spans: List[Union[int, Tuple[int, int]]]  # start and end character indices of the matches


def merged_spans(spans: List[Tuple[int, int]]):
    merged = [(-1, -1)]

    for start, end in sorted(spans):
        if start > merged[-1][1]:  # if the new start is after the latest end, add a new span
            merged.append((start, end))
        else:  # if not, keep the current start and replace its end
            merged[-1] = (merged[-1][0], max(merged[-1][1], end))

    del merged[0]
    return merged


def span_char_count(spans: List[Tuple[int, int]]):
    return sum(end - start for start, end in spans)


@dataclass
class Level:
    sublevels: List[Level]


@dataclass
class Tree:
    levels: List[Level]

    def walk(self) -> Iterator[Tuple[int, Level]]:
        """Walk the tree, returns a tuple of current level and the level object."""
        stack = self.levels[::-1]
        lvl = [len(self.levels)]

        while stack:
            current = stack.pop()
            yield (len(lvl), current)
            lvl[-1] -= 1

            try:
                stack += current.sublevels[::-1]
                lvl.append(len(current.sublevels))
            except AttributeError:
                pass

            while lvl and lvl[-1] == 0:  # done with the current level?
                lvl.pop()
