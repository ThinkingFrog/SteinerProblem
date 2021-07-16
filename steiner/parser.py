from pathlib import Path
from typing import Dict, List, Tuple

from steiner.graph import Graph


class STPParser:
    _eof_mark: str
    _nodes_count_mark: str
    _edge_mark: str
    _terminal_mark: str

    def __init__(self) -> None:
        self._eof_mark = "EOF"
        self._nodes_count_mark = "Nodes"
        self._edge_mark = "E"
        self._terminal_mark = "T"

    def parse(self, graph_file: Path) -> Tuple[Graph, List[int]]:
        """Method to parse STP files

        Args:
            graph_file (Path): Path to stp file

        Returns:
            Graph: Resulting Graph class instance
            List[int]: List of terminal nodes numbers
        """

        terminals: List[int] = list()

        with graph_file.open("r") as gf:
            for line in gf:
                if line == self._eof_mark:
                    break

                splitted = [substr.strip() for substr in line.split()]
                if len(splitted) < 2:
                    continue

                if splitted[0] == self._nodes_count_mark:
                    graph = Graph(splitted[1])
                if splitted[0] == self._edge_mark:
                    graph.add_edge(splitted[1], splitted[2], splitted[3])

                if splitted[0] == self._terminal_mark:
                    terminals.append(splitted[1])

        return graph, terminals
