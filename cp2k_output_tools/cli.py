import json
import os
import pathlib
import sys

import click

from .blocks.common import merged_spans, span_char_count
from .levelparser import parse_all, pretty_print
from .parser import parse_iter_blocks


@click.command()
@click.argument("fhandle", metavar="[FILE|-]", type=click.File(), default="-")
@click.option(
    "-f",
    "--format",
    "oformat",
    type=click.Choice(("json", "yaml", "highlight")),
    default="json",
    help="Output format (json or yaml are structure formats, highlight shows which lines of the output have been matched)",
)
@click.option(
    "--color",
    "color",
    type=click.Choice(("auto", "always")),
    default="auto",
    help="When to colorize output",
)
@click.option("-s", "--safe-keys", is_flag=True, help="generate 'safe' key names (e.g. without spaces, dashes, ..)")
@click.option("-S", "--statistics", is_flag=True, help="print some statistics to stderr")
@click.option("-k", "--key", "paths", metavar="<PATH>", type=str, multiple=True, help="Path, ex.: 'energies/total force_eval'")
@click.option("--experimental", is_flag=True, help="Use the experimental level parser", default=False)
def cp2kparse(fhandle, oformat, color, safe_keys, statistics, paths, experimental):
    """Parse the CP2K output FILE and return a structured output"""

    tree = {}
    spans = []

    content = fhandle.read()

    if experimental:
        tree = parse_all(content)
        for lvl, data in tree.walk():
            pretty_print(data, " " * 4 * (lvl - 1))
        return

    for match in parse_iter_blocks(content, key_mangling=safe_keys):
        tree.update(match.data)
        spans += match.spans

    spans = merged_spans(spans)

    def _(val):
        if isinstance(val, list):
            return ", ".join(str(v) for v in val)

        return val

    if paths:
        assert oformat != "parsed", "When selecting a specific path to output, json or yaml output format has to be used"
        for path in paths:
            sections = path.split("/")
            ref = tree
            for section in sections:
                if isinstance(ref, list):
                    section = int(section)  # if we encounter a list, convert the respective path element
                ref = ref[section]  # exploit Python using references into dicts/lists

            click.echo(f"{path}: {_(ref)}")

        return

    if oformat == "yaml":
        from ruamel.yaml import YAML

        yaml = YAML()
        yaml.dump(tree, sys.stdout)
    elif oformat == "highlight":
        ptr = 0
        for start, end in spans:
            click.secho(content[ptr:start], nl=False, dim=True, color=None if color == "auto" else True)
            click.secho(content[start:end], nl=False, bold=True, color=None if color == "auto" else True)
            ptr = end
        click.secho(content[ptr:], nl=False, dim=True, color=None if color == "auto" else True)

    else:
        click.echo(json.dumps(tree, indent=2, sort_keys=True))

    if statistics:
        click.echo("Statistics:\n===========\n", err=True)
        click.echo(f"Number of lines:      {len(content.splitlines()):>8}", err=True)
        click.echo(f"Number of characters: {len(content):>8}", err=True)
        click.echo(f"Percentage parsed:    {100*span_char_count(spans)/len(content):>8.2f}", err=True)


@click.command()
@click.argument("fhandle", metavar="[BANDSTRUCTURE_FILE|-]", type=click.File(), default="-")
@click.option(
    "-p",
    "--output-pattern",
    type=str,
    help="The output pattern for the different set files",
    default="{bsfile_basename}.set-{setnr}.csv",
    show_default=True,
)
@click.option(
    "-C",
    "--output-dir",
    type=click.Path(exists=True, file_okay=False, writable=True, path_type=pathlib.Path),
    help="Directory in which to create the CSV files",
    default=".",
    show_default=True,
)
def cp2k_bs2csv(fhandle, output_pattern, output_dir):
    """
    Convert the input from the given BANDSTRUCTURE_FILE (or stdin) and write
    CSV output files based on the given pattern.
    """
    from cp2k_output_tools.bandstructure_parser import set_gen

    content = fhandle.read()

    for setnr, npoints, _, specialpoints, points in set_gen(content):
        filename = output_pattern.format(bsfile_basename=os.path.basename(fhandle.name), setnr=setnr)

        print(f"writing point set {filename} (total number of k-points: {npoints})")
        with output_dir.joinpath(filename).open("w") as csvout:
            print("with the following special points:")

            for point in specialpoints:
                print(f"  {point.name:>8}: {point.a:10.8f} / {point.b:10.8f} / {point.c:10.8f}")

            for point in points:
                csvout.write(f"{point.a:10.8f} {point.b:10.8f} {point.c:10.8f}")
                for value in point.bands:
                    csvout.write(f" {value:10.8f}")
                csvout.write("\n")
