from .blocks import available_matchers


def parse_iter(content, matchers=available_matchers):
    def _resolve_matcher(obj):
        if isinstance(obj, str):
            # if a matcher is a string, look it up in our registry of matchers
            return obj, available_matchers[obj]

        # if not we assume it is a callable/function with a specific name
        return obj.__name__, obj

    for mname, mfunc in [_resolve_matcher(m) for m in matchers]:
        match = mfunc(content)

        if match:
            yield (mname, match.values)
