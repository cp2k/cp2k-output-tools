import regex as re

KV_SECTION_RE = re.compile(
    r"""
^\ (?P<section>
    CP2K|GLOBAL|DBCSR
    )\|\ (?P<key>.+?):?\ {2,}(?P<value>.+)\n
""",
    re.VERBOSE | re.MULTILINE,
)


def match_kv_sections(content):
    result = {}

    for match in KV_SECTION_RE.finditer(content):
        section = match["section"].lower()

        if section not in result:
            result[section] = {}

        result[section][match["key"].lower()] = match["value"]

    if not result:
        return None

    return result
