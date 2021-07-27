from pathlib import Path

import click

from steiner.parser import STPParser
from steiner.solvers.simple116 import SolverSimple116
from steiner.utils.graph import show_graph


@click.command(name="steiner")
@click.option(
    "--data",
    "-d",
    help="Path to file with graph",
    type=click.Path(exists=True, file_okay=True, readable=True, path_type=Path),
    default=None,
)
def main(data: Path):
    parser = STPParser()
    graph, terminals = parser.parse(data)
    show_graph(graph, "Original graph")
    print(f"Parsed terminals are: {terminals}")

    print("Start 11/6 algorithm")
    solver = SolverSimple116()
    final_tree, final_cost = solver.solve(graph, terminals)
