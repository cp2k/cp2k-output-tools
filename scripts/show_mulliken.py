#!/usr/bin/env python3

import gzip
import pathlib

import click

from cp2k_output_tools.levelparser import parse_all


@click.command()
@click.argument(
    "cp2k_output_files",
    type=click.Path(exists=True, file_okay=True, dir_okay=False, path_type=pathlib.Path),
    nargs=-1,
    required=True,
)
def main(cp2k_output_files):
    for fpath in cp2k_output_files:
        print(f"{fpath}:")

        if fpath.suffix == ".gz":
            with gzip.open(fpath, "rt") as fhandle:
                content = fhandle.read()
        else:
            content = fpath.read_text()

        tree = parse_all(content)

        try:
            mulliken = tree.levels[0].sublevels[0].mulliken_population_analysis
            for element, moment in zip(mulliken.elements, mulliken.spin_moment):
                print(f"    {element}    {moment}")
        except (AttributeError, IndexError):
            pass


if __name__ == "__main__":
    main()
