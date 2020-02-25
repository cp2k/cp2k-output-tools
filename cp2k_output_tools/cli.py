import argparse
import json
import sys

from .parser import parse_iter


def cp2kparse():
    parser = argparse.ArgumentParser(description="Parse the CP2K output file and return a JSON")
    parser.add_argument(
        "file",
        metavar="<file>",
        nargs="?",
        type=argparse.FileType("r"),
        default=sys.stdin,
        help="CP2K output file, stdin if not specified",
    )
    parser.add_argument("-y", "--yaml", action="store_true", help="output yaml instead of json")
    parser.add_argument(
        "-s", "--safe-keys", action="store_true", help="generate 'safe' key names (e.g. without spaces, dashes, ..)"
    )
    parser.add_argument(
        "-k", "--key", dest="paths", metavar="<path>", type=str, action="append", help="Path, ex.: 'energies/total force_eval'"
    )
    args = parser.parse_args()

    tree = {}

    for match in parse_iter(args.file.read(), key_mangling=args.safe_keys):
        tree.update(match)

    def _(val):
        if isinstance(val, list):
            return ", ".join(str(v) for v in val)

        return val

    if args.paths:
        for path in args.paths:
            sections = path.split("/")
            ref = tree
            for section in sections:
                if isinstance(ref, list):
                    section = int(section)  # if we encounter a list, convert the respective path element
                ref = ref[section]  # exploit Python using references into dicts/lists

            print(f"{path}: {_(ref)}")

        return

    if args.yaml:
        from ruamel.yaml import YAML

        yaml = YAML()

        yaml.dump(tree, sys.stdout)
    else:
        print(json.dumps(tree, indent=2, sort_keys=True))
