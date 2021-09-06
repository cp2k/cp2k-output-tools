#!/usr/bin/env python3

import pathlib

import click
import pandas as pd

from cp2k_output_tools.levelparser import parse_all


@click.command()
@click.argument(
    "cp2k_output_files",
    type=click.Path(exists=True, file_okay=True, dir_okay=False, path_type=pathlib.Path),
    nargs=-1,
    required=True,
)
def main(cp2k_output_files):
    stats = {}

    for fpath in cp2k_output_files:
        tree = parse_all(fpath.read_text())

        print(f"Checking '{fpath}'...")

        entry = [False, False] * 4

        try:
            entry[1] = tree.levels[0].sublevels[0].converged
            entry[0] = True
        except (AttributeError, IndexError):
            pass

        try:
            entry[3] = tree.levels[1].sublevels[0].moments is not None
            entry[2] = True
        except (AttributeError, IndexError):
            pass

        try:
            entry[5] = tree.levels[1].sublevels[1].polarizability_tensor is not None
            entry[4] = True
        except (AttributeError, IndexError):
            pass

        try:
            entry[7] = len(tree.levels[2].sublevels[0].data.frequencies) > 0
            entry[6] = True
        except (AttributeError, IndexError):
            pass

        stats[fpath.name] = entry

    df = pd.DataFrame(
        stats.values(),
        index=stats.keys(),
        columns=(
            "geo.opt. succeeded",
            "geo.opt. converged",
            "SCF succeeded",
            "moments calculated",
            "linres succeeded",
            "pol. tensor calculated",
            "vib.anal. succeeded",
            "vib. anal. completed",
        ),
    )
    df["All OK"] = df.all(axis=1)
    print(df.to_string())
    print(df.sum(axis=0).to_frame("TOTAL").transpose())


if __name__ == "__main__":
    main()
