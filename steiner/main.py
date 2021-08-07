import time
from pathlib import Path

import click
from tqdm import tqdm

from steiner.core.config import Config
from steiner.core.steiner_result import SteinerResult
from steiner.core.stpparser import STPParser
from steiner.core.validator import Validator
from steiner.solvers.solver_kmb_base import SolverKMBBase
from steiner.solvers.solver_kmb_full import SolverKMBFull
from steiner.solvers.solver_simple116_base import SolverSimple116Base


@click.command(name="steiner")
@click.option(
    "--data",
    "-d",
    help="Path to file/dir with graph(s)",
    type=click.Path(
        exists=True, file_okay=True, dir_okay=True, readable=True, path_type=Path
    ),
    default=None,
)
@click.option(
    "--output",
    "-o",
    help="Output directory",
    type=click.Path(
        exists=True, file_okay=True, dir_okay=True, readable=True, path_type=Path
    ),
    default=None,
)
def main(data: Path, output: Path):
    result = SteinerResult()
    config = Config(data)
    parser = STPParser()
    validator = Validator()

    for data in tqdm(config.data()):
        graph_info, graph, terminals = parser.parse(data)

        for solver in [SolverKMBBase(), SolverKMBFull(), SolverSimple116Base()]:
            start_time = time.time()

            steiner_tree, steiner_tree_cost = solver.solve(graph, terminals)

            finish_time = time.time()
            runtime = finish_time - start_time

            is_valid = validator.validate(steiner_tree, terminals)
            result.add(graph_info, solver.name(), steiner_tree_cost, runtime, is_valid)

    result.dump(output)
