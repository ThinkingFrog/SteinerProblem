from pathlib import Path

import click

from steiner.parser import STPParser
from steiner.solvers.kmb import SolverKMB
from steiner.utils.print_graph import print_graph


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
    print("Parsed graph:")
    print_graph(graph)
    print(f"Parsed terminals are: {terminals}")

    print("Start KMB algorithm")
    solver = SolverKMB()
    final_tree, final_cost = solver.solve(graph, terminals)
