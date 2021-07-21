from typing import List

import networkx as nx
import networkx.algorithms.tree.mst as nxatm

from steiner.utils.print_graph import print_graph


class SolverKMB:
    def __init__(self) -> None:
        pass

    def solve(self, graph: nx.Graph, terminals: List[int]) -> nx.Graph:
        shortest_paths_graph = nx.Graph()

        for term1 in terminals:
            for term2 in terminals:
                if term1 != term2:
                    weight = nx.dijkstra_path_length(graph, term1, term2)
                    shortest_paths_graph.add_edge(term1, term2, weight=weight)

        print("Shortest paths graph:")
        print_graph(shortest_paths_graph)

        shortest_paths_graph_mst = nxatm.minimum_spanning_tree(shortest_paths_graph)
        print("Shortest paths graph MST:")
        print_graph(shortest_paths_graph_mst)

        unfolded_shortest_paths_graph_mst = nx.Graph()
        for src, dest, weight in shortest_paths_graph_mst.edges.data("weight"):
            corresponding_path = nx.dijkstra_path(graph, src, dest)
            for node in corresponding_path:
                try:
                    next_node = corresponding_path[corresponding_path.index(node) + 1]
                except IndexError:
                    break

                unfolded_shortest_paths_graph_mst.add_edge(
                    node,
                    next_node,
                    weight=graph.get_edge_data(node, next_node)["weight"],
                )
        print("Unfolded shortest paths graph MST:")
        print_graph(unfolded_shortest_paths_graph_mst)

        final_mst = nxatm.minimum_spanning_tree(unfolded_shortest_paths_graph_mst)
        print("Final MST:")
        print_graph(final_mst)
        final_cost = sum([cost for src, dest, cost in final_mst.edges.data("weight")])
        print(f"Final tree cost is {final_cost}")