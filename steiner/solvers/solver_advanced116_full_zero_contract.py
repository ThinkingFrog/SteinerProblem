import networkx as nx

from steiner.solvers.solver_advanced116_full import SolverAdvanced116Full


class SolverAdvanced116FullZeroContract(SolverAdvanced116Full):
    def _contract_edge(self, graph: nx.Graph, node1: int, node2: int) -> nx.Graph:
        contracted_graph = graph.copy()
        try:
            contracted_graph[node1][node2]["weight"] = 0
            contracted_graph[node1][node2]["distance"] = 0
        except BaseException:
            pass

        return contracted_graph

    def name(self) -> str:
        return "Advanced 11/6 Full w/ zeroing contraction"
