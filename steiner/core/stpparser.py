from pathlib import Path
from typing import List, Tuple

import networkx as nx


class STPParser:
    _eof_mark: str
    _nodes_count_mark: str
    _edge_mark: str
    _terminal_mark: str
    _name_mark: str

    def __init__(self) -> None:
        self._eof_mark = "EOF"
        self._edge_mark = "E"
        self._terminal_mark = "T"
        self._name_mark = "Name"

    def parse(self, graph_file: Path) -> Tuple[str, nx.Graph, List[int]]:
        """Method to parse STP files

        Args:
            graph_file (Path): Path to stp file

        Returns:
            str: Name of the graph
            nx.Graph: Resulting networkx.Graph class instance
            List[int]: List of terminal nodes numbers
        """

        name: str
        terminals: List[int] = list()
        graph = nx.Graph()

        with graph_file.open("r") as gf:
            for line in gf:
                if line == self._eof_mark:
                    break

                splitted = [substr.strip() for substr in line.split()]
                if len(splitted) < 2:
                    continue

                if splitted[0] == self._name_mark:
                    name = splitted[1]
                    if name[0] == '"' and name[-1] == '"':
                        name = name[1:-1]

                if splitted[0] == self._edge_mark:
                    graph.add_edge(
                        int(splitted[1]), int(splitted[2]), weight=int(splitted[3])
                    )

                if splitted[0] == self._terminal_mark:
                    terminals.append(int(splitted[1]))

        return name, graph, terminals
