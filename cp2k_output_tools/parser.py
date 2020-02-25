from typing import List

from .blocks import builtin_matchers
from .blocks.common import safe_string


def _mangled_keys(idict, mangle_func):
    if isinstance(idict, dict):
        return {mangle_func(k): _mangled_keys(v, mangle_func) for k, v in idict.items()}

    if isinstance(idict, list):
        return [_mangled_keys(i, mangle_func) for i in idict]

    return idict


def parse_iter(content: str, matchers: List[callable] = builtin_matchers, key_mangling: bool = False):
    for matcher in matchers:
        match = matcher(content)

        if match:
            if key_mangling:
                yield _mangled_keys(match, safe_string)
            else:
                yield match
