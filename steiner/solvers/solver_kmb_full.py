from typing import List, Tuple

import networkx as nx
from networkx.algorithms.tree.mst import minimum_spanning_tree

from steiner.solvers.solver_kmb_base import SolverKMBBase


class SolverKMBFull(SolverKMBBase):
    def solve(self, graph: nx.Graph, terminals: List[int]) -> Tuple[nx.Graph, int]:
        metric_closure_mst_graph, _ = super().solve(graph, terminals)

        unfolded_metric_closure_mst_graph = self._unfold_induced_metric_closure(
            graph, metric_closure_mst_graph
        )

        steiner_tree = minimum_spanning_tree(unfolded_metric_closure_mst_graph)
        steiner_tree_cost = self._sum_weight(steiner_tree)

        return steiner_tree, steiner_tree_cost

    def name(self) -> str:
        return "KMB Full"

    def _unfold_induced_metric_closure(
        self, original_graph: nx.Graph, metric_closure_graph: nx.Graph
    ) -> nx.Graph:
        unfolded_graph = nx.Graph()

        for src, dest, weight in metric_closure_graph.edges.data("weight"):
            corresponding_path = nx.dijkstra_path(original_graph, src, dest)
            for node in corresponding_path:
                try:
                    next_node = corresponding_path[corresponding_path.index(node) + 1]
                except IndexError:
                    break

                unfolded_graph.add_edge(
                    node,
                    next_node,
                    weight=original_graph.get_edge_data(node, next_node)["weight"],
                )

        return unfolded_graph
