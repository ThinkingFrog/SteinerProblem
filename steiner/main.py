from pathlib import Path

import click

from steiner.core.config import Config
from steiner.core.steiner_result import SteinerResult
from steiner.core.stpparser import STPParser
from steiner.solvers.simple116 import SolverSimple116
from steiner.utils.graph import draw_graph


@click.command(name="steiner")
@click.option(
    "--data",
    "-d",
    help="Path to file/dir with graph",
    type=click.Path(exists=True, file_okay=True, readable=True, path_type=Path),
    default=None,
)
@click.option(
    "--verbose", "-v", help="Enable more textual output", default=False, is_flag=True,
)
@click.option(
    "--graphics", "-g", help="Enable visual output", default=False, is_flag=True,
)
def main(data: Path, verbose: bool, graphics: bool):
    result = SteinerResult()
    config = Config(data)
    parser = STPParser()

    for data in config.data():
        if verbose:
            print("\nStart graph parsing")

        name, graph, terminals = parser.parse(data)

        if verbose:
            print(f"Parsed graph {name}")
            print("Start 11/6 algorithm")

        if graphics:
            draw_graph(graph, "Original graph")

        solver = SolverSimple116()
        final_tree, final_cost = solver.solve(graph, terminals)

        if verbose:
            print("Finish 11/6 algorithm")
            print(f"Steiner tree cost is {final_cost}\n")

        if graphics:
            draw_graph(final_tree, "Steiner tree")

        result.add(name, "11/6", final_cost)

    result.print()
    result.write_to_csv(Path("result.csv"))
    result.write_to_json(Path("result.json"))
