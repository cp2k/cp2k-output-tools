import regex as re

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


def match_program_info(content):
    match = PROGRAM_INFO_START_RE.search(content)

    if not match:
        return None

    keys = match.captures("key")
    values = match.captures("value")

    result = dict(zip([k.lower() for k in keys], values))
    result[match["inkey"].lower()] = "".join(match.captures("invalue"))

    match = PROGRAM_INFO_STOP_RE.search(content)

    if match:
        keys = match.captures("key")
        values = match.captures("value")

        result.update(zip([k.lower() for k in keys], values))
        result[match["inkey"].lower()] = "".join(match.captures("invalue"))

    return {"program info": result}
