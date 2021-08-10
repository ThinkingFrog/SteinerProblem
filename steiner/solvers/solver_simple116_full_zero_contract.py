import networkx as nx

from steiner.solvers.solver_simple116_full import SolverSimple116Full


class SolverSimple116FullZeroContract(SolverSimple116Full):
    def _contract_edge(self, graph: nx.Graph, node1: int, node2: int) -> nx.Graph:
        contracted_graph = graph.copy()
        contracted_graph[node1][node2]["weight"] = 0

        return contracted_graph

    def name(self) -> str:
        return "Simple 11/6 Full w/ zeroing contraction"
