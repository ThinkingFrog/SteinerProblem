from abc import ABC, abstractmethod
from typing import List, Tuple

import networkx as nx
from networkx.algorithms.approximation.steinertree import metric_closure
from networkx.algorithms.traversal.depth_first_search import dfs_postorder_nodes
from networkx.algorithms.tree.mst import minimum_spanning_tree
from networkx.classes.function import induced_subgraph


class BaseSolver(ABC):
    @abstractmethod
    def solve(self, graph: nx.Graph, terminals: List[int]) -> Tuple[nx.Graph, int]:
        pass

    @abstractmethod
    def name(self) -> str:
        pass

    def _get_induced_metric_closure(
        self, graph: nx.Graph, terminals: List[int]
    ) -> nx.Graph:
        mc_graph = metric_closure(graph)
        induced_mc_graph = induced_subgraph(mc_graph, terminals)
        for src, dest, edata in induced_mc_graph.edges(data=True):
            edata["weight"] = edata["distance"]
        return induced_mc_graph

    #        induced_metric_closure_graph = nx.Graph()
    #
    #         for term1 in terminals:
    #             for term2 in terminals:
    #                 if term1 != term2:
    #                     weight = nx.dijkstra_path_length(graph, term1, term2)
    #                     induced_metric_closure_graph.add_edge(term1, term2, weight=weight)
    #
    #        return induced_metric_closure_graph

    def _sum_weight(self, graph: nx.Graph) -> int:
        return sum(cost for src, dest, cost in graph.edges.data("weight"))

    def _optimize_result(
        self, original_graph: nx.Graph, mc_graph: nx.Graph, terminals: List[int]
    ) -> Tuple[nx.Graph, int]:
        unfolded_graph = self._unfold_induced_metric_closure(original_graph, mc_graph)

        mst_graph = minimum_spanning_tree(unfolded_graph)

        steiner_tree = self._remove_redundant_nodes(mst_graph, terminals)
        steiner_tree_cost = self._sum_weight(steiner_tree)

        return steiner_tree, steiner_tree_cost

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

    def _remove_redundant_nodes(
        self, graph: nx.Graph, terminals: List[int]
    ) -> nx.Graph:
        redundant_nodes = list()

        for node in dfs_postorder_nodes(graph, terminals[0]):
            valid_neighbours = []

            for n in graph[node]:
                if n not in redundant_nodes:
                    valid_neighbours.append(n)

            if node not in terminals and len(valid_neighbours) == 1:
                redundant_nodes.append(node)

        cleaned_graph: nx.Graph = graph.copy()
        cleaned_graph.remove_nodes_from(redundant_nodes)

        return cleaned_graph
