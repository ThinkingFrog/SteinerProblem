from typing import List, Tuple

import networkx as nx
from networkx.algorithms.tree.mst import minimum_spanning_tree

from steiner.solvers.base_solver import BaseSolver


class SolverKMBBase(BaseSolver):
    def solve(self, graph: nx.Graph, terminals: List[int]) -> Tuple[nx.Graph, int]:
        metric_closure_graph = self._get_induced_metric_closure(graph, terminals)

        steiner_tree = minimum_spanning_tree(metric_closure_graph)
        steiner_tree_cost = self._sum_weight(steiner_tree)

        return steiner_tree, steiner_tree_cost

    def name(self) -> str:
        return "KMB Basic"
