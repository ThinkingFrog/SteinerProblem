import networkx as nx

from steiner.solvers.solver_advanced116_base import SolverAdvanced116Base


class SolverAdvanced116BaseZeroContract(SolverAdvanced116Base):
    def _contract_edge(self, graph: nx.Graph, node1: int, node2: int) -> nx.Graph:
        contracted_graph = graph.copy()
        contracted_graph[node1][node2]["weight"] = 0

        return contracted_graph

    def name(self) -> str:
        return "Advanced 11/6 Basic w/ zeroing contraction"
