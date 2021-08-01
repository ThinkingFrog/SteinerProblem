from typing import List, Tuple

import networkx as nx
from networkx.algorithms.tree.mst import minimum_spanning_tree

from steiner.solvers.base_solver import BaseSolver
from steiner.utils.graph import graph_weight_sum


class SolverKMB(BaseSolver):
    def solve(self, graph: nx.Graph, terminals: List[int]) -> Tuple[nx.Graph, int]:
        metric_closure_graph = self._get_induced_metric_closure(graph, terminals)

        metric_closure_mst_graph = minimum_spanning_tree(metric_closure_graph)

        unfolded_metric_closure_mst_graph = self._unfold_induced_metric_closure(
            graph, metric_closure_mst_graph
        )

        steiner_tree = minimum_spanning_tree(unfolded_metric_closure_mst_graph)
        steiner_tree_cost = graph_weight_sum(steiner_tree)

        return steiner_tree, steiner_tree_cost

    def _get_induced_metric_closure(
        self, graph: nx.Graph, terminals: List[int]
    ) -> nx.Graph:
        induced_metric_closure_graph = nx.Graph()

        for term1 in terminals:
            for term2 in terminals:
                if term1 != term2:
                    weight = nx.dijkstra_path_length(graph, term1, term2)
                    induced_metric_closure_graph.add_edge(term1, term2, weight=weight)

        return induced_metric_closure_graph

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
