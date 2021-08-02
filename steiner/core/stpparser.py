from pathlib import Path
from typing import List, Tuple

import networkx as nx

from steiner.core.graph_info import GraphInfo


class STPParser:
    def __init__(self) -> None:
        self._eof_mark = "EOF"

        self._edge_mark = "E"
        self._terminal_mark = "T"

        self._name_info_mark = "Name"
        self._cost_info_mark = "Cost"
        self._nodes_info_mark = "Nodes"
        self._edges_info_mark = "Edges"
        self._terminals_info_mark = "Terminals"

    def parse(self, graph_file: Path) -> Tuple[GraphInfo, nx.Graph, List[int]]:
        """Method to parse STP files

        Args:
            graph_file (Path): Path to stp file

        Returns:
            GraphInfo: Info on the graph
            nx.Graph: Resulting networkx.Graph class instance
            List[int]: List of terminal nodes numbers
        """

        graph_info = GraphInfo()
        terminals: List[int] = list()
        graph = nx.Graph()

        with graph_file.open("r") as gf:
            for line in gf:
                if line == self._eof_mark:
                    break

                splitted = [substr.strip() for substr in line.split()]
                if len(splitted) < 2:
                    continue

                if splitted[0] == self._name_info_mark:
                    name = splitted[1]
                    if name[0] == '"' and name[-1] == '"':
                        name = name[1:-1]
                    graph_info.name = name

                if splitted[0] == self._cost_info_mark:
                    graph_info.cost = int(splitted[1])

                if splitted[0] == self._nodes_info_mark:
                    graph_info.nodes = int(splitted[1])

                if splitted[0] == self._edges_info_mark:
                    graph_info.edges = int(splitted[1])

                if splitted[0] == self._terminals_info_mark:
                    graph_info.terminals = int(splitted[1])

                if splitted[0] == self._edge_mark:
                    graph.add_edge(
                        int(splitted[1]), int(splitted[2]), weight=int(splitted[3])
                    )

                if splitted[0] == self._terminal_mark:
                    terminals.append(int(splitted[1]))

        return graph_info, graph, terminals
