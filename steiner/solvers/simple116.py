from itertools import combinations
from typing import Dict, List, Tuple, Union

import networkx as nx
from networkx.algorithms.approximation.steinertree import metric_closure
from networkx.algorithms.tree.mst import minimum_spanning_tree

from steiner.solvers.base_solver import BaseSolver
from steiner.utils.graph import graph_weight_sum


class SolverSimple116(BaseSolver):
    TRIPLES_META_DATATYPE = List[Dict[str, Union[Tuple[int], int]]]

    def solve(self, graph: nx.Graph, terminals: List[int]) -> Tuple[nx.Graph, int]:
        # Step 1

        induced_metric_closure = self._get_induced_metric_closure(graph, terminals)
        triples = self._get_triples(induced_metric_closure)

        # Step 2

        triples_meta = self._triples_closest_nodes(graph, triples)

        # Step 3

        additional_nodes = list()
        while True:
            win, triple_meta = self._find_win(induced_metric_closure, triples_meta)

            if win <= 0:
                break

            induced_metric_closure = self._contract_triple(
                induced_metric_closure, triple_meta["triple"]
            )
            additional_nodes.append(triple_meta["closest_node"])

        # Step 4

        terminals_additional_subgraph = self._get_induced_metric_closure(
            graph, terminals + additional_nodes
        )
        steiner_tree = minimum_spanning_tree(terminals_additional_subgraph)
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

    def _get_triples(self, graph: nx.Graph) -> List[Tuple[int]]:
        triples = list(combinations(graph.nodes, 3))

        for tr in triples:
            if (
                tr[0] not in graph[tr[1]]
                or tr[0] not in graph[tr[2]]
                or tr[1] not in graph[tr[2]]
            ):
                triples.remove(tr)

        return triples

    def _triples_closest_nodes(
        self, graph: nx.Graph, triples: List[Tuple[int]]
    ) -> TRIPLES_META_DATATYPE:
        triples_meta = list()

        metric_closure_graph = metric_closure(graph)

        for tr in triples:

            min_dist = 0
            min_vertex = 0

            for v in graph.nodes:
                if v in tr:
                    continue

                min_paths_sum = (
                    metric_closure_graph.get_edge_data(v, tr[0])["distance"]
                    + metric_closure_graph.get_edge_data(v, tr[1])["distance"]
                    + metric_closure_graph.get_edge_data(v, tr[2])["distance"]
                )
                if min_dist == 0 or min_paths_sum < min_dist:
                    min_dist = min_paths_sum
                    min_vertex = v

            triples_meta.append(
                {"triple": tr, "closest_node": min_vertex, "dist_to_node": min_dist}
            )

        return triples_meta

    def _contract_triple(self, graph: nx.Graph, triple: Tuple[int]) -> nx.Graph:
        intermediate_contracted_graph = nx.contracted_nodes(
            graph, triple[0], triple[1], self_loops=False
        )
        contracted_graph = nx.contracted_nodes(
            intermediate_contracted_graph, triple[0], triple[2], self_loops=False
        )

        return contracted_graph

    def _find_win(
        self,
        graph: nx.Graph,
        triples_meta: TRIPLES_META_DATATYPE,
    ) -> Tuple[int, TRIPLES_META_DATATYPE]:

        if graph.size() < 4:
            return 0, {"triple": (0, 0, 0), "closest_node": 0, "dist_to_node": 0}

        max_win = 0
        max_triple_meta = {"triple": (0, 0, 0), "closest_node": 0, "dist_to_node": 0}

        for triple in triples_meta:
            tr = triple["triple"]
            node = triple["closest_node"]
            dist = triple["dist_to_node"]

            if (
                tr[0] not in list(graph.nodes)
                or tr[1] not in list(graph.nodes)
                or tr[2] not in list(graph.nodes)
            ):
                continue

            graph_mst = minimum_spanning_tree(graph)
            graph_mst_cost = graph_weight_sum(graph_mst)

            contracted_graph = self._contract_triple(graph, tr)
            contracted_graph_mst = minimum_spanning_tree(contracted_graph)
            contracted_graph_mst_cost = graph_weight_sum(contracted_graph_mst)

            win = graph_mst_cost - contracted_graph_mst_cost - dist

            if win > max_win:
                max_win = win
                max_triple_meta = {
                    "triple": tr,
                    "closest_node": node,
                    "dist_to_node": dist,
                }

        return max_win, max_triple_meta
