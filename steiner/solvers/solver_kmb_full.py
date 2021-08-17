from typing import List, Tuple

import networkx as nx

from steiner.solvers.solver_kmb_base import SolverKMBBase


class SolverKMBFull(SolverKMBBase):
    def solve(self, graph: nx.Graph, terminals: List[int]) -> Tuple[nx.Graph, int]:
        metric_closure_mst_graph, _ = super().solve(graph, terminals)

        steiner_tree, steiner_tree_cost = self._optimize_result(
            graph, metric_closure_mst_graph, terminals
        )

        return steiner_tree, steiner_tree_cost

    def name(self) -> str:
        return "KMB Full"
