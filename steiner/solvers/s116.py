from itertools import combinations
from typing import List, Tuple

import networkx as nx
import networkx.algorithms.approximation.steinertree as nxaas
import networkx.algorithms.tree.mst as nxatm
import networkx.classes.function as nxcf

from steiner.utils.graph import show_graph


class Solver116:
    def solve(self, graph: nx.Graph, terminals: List[int]) -> Tuple[nx.Graph, int]:
        shortest_paths_graph = self.get_induced_metric_closure(graph, terminals)
        show_graph(
            shortest_paths_graph, "Graph of terminals with paths replaced by shortest"
        )

        triples = self.get_triples(shortest_paths_graph)
        print(triples)

        min_vs = self.find_minimizing_v(shortest_paths_graph, triples)
        print(min_vs)

        return None, None

    def get_induced_metric_closure(
        self, graph: nx.Graph, terminals: List[int]
    ) -> nx.Graph:
        induced_metric_closure_graph = nx.Graph()

        for term1 in terminals:
            for term2 in terminals:
                if term1 != term2:
                    weight = nx.dijkstra_path_length(graph, term1, term2)
                    induced_metric_closure_graph.add_edge(term1, term2, weight=weight)

        return induced_metric_closure_graph

    def get_triples(self, graph: nx.Graph) -> List[Tuple[int]]:
        triples = list(combinations(graph.nodes, 3))

        for tr in triples:
            if (
                tr[0] not in graph[tr[1]]
                or tr[0] not in graph[tr[2]]
                or tr[1] not in graph[tr[2]]
            ):
                triples.remove(tr)

        return triples

    def find_minimizing_v(
        self, graph: nx.Graph, triples: List[Tuple[int]]
    ) -> List[Tuple[int]]:
        minimizing_vs = list()

        for tr in triples:

            min_dist = 0
            min_vertex = 0

            for v in graph.nodes:
                if v in tr:
                    continue

                min_paths_sum = (
                    nx.dijkstra_path_length(graph, v, tr[0])
                    + nx.dijkstra_path_length(graph, v, tr[1])
                    + nx.dijkstra_path_length(graph, v, tr[2])
                )
                if min_dist == 0 or min_paths_sum < min_dist:
                    min_dist = min_paths_sum
                    min_vertex = v

            minimizing_vs.append((min_vertex, min_dist))

        return minimizing_vs
