from typing import List, Tuple

import networkx as nx

from steiner.solvers.solver_advanced116_base import SolverAdvanced116Base


class SolverAdvanced116Full(SolverAdvanced116Base):
    def solve(self, graph: nx.Graph, terminals: List[int]) -> Tuple[nx.Graph, int]:
        metric_closure_mst_graph, _ = super().solve(graph, terminals)

        steiner_tree, steiner_tree_cost = self._optimize_result(
            graph, metric_closure_mst_graph, terminals
        )

        return steiner_tree, steiner_tree_cost

    def name(self) -> str:
        return "Advanced 11/6 Full"
