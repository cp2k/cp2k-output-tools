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
    args = parser.parse_args()

    tree = {}

    for match in parse_iter(args.file.read()):
        tree.update(match)

    if args.yaml:
        from ruamel.yaml import YAML

        yaml = YAML()

        yaml.dump(tree, sys.stdout)
    else:
        print(json.dumps(tree, indent=2, sort_keys=True))
