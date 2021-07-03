import json
import sys

import click

from .parser import parse_iter
from .blocks.common import merged_spans, span_char_count


@click.command()
@click.argument("fhandle", metavar="[FILE|-]", type=click.File(), default="-")
@click.option(
    "-o",
    "--format",
    "oformat",
    type=click.Choice(("json", "yaml", "highlight")),
    default="json",
    help="Output format (json or yaml are structure formats, highlight shows which lines of the output have been matched)",
)
@click.option("-s", "--safe-keys", is_flag=True, help="generate 'safe' key names (e.g. without spaces, dashes, ..)")
@click.option("-S", "--statistics", is_flag=True, help="print some statistics to stderr")
@click.option("-k", "--key", "paths", metavar="<PATH>", type=str, multiple=True, help="Path, ex.: 'energies/total force_eval'")
def cp2kparse(fhandle, oformat, safe_keys, statistics, paths):
    """Parse the CP2K output FILE and return a structured output"""

    tree = {}
    spans = []

    content = fhandle.read()

    for match in parse_iter(content, key_mangling=safe_keys):
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
            click.secho(content[ptr:start], nl=False, dim=True)
            click.secho(content[start:end], nl=False, bold=True)
            ptr = end
        click.secho(content[ptr:], nl=False, dim=True)

    else:
        click.echo(json.dumps(tree, indent=2, sort_keys=True))

    if statistics:
        click.echo("Statistics:\n===========\n", err=True)
        click.echo(f"Number of lines:      {len(content.splitlines()):>8}", err=True)
        click.echo(f"Number of characters: {len(content):>8}", err=True)
        click.echo(f"Percentage parsed:    {100*span_char_count(spans)/len(content):>8.2f}", err=True)
