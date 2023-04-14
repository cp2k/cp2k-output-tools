import argparse
import contextlib
import mmap
import re
import sys

from .xyz import FRAME_MATCH_REGEX


@contextlib.contextmanager
def mmapped(fhandle):
    fmapped = mmap.mmap(fhandle.fileno(), 0, access=mmap.ACCESS_READ)

    try:
        yield fmapped
    finally:
        fmapped.close()


CP2K_COMMENT_MATCH = re.compile(
    r"""
^[ \t]* i    [ ] = [ \t]+ (?P<iteration> \d+),
 [ \t]* time [ ] = [ \t]+ (?P<time> [\+\-]?  ( \d*[\.]\d+  | \d+[\.]?\d* )  ([Ee][\+\-]?\d+)? ),
 [ \t]* E    [ ] = [ \t]+ (?P<energy> [\+\-]?  ( \d*[\.]\d+  | \d+[\.]?\d* )  ([Ee][\+\-]?\d+)? )
""",
    re.VERBOSE,
)

# this one acts directly on the mmapped byte-like contnet:
FRAME_MATCH = re.compile(FRAME_MATCH_REGEX.encode("utf8"), re.VERBOSE | re.MULTILINE)


def xyz_restart_cleaner():
    parser = argparse.ArgumentParser(description="Clean a trajectory written by CP2K from restarts, discarding discontinued frames")
    parser.add_argument("source", metavar="<source>", type=argparse.FileType("rb"), help="source trajectory file")
    parser.add_argument(
        "output",
        metavar="<output>",
        nargs="?",
        type=argparse.FileType("wb"),
        default=sys.stdout.buffer,
        help="destination trajectory file",
    )

    args = parser.parse_args()

    iteration = -1
    frames_cache = []

    with mmapped(args.source) as content:
        for frame_match in FRAME_MATCH.finditer(content):
            comment_match = CP2K_COMMENT_MATCH.match(frame_match["comment"].decode("utf8"))

            last_iteration = iteration
            iteration = int(comment_match["iteration"])

            if iteration <= last_iteration:
                try:
                    ndrop = next(n for n, (i, f) in enumerate(reversed(frames_cache), start=1) if i < iteration) - 1
                except StopIteration:
                    print(
                        "WARNING: restart point may lie before already flushed frames, please run this again on the generated output",
                        file=sys.stderr,
                    )
                    ndrop = len(frames_cache)

                nflush = len(frames_cache) - ndrop
                print(f"found restart point @{last_iteration}, dropping {ndrop} frames, flushing {nflush}", file=sys.stderr)

                for frame in frames_cache[:-ndrop]:
                    args.output.write(frame[1])

                frames_cache.clear()

            frames_cache.append((iteration, frame_match[0]))

        print(f"flushing remaining {len(frames_cache)} frames", file=sys.stderr)

        for frame in frames_cache:
            args.output.write(frame[1])
