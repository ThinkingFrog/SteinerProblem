from pathlib import Path

import click

from steiner.core.steiner_result import SteinerResult
from steiner.core.stpparser import STPParser
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
@click.option(
    "--verbose", "-v", help="Enable more output", default=False, is_flag=True,
)
def main(data: Path, verbose: bool):
    result = SteinerResult()

    parser = STPParser()
    name, graph, terminals = parser.parse(data)

    if verbose:
        show_graph(graph, "Original graph")
        print(f"Parsed terminals are: {terminals}")
        print("Start 11/6 algorithm")

    solver = SolverSimple116()
    final_tree, final_cost = solver.solve(graph, terminals)

    result.add(name, "11/6", final_cost)

    # if verbose:
    # show_graph(final_tree, "Final 11/6 graph")
    # print(f"Final cost is {final_cost}")
    result.print()
