from typing import List

from .blocks import builtin_matchers


def parse_iter(content, matchers: List[callable] = builtin_matchers):
    for matcher in matchers:
        match = matcher(content)

        if match:
            yield match
