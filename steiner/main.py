from pathlib import Path

import click

from steiner.core.config import Config
from steiner.core.steiner_result import SteinerResult
from steiner.core.stpparser import STPParser
from steiner.solvers.solver_factory import SolverFactory
from steiner.utils.graph import draw_graph


@click.command(name="steiner")
@click.option(
    "--data",
    "-d",
    help="Path to file/dir with graph",
    type=click.Path(exists=True, file_okay=True, dir_okay=True,readable=True, path_type=Path),
    default=None,
)
@click.option(
    "--verbose", "-v", help="Enable more textual output", default=False, is_flag=True,
)
@click.option(
    "--graphics", "-g", help="Enable visual output", default=False, is_flag=True,
)
@click.option(
    "--output", "-o", help="Output directory", type=click.Path(exists=True, file_okay=True, dir_okay=True,readable=True, path_type=Path), default=None
)
def main(data: Path, verbose: bool, graphics: bool, output: Path):
    result = SteinerResult()
    config = Config(data)
    parser = STPParser()
    factory = SolverFactory()

    for data in config.data():
        for solver_name in ["KMB", "11/6"]:
            if verbose:
                print("\nStart graph parsing")

            name, graph, terminals = parser.parse(data)

            if verbose:
                print(f"Parsed graph {name}")
                print(f"Start {solver_name} algorithm")

            if graphics:
                draw_graph(graph, "Original graph")

            solver = factory.get_solver(solver_name)
            steiner_tree, steiner_tree_cost = solver.solve(graph, terminals)

            if verbose:
                print(f"Steiner tree cost is {steiner_tree_cost}")
                print(f"Finish {solver_name} algorithm\n")
            if graphics:
                draw_graph(steiner_tree, "Steiner tree")
            
            result.add(name, solver_name, steiner_tree_cost)

    if verbose:
        result.print()

    result.write_to_csv(output / "result.csv")
    result.write_to_json(output / "result.json")
