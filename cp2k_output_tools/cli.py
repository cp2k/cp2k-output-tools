import json
import os
import pathlib
from io import StringIO

import click
from rich.console import Console
from rich.highlighter import RegexHighlighter, ReprHighlighter
from rich.markup import escape
from rich.syntax import Syntax

from .blocks.common import merged_spans, span_char_count
from .levelparser import parse_all, pretty_print
from .parser import parse_iter_blocks


class FortranNumberHighlighter(RegexHighlighter):
    base_style = "repr."
    highlights = ReprHighlighter.highlights + [r"(?P<number>[\+\-]?(\d*[\.]\d+|\d+[\.]?\d*)([DEe][\+\-]?\d+)?)"]


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
    console = Console(
        force_terminal=True if color == "always" else None,
        highlighter=FortranNumberHighlighter(),
    )
    error_console = Console(force_terminal=True if color == "always" else None, highlighter=FortranNumberHighlighter(), stderr=True)

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

            console.print(f"{path}: {_(ref)}")

        return

    if oformat == "yaml":
        from ruamel.yaml import YAML

        yaml = YAML()
        yaml.indent(mapping=2, sequence=4, offset=2)
        ycontent = StringIO()
        yaml.dump(tree, ycontent)
        syntax = Syntax(ycontent.getvalue(), "yaml")
        console.print(syntax)

    elif oformat == "highlight":
        ptr = 0
        for start, end in spans:
            console.print(
                f"[dim]{escape(content[ptr:start])}[/][bold]{escape(content[start:end])}[/]",
                end="",
            )
            ptr = end
        console.print(f"[dim]{escape(content[ptr:])}[/]")

    else:
        syntax = Syntax(json.dumps(tree, indent=2, sort_keys=True), "json")
        console.print(syntax)

    if statistics:
        error_console.print("Statistics:\n===========\n")
        error_console.print(f"Number of lines:      {len(content.splitlines()):>8}")
        error_console.print(f"Number of characters: {len(content):>8}")
        error_console.print(f"Percentage parsed:    {100*span_char_count(spans)/len(content):>8.2f}")


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
