from itertools import combinations
from typing import List, Tuple

import networkx as nx
from networkx.algorithms.tree.mst import minimum_spanning_tree

from steiner.utils.graph import graph_weight_sum, show_graph


class SolverSimple116:
    def solve(self, graph: nx.Graph, terminals: List[int]) -> Tuple[nx.Graph, int]:
        # Step 1

        w_list = list()

        shortest_paths_graph = self.get_induced_metric_closure(graph, terminals)
        # show_graph(
        #    shortest_paths_graph, "Graph of terminals with paths replaced by shortest"
        #)

        triples = self.get_triples(shortest_paths_graph)
        print(triples)

        # Step 2

        triples_meta_info = self.find_minimizing_v(graph, triples)
        print(triples_meta_info)

        # Step 3

        while True:
            win, triple, meta = self.find_win(
                shortest_paths_graph, triples, triples_meta_info
            )

            if win <= 0:
                break

            shortest_paths_graph = self.contract_triple(shortest_paths_graph, triple)
            # show_graph(shortest_paths_graph, "Graph after contraction")
            w_list.append(meta[0])

        # Step 4

        terminals_w_subgraph = self.get_induced_metric_closure(
            graph, terminals + w_list
        )
        # show_graph(terminals_w_subgraph, "Last subgraph")
        final_mst = minimum_spanning_tree(terminals_w_subgraph)
        final_cost = graph_weight_sum(final_mst)

        return final_mst, final_cost

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

    def contract_triple(self, graph: nx.Graph, triple: Tuple[int]) -> nx.Graph:
        intermediate_contracted_graph = nx.contracted_nodes(
            graph, triple[0], triple[1], self_loops=False
        )
        contracted_graph = nx.contracted_nodes(
            intermediate_contracted_graph, triple[0], triple[2], self_loops=False
        )

        return contracted_graph

    def find_win(
        self,
        graph: nx.Graph,
        triples: List[Tuple[int]],
        triples_metainfo: List[Tuple[int]],
    ) -> Tuple[int, Tuple[int], Tuple[int]]:
        if graph.size() < 4:
            return 0, (0, 0, 0), (0, 0, 0)

        max_win = 0
        max_triple = (0, 0, 0)
        max_triple_meta = (0, 0)

        for tr, meta in zip(triples, triples_metainfo):
            if (
                tr[0] not in list(graph.nodes)
                or tr[1] not in list(graph.nodes)
                or tr[2] not in list(graph.nodes)
            ):
                continue

            graph_mst = minimum_spanning_tree(graph)
            # show_graph(graph_mst, "Shortest paths graph MST")
            graph_mst_cost = graph_weight_sum(graph_mst)

            contracted_graph = self.contract_triple(graph, tr)
            # show_graph(contracted_graph, "Contracted_graph")
            contracted_graph_mst = minimum_spanning_tree(contracted_graph)
            # show_graph(contracted_graph_mst, "Contracted_graph_mst")
            contracted_graph_mst_cost = graph_weight_sum(contracted_graph_mst)

            dz = meta[1]

            win = graph_mst_cost - contracted_graph_mst_cost - dz

            if win > max_win:
                max_win = win
                max_triple = tr
                max_triple_meta = meta

        return max_win, max_triple, max_triple_meta
