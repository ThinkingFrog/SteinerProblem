from typing import List, Tuple

import networkx as nx

from steiner.solvers.solver_simple116_base import SolverSimple116Base


class SolverSimple116Full(SolverSimple116Base):
    def solve(self, graph: nx.Graph, terminals: List[int]) -> Tuple[nx.Graph, int]:
        mc_tree, _ = super().solve(graph, terminals)

        steiner_tree, steiner_tree_cost = self._optimize_result(
            graph, mc_tree, terminals
        )

        return steiner_tree, steiner_tree_cost

    def name(self) -> str:
        return "Simple 11/6 Full"
