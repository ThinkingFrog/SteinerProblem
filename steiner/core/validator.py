from typing import List

import networkx as nx
from networkx.algorithms.approximation.steinertree import metric_closure
from networkx.algorithms.tree.recognition import is_tree


class Validator:
    def validate(self, graph: nx.Graph, terminals: List[int]) -> bool:
        return self.is_tree(graph) and self.terminals_reachable(graph, terminals)

    def is_tree(self, graph: nx.Graph) -> bool:
        return is_tree(graph)

    def terminals_reachable(self, graph: nx.Graph, terminals: List[int]) -> bool:
        mc_graph = metric_closure(graph)

        for term1 in terminals:
            for term2 in terminals:
                if term1 != term2 and term2 not in mc_graph[term1]:
                    return False

        return True
