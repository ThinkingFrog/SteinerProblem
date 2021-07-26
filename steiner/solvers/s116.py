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
