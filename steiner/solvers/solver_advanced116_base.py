from collections import defaultdict
from typing import Dict, List, Tuple, Union

import networkx as nx
from networkx.algorithms.approximation.steinertree import metric_closure
from networkx.algorithms.components import connected_components
from networkx.algorithms.tree.mst import minimum_spanning_tree

from steiner.solvers.solver_simple116_base import SolverSimple116Base


class SolverAdvanced116Base(SolverSimple116Base):
    TRIPLES_META_DATATYPE = List[Dict[str, Union[Tuple[int], int]]]

    def solve(self, graph: nx.Graph, terminals: List[int]) -> Tuple[nx.Graph, int]:
        # Step 1

        induced_metric_closure = self._get_induced_metric_closure(graph, terminals)
        triples = self._get_triples(induced_metric_closure)

        # Step 2

        voronoi_regions = self._voronoi_regions(graph, terminals)

        # Step 3

        triples_meta = self._triples_closest_nodes(graph, triples, voronoi_regions)

        # Step 4

        additional_nodes = list()
        while True:
            imc_mst = minimum_spanning_tree(induced_metric_closure)
            self._save_matrix: Dict[int, Dict[int, int]] = defaultdict(
                lambda: defaultdict(int)
            )
            self._findsave(imc_mst)

            win, triple_meta = self._find_win(
                induced_metric_closure, triples_meta, self._save_matrix
            )

            if win <= 0:
                break

            induced_metric_closure = self._contract_triple(
                induced_metric_closure, triple_meta["triple"]
            )
            additional_nodes.append(triple_meta["closest_node"])

        # Step 5

        terminals_additional_subgraph = self._get_induced_metric_closure(
            graph, terminals + additional_nodes
        )
        steiner_tree = minimum_spanning_tree(terminals_additional_subgraph)
        steiner_tree_cost = self._sum_weight(steiner_tree)

        return steiner_tree, steiner_tree_cost

    def name(self) -> str:
        return "Advanced 11/6 Basic"

    def save(self, graph: nx.Graph, node1: int, node2: int) -> int:
        return minimum_spanning_tree(graph) - minimum_spanning_tree(
            self._contract_edge(graph, node1, node2)
        )

    def _findsave(self, graph: nx.Graph) -> None:
        gc = graph.copy()

        if gc.number_of_edges() < 1:
            return

        max_edge = (0, 0)
        max_edge_len = 0

        for src, dest, edata in graph.edges(data=True):
            if max(edata["weight"], edata["distance"]) > max_edge_len or max_edge == (0,0):
                max_edge_len = max(edata["weight"], edata["distance"])
                max_edge = (src, dest)

        gc.remove_edge(max_edge[0], max_edge[1])
        T1_nodes, T2_nodes = connected_components(gc)
        T1 = gc.subgraph(T1_nodes).copy()
        T2 = gc.subgraph(T2_nodes).copy()
        for node1 in T1:
            for node2 in T2:
                self._save_matrix[node1][node2] = self._save_matrix[node2][node1] = max_edge_len

        self._findsave(T1)
        self._findsave(T2)

    def _voronoi_regions(
        self, graph: nx.Graph, terminals: List[int]
    ) -> Dict[int, List[int]]:
        voronoi_regions = defaultdict(list)
        mc_graph = metric_closure(graph)
        nodes_closest_terminals = dict()

        for node in graph.nodes:
            if node in terminals:
                continue
            closest_term_dist = 0
            closest_term = 0
            for term in terminals:
                if (
                    closest_term_dist == 0
                    or mc_graph[term][node]["distance"] < closest_term_dist
                ):
                    closest_term_dist = mc_graph[term][node]["distance"]
                    closest_term = term
            nodes_closest_terminals[node] = closest_term

        for node, term in nodes_closest_terminals.items():
            voronoi_regions[term].append(node)
            
        for term in terminals:
            voronoi_regions[term].append(term)

        # Double check that voronoi regions are correct
        checked_nodes = list()
        for l in voronoi_regions.values():
            for node in l:
                if node in checked_nodes:
                    raise ValueError("Some nodes in voronoi region are duplicated")
                checked_nodes.append(node)
        for node in graph.nodes:
            if node not in checked_nodes:
                raise ValueError("Not all graph nodes are in voronoi regions")

        return voronoi_regions

    def _triples_closest_nodes(
        self,
        graph: nx.Graph,
        triples: List[Tuple[int]],
        voronoi_regions: Dict[int, List[int]],
    ) -> TRIPLES_META_DATATYPE:
        triples_meta = list()

        metric_closure_graph = metric_closure(graph)
        for node in metric_closure_graph.nodes:
            metric_closure_graph.add_edge(node, node, distance=0)

        for tr in triples:

            min_dist = 0
            min_vertex = 0

            if (
                voronoi_regions[tr[0]] + voronoi_regions[tr[1]] + voronoi_regions[tr[2]]
                == []
            ):
                raise ValueError("Triple has empty union")

            for v in (
                voronoi_regions[tr[0]] + voronoi_regions[tr[1]] + voronoi_regions[tr[2]]
            ):
                min_paths_sum = (
                        metric_closure_graph.get_edge_data(v, tr[0])["distance"]
                        + metric_closure_graph.get_edge_data(v, tr[1])["distance"]
                        + metric_closure_graph.get_edge_data(v, tr[2])["distance"]
                )
                if min_dist == 0 or min_paths_sum <= min_dist:
                    min_dist = min_paths_sum
                    min_vertex = v

            triples_meta.append(
                {"triple": tr, "closest_node": min_vertex, "dist_to_node": min_dist}
            )

        return triples_meta

    def _find_win(
        self,
        graph: nx.Graph,
        triples_meta: TRIPLES_META_DATATYPE,
        save_matrix: Dict[int, Dict[int, int]],
    ) -> Tuple[int, TRIPLES_META_DATATYPE]:

        if graph.size() < 4:
            return 0, {"triple": (0, 0, 0), "closest_node": 0, "dist_to_node": 0}

        max_win = 0
        max_triple_meta = {"triple": (0, 0, 0), "closest_node": 0, "dist_to_node": 0}

        for triple in triples_meta:
            tr = triple["triple"]
            node = triple["closest_node"]
            dist = triple["dist_to_node"]

            if (
                tr[0] not in list(graph.nodes)
                or tr[1] not in list(graph.nodes)
                or tr[2] not in list(graph.nodes)
            ):
                continue

            save_list = [
                save_matrix[tr[0]][tr[1]],
                save_matrix[tr[0]][tr[2]],
                save_matrix[tr[1]][tr[2]],
            ]

            win = max(save_list) + min(save_list) - dist

            if win > max_win:
                max_win = win
                max_triple_meta = {
                    "triple": tr,
                    "closest_node": node,
                    "dist_to_node": dist,
                }

        return max_win, max_triple_meta
