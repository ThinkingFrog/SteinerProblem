import click

from pathlib import Path

from steiner.parser import STPParser

@click.command(name="steiner")
@click.option(
    "--file",
    "-f",
    help="Path to file with graph",
    type=click.Path(exists=True, file_okay=True, readable=True, path_type=Path),
    default=None
)
def main(file: Path):
    parser = STPParser()
    graph, terminals, comment = parser.parse(file)
    graph.print()