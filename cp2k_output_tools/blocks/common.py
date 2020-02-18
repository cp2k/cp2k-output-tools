from collections import namedtuple

# floating point regex
FLOAT = r"[\+\-]?(\d*[\.]\d+|\d+[\.]?\d*)([Ee][\+\-]?\d+)?"

# return value from a matcher function
MatcherResult = namedtuple("MatcherResult", ["values", "span"])
