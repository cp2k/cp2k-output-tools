import contextlib
import mmap
import re
from collections.abc import Iterator

__all__ = ["parse", "parse_iter", "BlockIterator"]


@contextlib.contextmanager
def as_byteorstringlike(fh_or_content):
    """
    Yields a tuple (content, content_type),
    where content_type is True if content is a unicode string,
    and False if it is a byte-like (and needs to be decoded).
    """

    if isinstance(fh_or_content, str):
        yield fh_or_content, True
    elif isinstance(fh_or_content, bytes):
        yield fh_or_content, False
    else:
        # if the handle is a file handle, use mmap to return a byte-like object
        mmapped = mmap.mmap(fh_or_content.fileno(), 0, access=mmap.ACCESS_READ)

        try:
            yield mmapped, False
        finally:
            mmapped.close()


# MULTILINE and VERBOSE regex to match coordinate lines in a frame:
POS_MATCH_REGEX = r"""
^                                                               # Linestart
[ \t]*                                                          # Optional white space
(?P<sym>[A-Za-z]+[A-Za-z0-9]*)\s+                               # get the symbol
(?P<x> [\-\+]? (\d*\.\d+|\d+\.?\d*) ([Ee][\+\-]?\d+)? ) [ \t]+  # Get x
(?P<y> [\-\+]? (\d*\.\d+|\d+\.?\d*) ([Ee][\+\-]?\d+)? ) [ \t]+  # Get y
(?P<z> [\-\+]? (\d*\.\d+|\d+\.?\d*) ([Ee][\+\-]?\d+)? )         # Get z
"""

# MULTILINE and VERBOSE regex to match frames:
FRAME_MATCH_REGEX = r"""
                                        # First line contains an integer
                                        # and only an integer: the number of atoms
^[ \t]* (?P<natoms> [0-9]+) [ \t]*[\n]  # End first line
(?P<comment>.*) [\n]                    # The second line is a comment
(?P<positions>                          # This is the block of positions
    (
        (
            \s*                         # White space in front of the element spec is ok
            (
                [A-Za-z]+[A-Za-z0-9]*   # Element spec
                (
                   \s+                  # White space in front of the number
                   [\-\+]?              # Plus or minus in front of the number (optional)
                   (\d*                 # optional decimal in the beginning .0001 is ok, for example
                    \.                  # There has to be a dot followed by
                    \d+)                # at least one decimal
                    |                   # OR
                   (\d+                 # at least one decimal, followed by
                    \.?                 # an optional dot
                    \d*)                # followed by optional decimals
                   ([Ee][\+\-]?\d+)?    # optional exponents E+03, e-05
                ){3}                    # I expect three float values
                |
                \#                      # If a line is commented out, that is also ok
            )
            .*                          # I do not care what is after the comment or the position spec
            |                           # OR
            \s*                         # A line only containing white space
         )
        [\n]                            # line break at the end
    )+
)                                       # A positions block should be one or more lines
"""


class BlockIterator(Iterator):
    """
    A iterator for wrapping the iterator returned by `match.finditer`
    to extract the required fields directly from the match object
    """

    def __init__(self, it, natoms):
        self._it = it
        self._natoms = natoms
        self._catom = 0

    def __next__(self):
        try:
            match = next(self._it)
        except StopIteration:
            # if we reached the number of atoms declared, everything is well
            # and we re-raise the StopIteration exception
            if self._catom == self._natoms:
                raise
            else:
                # otherwise we got too less entries
                raise ValueError(
                    f"Number of atom entries {self._catom} is smaller than the number of atoms {self._natoms}"
                ) from None

        self._catom += 1

        if self._catom > self._natoms:
            raise TypeError(f"Number of atom entries {self._catom} is larger than the number of atoms {self._natoms}")

        return (match["sym"], (float(match["x"]), float(match["y"]), float(match["z"])))


def parse_iter(fh_or_string):
    """Generates nested tuples for frames in XYZ files.

    Args:
        string: a string containing XYZ-structured text

    Yields:
        tuple: `(natoms, comment, atomiter)` for each frame
        in the XYZ data where `atomiter` is an iterator yielding a
        nested tuple `(symbol, (x, y, z))` for each entry.

    Raises:
        TypeError: If the number of atoms specified for the frame does not match
            the number of atom entries in the file.

    Examples:
        >>> print(len(list(parse_iter('''
        ... 5
        ... no comment
        ...  C         5.0000000000        5.0000000000        5.0000000000
        ...  H         5.6401052216        5.6401052216        5.6401052216
        ...  H         4.3598947806        4.3598947806        5.6401052208
        ...  H         4.3598947806        5.6401052208        4.3598947806
        ...  H         5.6401052208        4.3598947806        4.3598947806
        ... 5
        ... no comment
        ...  C         5.0000000000        5.0000000000        5.0000000000
        ...  H         5.6401902064        5.6401902064        5.6401902064
        ...  H         4.3598097942        4.3598097942        5.6401902063
        ...  H         4.3598097942        5.6401902063        4.3598097942
        ...  H         5.6401902063        4.3598097942        4.3598097942
        ... 5
        ... no comment
        ...  C         5.0000000000        5.0000000000        5.0000000000
        ...  H         5.6401902064        5.6401902064        5.6401902064
        ...  H         4.3598097942        4.3598097942        5.6401902063
        ...  H         4.3598097942        5.6401902063        4.3598097942
        ...  H         5.6401902063        4.3598097942        4.3598097942
        ... '''))))
        3
    """

    with as_byteorstringlike(fh_or_string) as (content, is_string):
        if is_string:
            frame_match = re.compile(FRAME_MATCH_REGEX, re.MULTILINE | re.VERBOSE)
            pos_match = re.compile(POS_MATCH_REGEX, re.MULTILINE | re.VERBOSE)
        else:
            frame_match = re.compile(FRAME_MATCH_REGEX.encode("utf8"), re.MULTILINE | re.VERBOSE)
            pos_match = re.compile(POS_MATCH_REGEX.encode("utf8"), re.MULTILINE | re.VERBOSE)

        for block in frame_match.finditer(content):
            natoms = int(block["natoms"])
            yield (
                natoms,
                block["comment"] if is_string else block["comment"].decode("utf8"),
                BlockIterator(pos_match.finditer(block["positions"]), natoms),
            )


def parse(fh_or_string):
    """
    The same as parse_iter(...) but instead of iterators, a list of nested dicts containing again
    a list for the 'atoms' key instead of another iterator are returned.
    """
    return [
        {"natoms": natoms, "comment": comment, "atoms": list(atomiter)} for (natoms, comment, atomiter) in parse_iter(fh_or_string)
    ]
