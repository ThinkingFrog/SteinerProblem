from pathlib import Path
from typing import Dict, List, Tuple

from steiner.graph import Graph


class STPParser:
    _section_start_mark: str
    _section_end_mark: str
    _eof_mark: str

    _comment_section_name: str
    _comment_name_mark: str
    _comment_creator_mark: str
    _comment_remark_mark: str
    
    _graph_section_name: str
    _nodes_count_mark: str
    _edges_count_mark: str
    _edge_mark: str

    _terminals_section_name: str
    _terminals_count_mark: str
    _terminal_mark: str

    def __init__(self) -> None:
        self._section_start_mark = "SECTION"
        self._section_end_mark = "END"
        self._eof_mark = "EOF"

        self._comment_section_name = "Comment"
        self._comment_name_mark = "Name"
        self._comment_creator_mark = "Creator"
        self._comment_remark_mark = "Remark"

        self._graph_section_name = "Graph"
        self._nodes_count_mark = "Nodes"
        self._edges_count_mark = "Edges"
        self._edge_mark = "E"

        self._terminals_section_name = "Terminals"
        self._terminals_count_mark = "Terminals"
        self._terminal_mark = "T"

    def parse(self, graph_file: Path) -> Tuple[Graph, List[int], Dict[str, str]]:
        """Method to parse STP files

        Args:
            graph_file (Path): Path to stp file

        Returns:
            Graph: Resulting Graph class instance
            List[int]: List of terminal nodes numbers
            Dict[str, str]]: Comment section dict with keys "Name", "Creator", "Remark"
        """

        comment: Dict[str, str] = dict()
        terminals: List[int] = list()

        with graph_file.open('r') as gf:
            for line in gf:
                if line == self._eof_mark:
                    break

                splitted = [substr.strip() for substr in line.split()]
                if len(splitted) < 2:
                    continue

                if splitted[0] == self._comment_name_mark:
                    comment["Name"] = splitted[1]
                if splitted[0] == self._comment_creator_mark:
                    comment["Creator"] = splitted[1]
                if splitted[0] == self._comment_remark_mark:
                    comment["Remark"] = splitted[1]

                if splitted[0] == self._nodes_count_mark:
                    graph = Graph(splitted[1])
                if splitted[0] == self._edge_mark:
                    graph.add_edge(splitted[1], splitted[2], splitted[3])
                
                if splitted[0] == self._terminal_mark:
                    terminals.append(splitted[1])

        return graph, terminals, comment
