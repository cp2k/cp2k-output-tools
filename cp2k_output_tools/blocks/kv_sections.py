import regex as re

KV_SECTION_RE = re.compile(
    r"""
^\ (
    (?P<section>CP2K|)\|\ (?P<key>cp2kflags)\: \s*(?P<value>.+?) \s*
    |
    (?P<section>CP2K|GLOBAL|DBCSR|DFT|QS)\|\ (?P<key>\s*\w.+?):?\ {2,}(?P<value>.+)
    )
\n
""",
    re.VERBOSE | re.MULTILINE,
)


def match_kv_sections(content):
    result = {}

    subsections = {"dft": ("cutoffs",), "qs": ("multi grid cutoff [a.u.]", "interaction thresholds")}

    for match in KV_SECTION_RE.finditer(content):
        section = match["section"].lower()

        if section not in result:
            result[section] = {}

        key = match["key"].lower()

        if section in subsections and any(key.startswith(k) for k in subsections[section]):
            subsection = next(k for k in subsections[section] if key.startswith(k))
            # if we encounter the cutoffs key in the DFT section we have subkes
            key = key.lstrip(f"{subsection}: ")  # strip the subsection from the key
            result[section][subsection] = {}  # and create a new dict for it
            rpointer = result[section][subsection]  # make sure this (and following values) go into this subdict
        elif key.startswith("   "):
            # if we have an indented keyword it belongs to the subsection started above
            key = key.lstrip()
        else:
            # otherwise we have regular keywords again
            rpointer = result[section]

        value = match["value"]

        if value in ["T", "F"]:
            rpointer[key] = True if value == "T" else False
            continue

        try:
            rpointer[key] = int(value)
            continue
        except ValueError:
            pass

        try:
            rpointer[key] = float(value)
            continue
        except ValueError:
            pass

        rpointer[key] = value

    if not result:
        return None

    return result
