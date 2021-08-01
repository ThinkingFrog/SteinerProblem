from typing import Dict

from steiner.solvers.base_solver import BaseSolver
from steiner.solvers.kmb import SolverKMB
from steiner.solvers.simple116 import SolverSimple116


class SolverFactory:
    _solvers_dict: Dict[str, BaseSolver]

    def __init__(self) -> None:
        self._solvers_dict = {"KMB": SolverKMB, "11/6": SolverSimple116}

    def get_solver(self, solver_name: str) -> BaseSolver:
        return self._solvers_dict[solver_name]()
