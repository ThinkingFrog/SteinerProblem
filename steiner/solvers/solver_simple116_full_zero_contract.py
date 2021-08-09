from typing import Tuple

import networkx as nx

from steiner.solvers.solver_simple116_full import SolverSimple116Full


class SolverSimple116FullZeroContract(SolverSimple116Full):
    def _contract_triple(self, graph: nx.Graph, triple: Tuple[int]) -> nx.Graph:
        contracted_graph = graph.copy()
        contracted_graph[triple[0]][triple[1]]["weight"] = 0
        contracted_graph[triple[0]][triple[2]]["weight"] = 0

        return contracted_graph

    def name(self) -> str:
        return "Simple 11/6 Full w/ zeroing contraction"
