import networkx as nx

from steiner.solvers.solver_simple116_base import SolverSimple116Base


class SolverSimple116BaseZeroContract(SolverSimple116Base):
    def _contract_edge(self, graph: nx.Graph, node1: int, node2: int) -> nx.Graph:
        contracted_graph = graph.copy()
        contracted_graph[node1][node2]["weight"] = 0

        return contracted_graph

    def name(self) -> str:
        return "Simple 11/6 Basic w/ zeroing contraction"
