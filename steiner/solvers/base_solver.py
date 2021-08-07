from abc import ABC, abstractmethod
from typing import List, Tuple

import networkx as nx


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
        induced_metric_closure_graph = nx.Graph()

        for term1 in terminals:
            for term2 in terminals:
                if term1 != term2:
                    weight = nx.dijkstra_path_length(graph, term1, term2)
                    induced_metric_closure_graph.add_edge(term1, term2, weight=weight)

        return induced_metric_closure_graph

    def _sum_weight(self, graph: nx.Graph) -> int:
        return sum(cost for src, dest, cost in graph.edges.data("weight"))
